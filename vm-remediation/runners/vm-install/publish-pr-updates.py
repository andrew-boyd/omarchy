"""Publish the user-authorized final handoff to the 17 existing draft PRs only."""
from pathlib import Path
import json, subprocess, hashlib, datetime

root=Path(__file__).resolve().parents[2]
local=root/'reviews/vm-install'
wave=root/'.state/vm-install/2026-09-20'
gh='/home/boyd/.local/share/mise/installs/gh/2.101.0/gh_2.101.0_linux_amd64/bin/gh'
index=wave/'pr-followups/review-index'
index_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=index,text=True).strip()
remote=subprocess.check_output(['git','ls-remote','https://github.com/andrew-boyd/omarchy.git','refs/heads/intel-mac/review-index'],text=True).split()[0]
assert remote==index_commit,'Publish evidence index before editing PR bodies'
api=lambda path:json.loads(subprocess.check_output([gh,'api',path],text=True))
# A live GitHub read proves the evidence is reachable before any PR links to it.
evidence=api('repos/andrew-boyd/omarchy/contents/vm-validation/HANDOFF.md?ref=intel-mac/review-index')
assert evidence['type']=='file'
records=json.loads((local/'prepared-pr-updates.json').read_text())
assert len(records)==17
receipts=[]
for row in records:
    endpoint=f"repos/{row['repository']}/pulls/{row['number']}"
    before=api(endpoint)
    assert before['state']=='open' and before['draft'],row['id']
    assert before['head']['sha']==row['expected_head'],row['id']+' head changed'
    body=Path(row['body_file']).read_text()
    current_hash=hashlib.sha256(before['body'].encode()).hexdigest()
    assert current_hash in (row['before_sha256'],row['after_sha256']),row['id']+' body changed'
    if current_hash!=row['after_sha256']:
        subprocess.run([gh,'pr','edit',str(row['number']),'--repo',row['repository'],'--body-file',row['body_file']],check=True,capture_output=True,text=True)
    after=api(endpoint)
    assert after['body']==body and after['draft'] and after['state']=='open'
    assert after['head']['sha']==row['expected_head']
    receipts.append({'id':row['id'],'url':after['html_url'],'head':after['head']['sha'],'body_sha256':hashlib.sha256(after['body'].encode()).hexdigest(),'body_verified':True,'still_open_draft':True,'original_source_urls_preserved':row['original_source_urls_preserved'],'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    report={'index_commit':index_commit,'index_url':'https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/HANDOFF.md','index_live_verified':True,'completed_count':len(receipts),'expected_count':17,'prs':receipts,'original_source_prs_modified':False,'basecamp_or_chat_posted':False}
    (local/'published-pr-updates.json').write_text(json.dumps(report,indent=2)+'\n')
    print(row['id'],'updated and verified',flush=True)
