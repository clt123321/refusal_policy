from __future__ import annotations

import argparse
import hashlib
import gc
import json
import time
from pathlib import Path

from src.execution.repair_runner import verify_execution_checkout


def _file_hashes(directory: Path) -> dict[str, str]:
    return {
        path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.rglob("*")) if path.is_file()
    }


def _generate_arm(model, tokenizer, selected, arm: str, device: str, torch) -> list[dict]:
    records = []
    for sample in selected:
        rendered = tokenizer.apply_chat_template(
            [{"role": "user", "content": sample["behavior"]}],
            tokenize=False, add_generation_prompt=True,
        )
        inputs = tokenizer(rendered, return_tensors="pt").to(device)
        with torch.inference_mode():
            output = model.generate(
                **inputs, max_new_tokens=256, do_sample=False,
                pad_token_id=tokenizer.pad_token_id,
            )
        generated_tokens = int(output.shape[1] - inputs["input_ids"].shape[1])
        records.append({
            "arm": arm, "sample_id": sample["sample_id"],
            "behavior_id": sample["behavior_id"], "behavior": sample["behavior"],
            "input_tokens": int(inputs["input_ids"].shape[1]),
            "generated": tokenizer.decode(
                output[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True,
            ),
            "generated_tokens": generated_tokens,
            "hit_max_new_tokens": generated_tokens >= 256,
        })
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--adapter", type=Path, required=True)
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execution-sha", required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    verify_execution_checkout(args.repo, args.execution_sha)
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer
    samples=json.loads(args.samples.read_text())["samples"]
    by_behavior={}
    for sample in samples:
        bid=sample["behavior_id"]
        digest=hashlib.sha256(f"17\0{bid}".encode()).hexdigest()
        if bid not in by_behavior or digest < by_behavior[bid][0]:
            by_behavior[bid]=(digest,sample)
    selected=[item for _,item in sorted(by_behavior.values(),key=lambda x:x[0])[:16]]
    tokenizer=AutoTokenizer.from_pretrained(args.base.as_posix())
    if tokenizer.pad_token is None: tokenizer.pad_token=tokenizer.eos_token
    torch.cuda.reset_peak_memory_stats()
    started=time.time()
    base_model=AutoModelForCausalLM.from_pretrained(args.base.as_posix(),torch_dtype=torch.float16).to(args.device).eval()
    records=_generate_arm(base_model, tokenizer, selected, "B", args.device, torch)
    del base_model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    repair_base=AutoModelForCausalLM.from_pretrained(args.base.as_posix(),torch_dtype=torch.float16).to(args.device).eval()
    repair_model=PeftModel.from_pretrained(repair_base,args.adapter.as_posix()).eval()
    records.extend(_generate_arm(repair_model, tokenizer, selected, "R_cal", args.device, torch))
    result={"status":"DEV_GENERATION_COMPLETE","execution_sha":args.execution_sha,"model":{"repo_id":"Qwen/Qwen2.5-1.5B-Instruct","revision":"989aa7980e4cf806f80c7fef2b1adb7bc71aa306","base":str(args.base),"base_file_hashes":_file_hashes(args.base),"repair_adapter":str(args.adapter),"repair_adapter_file_hashes":_file_hashes(args.adapter),"arm_state_isolation":"B generated before adapter load; R_cal loaded from a fresh base instance","dtype":"float16","chat_template":"native","max_new_tokens":256,"do_sample":False},"samples_file_sha256":hashlib.sha256(args.samples.read_bytes()).hexdigest(),"selection":{"seed":17,"count":len(selected),"behavior_ids":[x["behavior_id"] for x in selected],"selection_rule":"stable SHA256 seed/behavior_id order from fixed precheck coverage"},"wall_seconds":time.time()-started,"peak_memory_bytes":int(torch.cuda.max_memory_allocated()),"records":records}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!="records"},ensure_ascii=False,indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
