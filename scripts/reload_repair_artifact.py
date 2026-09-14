import json
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = Path("/root/.cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/snapshots/989aa7980e4cf806f80c7fef2b1adb7bc71aa306")
adapter = Path("/tmp/v6_repair_dev/output_cpu/adapter")
tokenizer = AutoTokenizer.from_pretrained(base.as_posix())
model = AutoModelForCausalLM.from_pretrained(base.as_posix(), torch_dtype=torch.float32).eval()
loaded = PeftModel.from_pretrained(model, adapter.as_posix()).eval()
finite = all(bool(torch.isfinite(p).all()) for p in loaded.parameters())
print(json.dumps({"reload_pass": True, "finite": finite, "adapter_files": sorted(p.name for p in adapter.iterdir())}, indent=2))
