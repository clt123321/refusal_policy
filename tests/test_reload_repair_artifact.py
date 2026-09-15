import sys
import types

from scripts.reload_repair_artifact import build_parser, validate_reload


def test_reload_cli_has_no_implicit_development_paths():
    args = build_parser().parse_args([
        "--base", "/model", "--adapter", "/adapter", "--receipt", "/receipt.json",
    ])
    assert str(args.base) == "/model"
    assert str(args.adapter) == "/adapter"
    assert str(args.receipt) == "/receipt.json"


def test_reference_mismatch_fails_reload(monkeypatch, tmp_path):
    import torch

    base = tmp_path / "base"
    base.mkdir()
    (base / "config.json").write_text("{}")
    adapter = tmp_path / "adapter"
    adapter.mkdir()
    (adapter / "adapter_config.json").write_text("{}")
    reference = tmp_path / "reference.pt"
    torch.save(torch.ones((1, 2)), reference)

    class Batch(dict):
        def to(self, _device):
            return self

    class Tokenizer:
        eos_token_id = 2

        @classmethod
        def from_pretrained(cls, _path):
            return cls()

        def apply_chat_template(self, *args, **kwargs):
            return "prompt"

        def __call__(self, *args, **kwargs):
            return Batch(input_ids=torch.tensor([[1]]))

        def decode(self, *args, **kwargs):
            return "SAFE"

    class Output:
        logits = torch.zeros((1, 1, 2))

    class Model:
        @classmethod
        def from_pretrained(cls, *args, **kwargs):
            return cls()

        def to(self, _device):
            return self

        def eval(self):
            return self

        def parameters(self):
            return [torch.zeros(1)]

        def __call__(self, **kwargs):
            return Output()

        def generate(self, **kwargs):
            return torch.tensor([[1, 2]])

    class Peft:
        @classmethod
        def from_pretrained(cls, model, _path):
            return model

    monkeypatch.setitem(sys.modules, "peft", types.SimpleNamespace(PeftModel=Peft))
    monkeypatch.setitem(
        sys.modules,
        "transformers",
        types.SimpleNamespace(AutoModelForCausalLM=Model, AutoTokenizer=Tokenizer),
    )
    result = validate_reload(base, adapter, "cpu", "float32", reference)
    assert result["memory_reload_comparison"]["within_tolerance"] is False
    assert result["reload_pass"] is False
