#!/usr/bin/python
"""Prepare existing draft bodies from verified receipts; never publish."""
from pathlib import Path
import json,re,hashlib
root=Path(__file__).resolve().parents[2];w=root/'.state/vm-install/2026-09-20';p=w/'remediation';out=p/'bodies';out.mkdir(exist_ok=True)
results=json.loads((root/'reviews/remediation/results.json').read_text())
required=['build7-artifact','build7-integration','build7-runtime-followups','build7-audio-pro','build7-t1bridge','build7-spi-pio','build7-nvme','old-snapshot-guard','P12-packages-self-tests','focused-branch-rechecks','missing-rechecks','build7-acceptance-clean-rerun','build7-encrypted-acceptance']
assert all(results['stages'].get(n)==0 for n in required),'Validation is not complete; do not prepare passing claims.'
assert all(r['aggregate_exit'] is not None for r in results['original_full_suites'])
assert not results['latest_live_pr_changes'],'Intervening remote changes require review.'
runtime=[r for r in results['guest_runs'] if r['run'].endswith('-remediation-runtime')]
assert len(runtime)==1 and runtime[0]['checks'].get('test-all.exit')==0
# Verify actual file coverage, not just the wrapper's exit: an earlier SSH
# invocation consumed the list stdin and silently skipped remaining files.
for suite in results['original_full_suites']:
 for test in suite['failed_files']:
  if test.endswith('/preinstalls-test.sh'):
   assert any(r['checks'].get(suite['id']+'.exit')==0 for r in results['guest_runs'] if 'preinstalls-assertion-rechecks' in r['run'])
  else:
   suffix='-recheck-'+suite['id']+'-'+Path(test).stem
   assert any(r['run'].endswith(suffix) and r['exit']==0 for r in results['guest_runs']), (suite['id'],test)
