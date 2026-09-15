import sys
import types

import pytest

import scripts.generate_harmbench_checkpoints as checkpoint_generation
from scripts.run_harmbench_classifier_precheck import (
    SentencePieceMistralTokenizer,
    classify_generation,
)


def test_native_sentencepiece_keeps_unknown_token_on_decode(monkeypatch, tmp_path):
    class Processor:
        def __init__(self, model_file):
            self.model_file = model_file

        def bos_id(self): return 1
        def eos_id(self): return 2
        def unk_id(self): return 0
        def vocab_size(self): return 32000
        def encode(self, text, out_type): return [0, 5]
        def decode(self, ids): return repr(ids)

    monkeypatch.setitem(
        sys.modules,
        "sentencepiece",
        types.SimpleNamespace(SentencePieceProcessor=Processor),
    )
    tokenizer = SentencePieceMistralTokenizer(tmp_path / "tokenizer.model")
    assert tokenizer.encode("x") == [1, 0, 5]
    assert tokenizer.decode([1, 0, 5, 2]) == "[0, 5]"
    assert tokenizer.pad_token_id == tokenizer.eos_token_id


def test_classifier_rejects_overlength_before_model_call():
    class Tokenizer:
        pad_token_id = 2
        def encode(self, _text): return [1, 4, 5]

    with pytest.raises(RuntimeError, match="CLASSIFIER_INPUT_EXCEEDS_CONTEXT"):
        classify_generation(None, Tokenizer(), "behavior", "generation", "cpu", None, 3)


def test_b_generation_precedes_adapter_and_r_cal_uses_fresh_base(monkeypatch):
    events = []
    loaded_bases = []

    class Model:
        def __init__(self, identity):
            self.identity = identity

    def load_base():
        model = Model(f"base-{len(loaded_bases) + 1}")
        loaded_bases.append(model)
        events.append(("load_base", model.identity))
        return model

    def load_adapter(base_model):
        events.append(("load_adapter", base_model.identity))
        return Model(f"adapted-{base_model.identity}")

    def generate_arm(model, _tokenizer, _selected, arm, _device, _torch):
        events.append(("generate", arm, model.identity))
        return [{"arm": arm}]

    fake_torch = types.SimpleNamespace(
        cuda=types.SimpleNamespace(is_available=lambda: False),
    )
    monkeypatch.setattr(checkpoint_generation, "_generate_arm", generate_arm)
    records = checkpoint_generation._generate_isolated_arms(
        load_base, load_adapter, None, [], "cpu", fake_torch,
    )

    assert records == [{"arm": "B"}, {"arm": "R_cal"}]
    assert events == [
        ("load_base", "base-1"),
        ("generate", "B", "base-1"),
        ("load_base", "base-2"),
        ("load_adapter", "base-2"),
        ("generate", "R_cal", "adapted-base-2"),
    ]
    assert loaded_bases[0] is not loaded_bases[1]
