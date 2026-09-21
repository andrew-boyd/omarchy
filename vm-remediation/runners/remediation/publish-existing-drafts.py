#!/usr/bin/python
"""Publish authorized follow-ups to existing branches/drafts; never create PRs."""
from pathlib import Path
import subprocess, json, hashlib, datetime, concurrent.futures, time
root=Path(__file__).resolve().parents[2];w=root/'.state/vm-install/2026-09-20';p=w/'remediation'
index=w/'pr-followups/review-index'
gh='/home/boyd/.local/share/mise/installs/gh/2.101.0/gh_2.101.0_linux_amd64/bin/gh'
records=json.loads((p/'prepared-pr-updates.json').read_text())
branches={r['id']:r for r in json.loads((p/'branch-preparation.json').read_text())}
assert len(records)==17 and len(branches)==10
def run(args,**kwargs):return subprocess.check_output(args,text=True,**kwargs)
def git(repo,*args):return run(['git','-C',str(repo),*args]).strip()
def api(path):return json.loads(run([gh,'api',path]))
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def remote_head(repo,branch):
 lines=run(['git','ls-remote','https://github.com/andrew-boyd/'+repo+'.git','refs/heads/'+branch]).split()
 assert len(lines)==2,(repo,branch,lines)
 return lines[0]
def check(row):
 parts=row['url'].split('/');repo='/'.join(parts[3:5]);number=parts[-1]
 assert repo in {'omacom/omarchy','omacom/omarchy-pkgs'}
 live=api('repos/'+repo+'/pulls/'+number)
 assert live['state']=='open' and live['draft'],row['id']
 assert live['head']['repo']['owner']['login']=='andrew-boyd'
 assert live['head']['ref']==row['head_branch']
 assert live['head']['sha'] in {row['old_head'],row['expected_head']},row['id']+' intervening head'
 assert digest(live['body']) in {row['old_body_sha256'],row['new_body_sha256']},row['id']+' intervening body'
 original=json.loads((p/'live-prs'/(row['id']+'.json')).read_text())
 assert live['base']['ref']==original['baseRefName'] and live['base']['sha']==original['baseRefOid'],row['id']+' changed base'
 return row['id'],live
# Independent read-only preflight finishes for every PR before any write.
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 preflight=dict(pool.map(check,records))
for row in records:
 if row['id'] not in branches:continue
 local=Path(branches[row['id']]['path'])
 assert git(local,'rev-parse','HEAD')==row['expected_head']
 subprocess.run(['git','-C',str(local),'merge-base','--is-ancestor',row['old_head'],row['expected_head']],check=True)
 assert not git(local,'status','--porcelain')
 repo='omarchy-pkgs' if row['id'].endswith('-packages') else 'omarchy'
 assert remote_head(repo,row['head_branch']) in {row['old_head'],row['expected_head']}
assert not git(index,'status','--porcelain'),'Commit reviewable evidence before publishing'
index_head=git(index,'rev-parse','HEAD')
remote_index=remote_head('omarchy','intel-mac/review-index')
subprocess.run(['git','-C',str(index),'merge-base','--is-ancestor',remote_index,index_head],check=True)
subprocess.run(['git','-C',str(index),'push','https://github.com/andrew-boyd/omarchy.git','HEAD:refs/heads/intel-mac/review-index'],check=True)
assert remote_head('omarchy','intel-mac/review-index')==index_head
evidence=api('repos/andrew-boyd/omarchy/contents/vm-remediation/HANDOFF.md?ref=intel-mac/review-index')
assert evidence['type']=='file'
receipts=[]
for row in records:
 if row['id'] in branches:
  repo='omarchy-pkgs' if row['id'].endswith('-packages') else 'omarchy'
  subprocess.run(['git','-C',branches[row['id']]['path'],'push','https://github.com/andrew-boyd/'+repo+'.git','HEAD:refs/heads/'+row['head_branch']],check=True)
  assert remote_head(repo,row['head_branch'])==row['expected_head']
 # The Git ref can be updated before GitHub refreshes its PR head record.
 # Accept neither an unexpected head nor a body edit against the stale one.
 for attempt in range(15):
  _,before=check(row)
  if before['head']['sha']==row['expected_head']:break
  time.sleep(2)
 assert before['head']['sha']==row['expected_head'],row['id']+' PR head did not catch up with verified Git ref'
 parts=row['url'].split('/');repo='/'.join(parts[3:5]);number=parts[-1]
 body=Path(row['body_file']).read_text();assert digest(body)==row['new_body_sha256']
 if digest(before['body'])!=row['new_body_sha256']:
  subprocess.run([gh,'pr','edit',number,'--repo',repo,'--body-file',row['body_file']],check=True,capture_output=True,text=True)
 after=api('repos/'+repo+'/pulls/'+number)
 assert after['body']==body and after['draft'] and after['state']=='open'
 assert after['head']['sha']==row['expected_head']
 receipts.append({'id':row['id'],'url':row['url'],'head':after['head']['sha'],'body_sha256':digest(after['body']),'still_open_draft':True,'body_verified':True,'source_pr_urls_preserved':row['source_pr_urls_preserved'],'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 report={'index_commit':index_head,'index_url':'https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-remediation/HANDOFF.md','index_live_verified':True,'completed_count':len(receipts),'expected_count':17,'prs':receipts,'original_source_prs_modified':False,'basecamp_or_chat_posted':False}
 (root/'reviews/remediation/published-pr-updates.json').write_text(json.dumps(report,indent=2)+'\n')
 print(row['id'],'updated and verified',flush=True)
