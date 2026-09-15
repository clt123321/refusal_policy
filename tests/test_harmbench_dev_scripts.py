import sys
import types

import pytest

from scripts.generate_harmbench_checkpoints import _generate_arm
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


def test_generation_helper_records_the_supplied_arm():
    import torch

    class Batch(dict):
        def to(self, _device): return self

    class Tokenizer:
        pad_token_id = 2
        def apply_chat_template(self, *args, **kwargs): return "prompt"
        def __call__(self, *args, **kwargs): return Batch(input_ids=torch.tensor([[1, 3]]))
        def decode(self, *args, **kwargs): return "answer"

    class Model:
        def generate(self, **kwargs): return torch.tensor([[1, 3, 4]])

    records = _generate_arm(
        Model(), Tokenizer(),
        [{"sample_id": "s", "behavior_id": "b", "behavior": "prompt"}],
        "B", "cpu", torch,
    )
    assert records[0]["arm"] == "B"
    assert records[0]["generated_tokens"] == 1
