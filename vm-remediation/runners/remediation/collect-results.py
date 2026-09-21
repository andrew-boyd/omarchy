#!/usr/bin/python
"""Collect observed results without converting focused reruns into full passes."""
from pathlib import Path
import json,datetime,re,hashlib
root=Path(__file__).resolve().parents[2];w=root/'.state/vm-install/2026-09-20';p=w/'remediation';b=w/'builds/build-20260921T043945Z-Fj2O1V'
b6=w/'builds/build-20260921T030051Z-m0fg6D'
full=b6/'sources/omarchy-iso/test-runs/omarchy-2026.09.21-intel-mac-local-x86_64-integration/runs/20260921-005008-remediation-branch-suites'
def exit_code(f):return int(f.read_text().strip()) if f.exists() else None
def receipt(f):return json.loads(f.read_text()) if f.exists() else None
def sha(f):
 with f.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
stages=['build7-artifact','build7-acceptance','build7-integration','build7-runtime','build7-runtime-followups','build7-audio-pro','build7-t1bridge','build7-spi-pio','build7-nvme','old-snapshot-guard','P12-packages-self-tests','focused-branch-rechecks','missing-rechecks','build7-acceptance-clean-rerun','build7-encrypted-acceptance']
records=[]
for name in ['integration','P03','P05','P06','P07','P09','P10','P11','P13','P14']:
 log=full/(name+'.log');commit=full/(name+'.commit');s=log.read_text(errors='replace') if log.exists() else ''
 records.append({'id':name,'tested_commit':commit.read_text().strip() if commit.exists() else None,'aggregate_exit':exit_code(full/(name+'.exit')),'log':str(log),'log_sha256':sha(log) if log.exists() else None,'failed_files':re.findall(r'^  (test/shell.d/[a-z0-9-]+-test.sh)$',s,re.M),'all_shell_files_passed':re.findall(r'^All (\d+) test files passed\.$',s,re.M)})
runs=[]
for build in [b6,b]:
 for d in (build/'sources/omarchy-iso/test-runs').glob('*integration/runs/*'):
  if not any(x in d.name for x in ['remediation-runtime','factory-reset','mac-packages','mac-migration','mac-nvme','old-snapshot-refusal','preinstalls-assertion-rechecks','recheck-']):continue
  if build==b6 and not any(x in d.name for x in ['old-snapshot-refusal','preinstalls-assertion-rechecks','recheck-']):continue
  runs.append({'build':build.name,'run':d.name,'path':str(d),'exit':exit_code(d/'scenario.exit'),'checks':{f.name:exit_code(f) for f in d.glob('*.exit')},'logs':[{'name':f.name,'bytes':f.stat().st_size,'sha256':sha(f)} for f in d.glob('*.log') if f.name!='serial.log']})
result={'collected_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artifact':receipt(b/'verification/artifact.json'),'stages':{n:exit_code(p/(n+'.exit')) for n in stages},'original_full_suites':records,'prepared_branches':receipt(p/'branch-preparation.json'),'guest_runs':runs,'first_acceptance_failure':receipt(p/'build7-first-acceptance-vt-failure.json'),'latest_live_pr_changes':receipt(p/'live-pr-delta.json'),'physical_mac_validation':False,'publication':'No remediation changes pushed yet; verify this field when publishing.'}
published=receipt(root/'reviews/remediation/published-pr-updates.json')
if published:
 result['publication']={'updated_existing_drafts':published['completed_count'],'expected_drafts':published['expected_count'],'receipt':'published-pr-updates.json','evidence_commit_at_body_publication':published['index_commit']}
 result['live_pr_comparison_scope']='Before these authorized follow-up pushes and body updates; the comparison found no intervening third-party changes.'
(root/'reviews/remediation/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'stages':result['stages'],'source_suites':{r['id']:r['aggregate_exit'] for r in records}},indent=2))
