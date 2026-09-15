from __future__ import annotations
import argparse,hashlib,json,time
from pathlib import Path
from scripts.run_harmbench_classifier_precheck import MISTRAL_CLS_PROMPT,SentencePieceMistralTokenizer,parse_label
from src.execution.repair_runner import verify_execution_checkout
def main():
 p=argparse.ArgumentParser(); p.add_argument('--model',type=Path,required=True); p.add_argument('--generation',type=Path,required=True); p.add_argument('--output',type=Path,required=True); p.add_argument('--execution-sha',required=True); p.add_argument('--device',default='cuda'); p.add_argument('--repo',type=Path,default=Path('.')); a=p.parse_args(); verify_execution_checkout(a.repo,a.execution_sha)
 import torch; from transformers import AutoModelForCausalLM
 cfg=json.loads((a.model/'config.json').read_text()); assert cfg['model_type']=='mistral' and cfg['hidden_size']==4096 and cfg['num_hidden_layers']==32
 tok=SentencePieceMistralTokenizer(a.model/'tokenizer.model'); max_input_tokens=int(cfg.get('max_position_embeddings',0)); model=AutoModelForCausalLM.from_pretrained(str(a.model),torch_dtype=torch.bfloat16).to(a.device).eval(); data=json.loads(a.generation.read_text()); torch.cuda.reset_peak_memory_stats(); start=time.time(); scored=[]
 for r in data['records']:
  prompt=MISTRAL_CLS_PROMPT.format(behavior=r['behavior'],generation=r['generated']); ids=tok.encode(prompt); assert max_input_tokens and len(ids)+1<=max_input_tokens, 'CLASSIFIER_INPUT_EXCEEDS_CONTEXT'; x={'input_ids':torch.tensor([ids],device=a.device),'attention_mask':torch.ones((1,len(ids)),dtype=torch.long,device=a.device)}
  with torch.inference_mode(): y=model.generate(**x,max_new_tokens=1,do_sample=False,pad_token_id=tok.eos_token_id)
  new=y[0,len(ids):].detach().cpu().tolist(); raw=tok.decode(new); scored.append({**{k:r[k] for k in ['arm','sample_id','behavior_id','generated_tokens','hit_max_new_tokens']},'classifier_raw_new_token':raw,'classifier_label':parse_label(raw),'classifier_input_tokens':len(ids)})
 by={};
 for r in scored: by.setdefault(r['sample_id'],{})[r['arm']]=r
 summary={arm:{'yes':sum(r['classifier_label']=='yes' for r in scored if r['arm']==arm),'no':sum(r['classifier_label']=='no' for r in scored if r['arm']==arm),'unknown':sum(r['classifier_label']=='UNKNOWN' for r in scored if r['arm']==arm),'n':sum(r['arm']==arm for r in scored),'max_length':sum(r['hit_max_new_tokens'] for r in scored if r['arm']==arm)} for arm in ['B','R_cal']}
 pairs=[]
 for sid,x in by.items(): pairs.append({'sample_id':sid,'behavior_id':x['B']['behavior_id'],'B':x['B']['classifier_label'],'R_cal':x['R_cal']['classifier_label'],'B_generated_tokens':x['B']['generated_tokens'],'R_cal_generated_tokens':x['R_cal']['generated_tokens']})
 out={'status':'DEV_CHECKPOINT_CONTENT_EVAL_COMPLETE','execution_sha':a.execution_sha,'classifier':{'repo_id':'cais/HarmBench-Mistral-7b-val-cls','revision':'51182c7cdaf9b2e5f05b745b81b047b67e7384a1','prompt_template':'official MISTRAL_CLS_PROMPT','tokenizer':'native SentencePiece','tokenizer_model_sha256':hashlib.sha256((a.model/'tokenizer.model').read_bytes()).hexdigest(),'config_sha256':hashlib.sha256((a.model/'config.json').read_bytes()).hexdigest(),'reference_token_id_equivalence':'NOT_ESTABLISHED_BY_THIS_RUN','dtype':'bfloat16','chat_template_used':False,'max_new_tokens':1,'max_input_tokens':max_input_tokens},'generation_source':str(a.generation),'generation_source_sha256':hashlib.sha256(a.generation.read_bytes()).hexdigest(),'generation_execution_sha':data.get('execution_sha'),'generation_model_identity':data.get('model'),'wall_seconds':time.time()-start,'peak_memory_bytes':int(torch.cuda.max_memory_allocated()),'summary':summary,'pairs':pairs,'scored_records':scored}; a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)); print(json.dumps({k:v for k,v in out.items() if k not in ['pairs','scored_records']},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
