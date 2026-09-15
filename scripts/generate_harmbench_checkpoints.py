from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--adapter", type=Path, required=True)
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execution-sha", required=True)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()
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
    base=AutoModelForCausalLM.from_pretrained(args.base.as_posix(),torch_dtype=torch.float16).to(args.device).eval()
    models={"B":base,"R_cal":PeftModel.from_pretrained(base,args.adapter.as_posix()).eval()}
    records=[]
    for arm,model in models.items():
        for sample in selected:
            rendered=tokenizer.apply_chat_template([{"role":"user","content":sample["behavior"]}],tokenize=False,add_generation_prompt=True)
            inputs=tokenizer(rendered,return_tensors="pt").to(args.device)
            with torch.inference_mode(): output=model.generate(**inputs,max_new_tokens=256,do_sample=False,pad_token_id=tokenizer.pad_token_id)
            generated=tokenizer.decode(output[0,inputs["input_ids"].shape[1]:],skip_special_tokens=True)
            records.append({"arm":arm,"sample_id":sample["sample_id"],"behavior_id":sample["behavior_id"],"behavior":sample["behavior"],"input_tokens":int(inputs["input_ids"].shape[1]),"generated":generated,"generated_tokens":int(output.shape[1]-inputs["input_ids"].shape[1]),"hit_max_new_tokens":int(output.shape[1]-inputs["input_ids"].shape[1])>=256})
    result={"status":"DEV_GENERATION_COMPLETE","execution_sha":args.execution_sha,"model":{"repo_id":"Qwen/Qwen2.5-1.5B-Instruct","base":str(args.base),"dtype":"float16","chat_template":"native","max_new_tokens":256,"do_sample":False},"selection":{"seed":17,"count":len(selected),"behavior_ids":[x["behavior_id"] for x in selected],"selection_rule":"stable SHA256 seed/behavior_id order from fixed precheck coverage"},"wall_seconds":time.time()-started,"peak_memory_bytes":int(torch.cuda.max_memory_allocated()),"records":records}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!="records"},ensure_ascii=False,indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
