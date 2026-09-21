#!/usr/bin/python
from pathlib import Path
import subprocess,json,hashlib,os
root=Path(__file__).resolve().parents[2];w=root/'.state/vm-install/2026-09-20';b=w/'builds/build-20260921T043945Z-Fj2O1V';p=w/'remediation';index=w/'pr-followups/review-index';out=index/'vm-remediation/integration';out.mkdir(parents=True,exist_ok=True)
bases={'omarchy':'45748a2812f42e32f915b053caf4074e150e2048','omarchy-pkgs':'4b60e4cd95972c16fbf3da634522a955cf7bf36c','omarchy-iso':'7cfb7111a06873d61c45d37034577d4ba08d3f4f'}
def git(repo,*args,**kw):return subprocess.check_output(['git','-C',str(repo),*args],**kw)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
rows=[]
for name,base in bases.items():
 repo=b/'sources'/name;head=(b/(name+'.commit')).read_text().strip();assert git(repo,'rev-parse','HEAD',text=True).strip()==head
 patch=out/(name+'.patch');patch.write_bytes(git(repo,'diff','--binary',base,head))
 bundle=out/(name+'.bundle');git(repo,'bundle','create',str(bundle),'HEAD','^'+base)
 verify=p/'bundle-verification'/name;verify.mkdir(parents=True,exist_ok=True);git(verify,'init','--quiet')
 git(verify,'fetch','--quiet','--depth=1',str(repo),base)
 git(verify,'bundle','verify',str(bundle),stderr=subprocess.STDOUT)
 git(verify,'fetch','--quiet',str(bundle),'HEAD');git(verify,'checkout','--quiet','--detach',head)
 tree=git(repo,'rev-parse',head+'^{tree}',text=True).strip();assert git(verify,'rev-parse','HEAD^{tree}',text=True).strip()==tree
 patch_index=p/(name+'-verify.index');env=dict(os.environ,GIT_INDEX_FILE=str(patch_index))
 git(verify,'read-tree',base,env=env);git(verify,'apply','--cached',str(patch),env=env);assert git(verify,'write-tree',text=True,env=env).strip()==tree
 rows.append({'repository':'omacom/'+name,'base':base,'tested_commit':head,'tree':tree,'bundle':bundle.name,'bundle_sha256':sha(bundle),'bundle_fresh_base_checkout_verified':True,'patch':patch.name,'patch_sha256':sha(patch),'patch_reconstruction_verified':True})
(out/'sources.json').write_text(json.dumps(rows,indent=2)+'\n')
followups=out.parent/'followups';followups.mkdir(exist_ok=True)
records=json.loads((p/'branch-preparation.json').read_text())
for r in records:
 branch=Path(r['path']);patch=followups/(r['id']+'.patch');patch.write_bytes(git(branch,'diff','--binary',r['original_head'],r['head']))
 r['patch_sha256']=sha(patch);git(branch,'merge-base','--is-ancestor',r['original_head'],r['head'])
 r['original_author_commits_preserved']=True
(followups/'commits.json').write_text(json.dumps(records,indent=2)+'\n')
# Separate test harness adjustment; not a change to the already built artifact.
repo=w/'repos/omarchy-iso';(out/'acceptance-tty4.patch').write_bytes(git(repo,'diff',(b/'omarchy-iso.commit').read_text().strip(),'HEAD','--','bin/omarchy-iso-test'))
print('Verified three source bundles/aggregate patches and',len(records),'follow-up ancestries; no publish.')
