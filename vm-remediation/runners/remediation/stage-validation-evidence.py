#!/usr/bin/python
"""Stage an explicit allowlist of public evidence. No remote writes."""
from pathlib import Path
import json, shutil, hashlib, re

root=Path(__file__).resolve().parents[2]
w=root/'.state/vm-install/2026-09-20';p=w/'remediation'
b=w/'builds/build-20260921T043945Z-Fj2O1V'
out=w/'pr-followups/review-index/vm-remediation'
results=json.loads((root/'reviews/remediation/results.json').read_text())
copied=[]
def copy(src,dest):
 if not src.is_file():return
 dest=out/dest;dest.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(src,dest);copied.append(dest)
copy(root/'reviews/remediation/results.json',Path('receipts/results.json'))
copy(root/'reviews/remediation/REPRODUCE.md',Path('REPRODUCE.md'))
for name in ['branch-runtime-equivalence.json','build7-bootstrap-intervention.json','build7-first-acceptance-vt-failure.json','final-acceptance-harness.json','editor-source-diagnosis.json','focused-recheck-stdin-correction.json','missing-rechecks.json','live-pr-delta.json','live-pr-reconciliation.json']:
 copy(p/name,Path('receipts')/name)
copy(root/'reviews/remediation/checks/host-test-isolation-restoration.json',Path('receipts/host-test-isolation-restoration.json'))
for name in ['artifact.json']:
 copy(b/'verification'/name,Path('receipts')/name)
copy(b/'installed-runtime-payload.json',Path('receipts/installed-runtime-payload.json'))
copy(p/'build7-encrypted-storage.log',Path('receipts/build7-encrypted-storage.log'))
for name in results['stages']:
 for suffix in ['.exit','.log']:
  copy(p/(name+suffix),Path('stages')/(name+suffix))
for name in ['build7-artifact-first-reader-failure','build7-artifact-second-mapping-failure','build7-artifact-third-mapping-failure','preinstalls-pipeline-reproduction','preinstalls-guest-pipeline-reproduction']:
 for suffix in ['.exit','.log']:
  copy(p/(name+suffix),Path('diagnostics')/(name+suffix))
for r in results['original_full_suites']:
 src=Path(r['log'])
 for suffix in ['.log','.exit','.commit']:
  copy(src.with_suffix(suffix),Path('source-suites')/(r['id']+suffix))
allowed={'.log','.exit','.commit','.txt','.json','.sha256','.png'}
for r in results['guest_runs']:
 run=Path(r['path'])
 for f in run.rglob('*'):
  if f.is_file() and f.suffix in allowed and f.name!='serial.log':
   copy(f,Path('guest-runs')/r['run']/f.relative_to(run))
# Only acceptance output and screenshots: no VM disks, EFI variable stores,
# SSH key material, private host snapshots or arbitrary build directories.
for run in (b/'sources/omarchy-iso/test-runs').glob('*/runs/*'):
 if not re.fullmatch(r'\d{8}-\d{6}',run.name):continue
 for f in run.rglob('*'):
  if f.is_file() and (f.suffix=='.png' or f.name in {'acceptance.log','test.log','results.json'}):
   copy(f,Path('acceptance')/run.parent.parent.name/run.name/f.relative_to(run))
for scope in ['remediation','vm-install']:
 for f in (root/'reviews'/scope).iterdir():
  if f.suffix in {'.sh','.py','.patch'}:
   copy(f,Path('runners')/scope/f.name)
# The earlier OCR-only test patch is required to reproduce this exact harness.
old=w/'pr-followups/review-index/vm-validation'
for f in old.rglob('*.patch'):
 if 'acceptance' in f.name or 'ocr' in f.name:
  copy(f,Path('harness')/f.name)

# Refuse publishing obvious real credential shapes. Synthetic test credentials
# and harmless words such as "token" do not trigger this scan.
patterns=[rb'-----BEGIN (?:OPENSSH|RSA|EC|DSA) PRIVATE KEY-----',rb'apikey_[0-9a-f]{32}_',rb'github_pat_[A-Za-z0-9_]{50,}',rb'ghp_[A-Za-z0-9]{36}']
matches=[]
for f in copied:
 if f.suffix not in {'.png','.bundle'} and any(re.search(pat,f.read_bytes()) for pat in patterns):matches.append(str(f.relative_to(out)))
assert not matches, 'Possible credentials in: '+', '.join(matches)
files=[f for f in out.rglob('*') if f.is_file() and f.name!='SHA256SUMS']
(out/'SHA256SUMS').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(out))+'\n' for f in sorted(files)))
print('Staged',len(copied),'allowlisted evidence files;',sum(f.stat().st_size for f in files),'bytes total. No remote writes.')