branches={r['id']:r for r in results['prepared_branches']};full={r['id']:r for r in results['original_full_suites']}
revisions=json.loads((p/'body-revisions.json').read_text())
public='https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-remediation/'
records=[]
for f in sorted((p/'live-prs').glob('*.json')):
 ident=f.stem;pr=json.loads(f.read_text());old=pr['body'];body=old;rev=revisions.get(ident,{})
 if rev.get('summary'):
  begin=body.index('\n\n')+2;end=body.index('\n\n**Draft consolidation',begin)
  body=body[:begin]+rev['summary']+body[end:]
 if rev.get('gaps'):
  begin=body.index('## Known gaps and follow-up work');end=body.index('Hardware reports',begin)
  body=body[:begin]+'## Known gaps and follow-up work\n\n'+''.join('- [ ] '+x+'\n' for x in rev['gaps'])+'\n'+body[end:]
 if ident=='P06':
  body=body.replace('The source migration does not enforce this prerequisite.','The migration enforces package and native-module prerequisites; it cannot verify the manual firmware/live-provider transition.')
  body=body.replace('manual P12 prerequisite is not automatically enforced.','manual P12 transition is still required; the follow-up checks packages/native modules only.')
 if ident=='P09':
  body=body.replace('Complete omacom/omarchy#11624 is accepted as the provisional','omacom/omarchy#11624, with the documented software-preservation follow-ups, is accepted as the provisional')
  body=body.replace('with unit-preservation and applicability gaps documented.','with the original findings and remaining physical applicability boundary documented.')
 table_changes={
  'Six production files match; target heredoc delimiter retained.':'The original consolidation preserved six production files apart from the target heredoc delimiter; a later follow-up makes attribute reads race-safe.',
  'Complete narrower Apple-controller starting point; custom-unit overwrite/deletion and unknown-state findings preserved. Accepted as a provisional consolidation target with those documented gaps.':'Narrower Apple-controller starting point; original custom-unit and unknown-state findings remain recorded. Software follow-ups preserve custom units and leave unknown identity pending; physical applicability remains provisional.',
  'with original overwrite and lost-retry defects preserved.':'with the original overwrite and lost-retry defects recorded. The follow-up preserves customized hooks and failed rebind state.',
  'inherited overwrite/route-reset/failure behavior retained.':'original configuration/route risks recorded. Follow-ups preserve customized files and routes and make repeated setup safe.',
  'paired with package omacom/omarchy-pkgs#249 and original model/header policy.':'paired with package omacom/omarchy-pkgs#249. The follow-up anchors the documented model set and uses matching kernel headers.',
 }
 begin=body.index('## Every reviewed source PR');end=body.index('<details>',begin)
 table=body[begin:end]
 for before,after in table_changes.items():table=table.replace(before,after)
 body=body[:begin]+table+body[end:]
 # Preserve dated older reports as history, including their actual failures.
 begin=body.index('## ISO / VM validation —');end=body.index('## Scope and dependencies',begin)
 history=body[begin:end]
 body=body[:begin]+'<details>\n<summary>Earlier ISO/VM validation, before these software repairs</summary>\n\n'+history+'\n</details>\n\n'+body[end:]
 head=branches[ident]['head'] if ident in branches else pr['headRefOid']
 section='## Rebuilt ISO and software follow-up — 2026-09-21 UTC\n\n'
 section+='Current draft head: `'+head+'`. Original contribution commits and attribution are preserved.\n\n'
 section+='The repaired combined ISO built and completed fresh unencrypted and encrypted installation/reboot checks. All 13 embedded local package archives and 52 changed runtime payloads were verified against the pinned source. Clean desktop acceptance reruns passed all eight files. The original interrupted/failed harness runs remain in the report; focused reruns are not relabeled as green original aggregates.\n\n'
 section+='**The ISO is not entirely green:** the stricter editor-startup check still fails because the unchanged baseline Neovim package requests an unavailable theme repository. A guest-only replacement-source experiment passed, but that repair is not in this ISO or these feature branches. The earlier acceptance suite did not catch that error.\n\n'
 if ident in branches:
  if ident.endswith('packages'):
   section+='- **This branch:** the optional brightness-controller repair is in the package companion; 12 repository self-test groups passed. Its production checks ran during the ISO package build. The existing stable dependency and the local ISO adapter remain explicitly separate.\n'
  else:
   r=full[ident]
   section+='- **This branch:** complete CLI/shell suite at `'+r['tested_commit']+'` returned **'+str(r['aggregate_exit'])+'**.'
   if r['failed_files']:section+=' Failed files: '+', '.join('`'+x+'`' for x in r['failed_files'])+'.'
   section+=' The later change is a test-only repair for the reproduced preinstall SIGPIPE assertion race; its focused check and each observed failed file were rechecked in fresh guest overlays. See the exact logs and commits below.\n'
  section+='- **Follow-up diff:** [software/test changes]('+public+'followups/'+ident+'.patch); the source-author contribution commits remain ancestors of this head.\n'
 else:
  section+='- **This branch:** no additional runtime changes in this remediation. Earlier per-feature checks remain dated evidence; inclusion in the new combined ISO does not silently repeat every earlier hardware-specific scenario.\n'
 section+='- **Combined baseline:** shared-ESP factory reset now passes staging, unattended first boot and provisioning while preserving foreign entries/files. An older unsafe factory snapshot is refused. These baseline repairs are supplied in the integration evidence, not inserted into unrelated feature branches.\n'
 section+='- **Boundary:** physical Intel Mac behavior and signed distribution delivery remain unverified. DMI/device input fixtures and virtual RTC/NVMe checks do not emulate Apple hardware.\n\n'
 section+='[Current handoff]('+public+'HANDOFF.md) · [Exact test/artifact receipts]('+public+'receipts/results.json) · [Reproduction]('+public+'REPRODUCE.md) · [Pinned source bundles]('+public+'integration/sources.json).\n\n'
 marker='<details>\n<summary>Earlier ISO/VM validation, before these software repairs</summary>'
 body=body.replace(marker,section+marker,1)
 # Every originally referenced PR survives, including rejected alternatives.
 pattern=r'https://github.com/[^/\s)]+/[^/\s)]+/pull/\d+'
 refs=set(re.findall(pattern,old));assert refs<=set(re.findall(pattern,body)),ident
 body+='\nSoftware repairs and test-harness corrections are subsequent agent-assisted commits by the consolidating contributor; original author credit does not imply approval of those follow-ups.\n'
 target=out/(ident+'.md');target.write_text(body)
 records.append({'id':ident,'url':pr['url'],'old_head':pr['headRefOid'],'expected_head':head,'head_branch':pr['headRefName'],'body_file':str(target),'old_body_sha256':hashlib.sha256(old.encode()).hexdigest(),'new_body_sha256':hashlib.sha256(body.encode()).hexdigest(),'source_pr_urls_preserved':len(refs)})
assert len(records)==17
(p/'prepared-pr-updates.json').write_text(json.dumps(records,indent=2)+'\n')
print('Prepared 17 existing draft bodies. No remote writes.')
