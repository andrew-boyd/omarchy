#!/usr/bin/python
from pathlib import Path
import hashlib,subprocess,json,sys
b=Path(sys.argv[1]).resolve();iso=b/'omarchy-2026.09.21-x86_64.iso';out=b/'verification';out.mkdir(exist_ok=True)
unsquashfs=Path(__file__).resolve().parents[2]/'.state/vm-install/2026-09-20/remediation/tools/usr/bin/unsquashfs'
assert (b/'build.exit').read_text().strip()=='0'
def digest(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
sfs=out/'airootfs.sfs'
if not sfs.exists():
 with sfs.open('wb') as f:subprocess.run(['bsdtar','-xOf',str(iso),'arch/x86_64/airootfs.sfs'],stdout=f,check=True)
 assert sfs.stat().st_size>1000000000
expected={n:h for h,n in (x.split(maxsplit=1) for x in (b/'package-sha256sums').read_text().splitlines())}
local_names=set((b/'local-packages').read_text().splitlines())
expected={n:h for n,h in expected.items() if n.rsplit('-',3)[0] in local_names}
assert len(expected)==len(local_names)==13
rows=[]
for filename,h in expected.items():
 package=out/filename
 with package.open('wb') as f:subprocess.run([str(unsquashfs),'-cat',str(sfs),'var/cache/omarchy/mirror/offline/'+filename],stdout=f,check=True)
 actual=digest(package);assert actual==h,filename
 name,version=subprocess.check_output(['pacman','-Qp',str(package)],text=True).strip().split(' ',1)
 rows.append({'name':name,'version':version,'filename':filename,'sha256':actual,'embedded_matches_receipt':True})
repo=b/'sources/omarchy';base='45748a2812f42e32f915b053caf4074e150e2048'
paths=subprocess.check_output(['git','-C',str(repo),'diff','--name-only','--diff-filter=ACM',base,'HEAD'],text=True).splitlines()
archives={r['name']:out/r['filename'] for r in rows};payload=[]
for rel in paths:
 if not rel.startswith(('bin/','default/','install/','migrations/','shell/','lib/')):continue
 archive=archives['omarchy-settings-dev' if rel.startswith('default/') else 'omarchy-dev']
 package_path='usr/'+rel if rel.startswith('bin/') else 'usr/share/omarchy/'+rel
 data=subprocess.check_output(['bsdtar','-xOf',str(archive),package_path]);h=hashlib.sha256(data).hexdigest();assert h==digest(repo/rel),rel
 listing=subprocess.check_output(['bsdtar','-tvf',str(archive),package_path],text=True).split()
 assert listing[2:4]==['root','root'] and listing[0][7]=='r',(rel,listing)
 if rel.startswith('bin/'):assert listing[0][9]=='x',(rel,listing)
 payload.append({'source':rel,'path':'/'+package_path,'sha256':h,'package_mode':listing[0],'root_owned':True})
assert len(rows)==13 and len(payload)>45
(b/'installed-runtime-payload.json').write_text(json.dumps(payload,indent=2)+'\n')
receipt={'iso':str(iso),'bytes':iso.stat().st_size,'sha256':digest(iso),'build_exit':0,'source_commits':{n:(b/(n+'.commit')).read_text().strip() for n in ['omarchy','omarchy-pkgs','omarchy-iso']},'embedded_packages':rows,'changed_runtime_files':payload}
(out/'artifact.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'iso_sha256':receipt['sha256'],'packages':len(rows),'changed_runtime_files':len(payload)}))
