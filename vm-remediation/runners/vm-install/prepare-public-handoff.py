"""Prepare the reviewed VM evidence packet and PR bodies; never publish."""
from pathlib import Path
import json, shutil, hashlib, re, subprocess

root = Path(__file__).resolve().parents[2]
wave = root / '.state/vm-install/2026-09-20'
local = root / 'reviews/vm-install'
index = wave / 'pr-followups/review-index'
out = index / 'vm-validation'
b5 = wave / 'builds/build-20260921T014550Z-X4tHsG'
b6 = wave / 'builds/build-20260921T030051Z-m0fg6D'
assert (b6 / 'acceptance.exit').read_text().strip() == '0'
assert (b6 / 'audio12-retest.exit').read_text().strip() == '0'
coverage = json.loads((local / 'coverage.json').read_text())
assert len(coverage) == 14 and all(x['vm_result'].startswith('passed') for x in coverage)
fixes = {x['id']: x for x in json.loads((local / 'prepared-pr-fixes.json').read_text())}
full = {x['id']: x for x in json.loads((local / 'prepared-pr-full-checks.json').read_text())}
assert set(full) == {'P13', 'P14'}
for d in ('receipts', 'runners', 'logs', 'screenshots', 'followups'):
    (out / d).mkdir(exist_ok=True)
for name in ('HANDOFF.md', 'REPRODUCE.md'):
    shutil.copyfile(local / name, out / name)
# Explicit allowlist; no environment files, VM disks or SSH keys.
receipts = ['coverage.json', 'builds.json', 'iso-artifact.json', 'iso-package-inputs.json',
 'build-5-iso-artifact.json', 'build-5-iso-package-inputs.json', 'integration-heads.json',
 'merge-resolutions.json', 'current-runtime-payload.json', 'installed-runtime-payload.json',
 'installed-system-inventory.json', 'guest-software-verification.json', 'guest-scenarios.json',
 'acceptance-first-run.json', 'acceptance-ocr-evidence.json', 'factory-reset-baseline-failure.json',
 'audio-header-dependency-repair.json', 'audio-repair-reuse.json', 'guest-harness-adjustments.json',
 'baseline-t2-firmware.json', 'local-runtime-dependency-check.json', 'verified-reuse-check.json',
 'libfprint-recheck.json', 'prepared-pr-fix-checks.json', 'prepared-pr-full-checks.json',
 'final-validation.json']
for name in receipts:
    shutil.copyfile(local / name, out / 'receipts' / name)
for name in ('start-build.sh', 'guest-full-suite.sh', 'guest-mac-desktop.sh', 'guest-suspend-fixtures.sh',
 'guest-t1-desktop.sh', 'guest-session.sh', 'run-guest-lock-check.py', 'run-package-scenario.sh',
 'run-migration-scenario.sh', 'run-nvme-scenario.sh', 'run-t1-desktop-recheck.sh', 'acceptance-ocr-whitespace.patch'):
    shutil.copyfile(local / name, out / 'runners' / name)
for b, prefix, names in [
 (b5, 'build5', ['build.log','acceptance.log','acceptance-2.log','acceptance-ocr-fallback.log',
  'guest-full-suite.log','guest-config-recheck.log','guest-snapper-recheck.log','guest-kitty-parser.log',
  'guest-mac-desktop-unlocked.log','guest-rtc-test.log','guest-suspend-fixtures.log','integration.log']),
 (b6, 'build6', ['build.log','acceptance.log','audio12-retest.log','inspection.log'])]:
    for name in names:
        shutil.copyfile(b / name, out / 'logs' / (prefix + '-' + name))
for name in ('P13-test-all.log', 'P14-test-all.log', 'P13-focused.log', 'P14-focused.log', 'P11-packages-focused.log'):
    shutil.copyfile(wave / 'pr-followups' / name, out / 'logs' / name)
ibase = b5 / 'sources/omarchy-iso/test-runs/omarchy-2026.09.21-intel-mac-local-x86_64-integration/runs'
for row in json.loads((local / 'guest-scenarios.json').read_text()):
    d = ibase / row['run']
    for log in row['logs']:
        if log['name'] in ('serial.log','installed-state.log'): continue
        shutil.copyfile(d / log['name'], out / 'logs' / (row['scope'] + '-' + log['name']))
shutil.copyfile(ibase / '20260920-224728-mac-packages-t1bridge/spi-retirement.log', out / 'logs/P06-spi-retirement.log')
final_run = next((b6 / 'sources/omarchy-iso/test-runs/omarchy-2026.09.21-intel-mac-local-x86_64-integration/runs').glob('*-mac-packages-audio12'))
for name in ('package-install.log','audio-header-regression.log','audio-hook-errors.log','runtime-payload.log','runtime-inventory.log','reboot.log','header-baseline.log'):
    shutil.copyfile(final_run / name, out / 'logs' / ('build6-audio12-' + name))
for p in (b5 / 'mac-desktop-unlocked').glob('*.png'):
    shutil.copyfile(p, out / 'screenshots' / p.name)
for p in (b5 / 'guest-lock-check-2').glob('*.png'):
    shutil.copyfile(p, out / 'screenshots' / ('lock-' + p.name))
for p in (ibase / '20260920-225713-mac-t1-desktop-recheck/t1-desktop-evidence').glob('*.png'):
    shutil.copyfile(p, out / 'screenshots' / ('t1-' + p.name))
final_acceptance = b6 / 'sources/omarchy-iso/test-runs/omarchy-2026.09.21-intel-mac-local-x86_64/runs/20260920-231220'
for name in ('success-acceptance-final.png', 'omarchy-acceptance/success-desktop.png'):
    shutil.copyfile(final_acceptance / name, out / 'screenshots' / ('build6-' + Path(name).name))
for ident, fix in fixes.items():
    patch = subprocess.check_output(['git','diff','--binary',fix['old_head'],fix['prepared_head']],cwd=fix['checkout'])
    (out / 'followups' / (ident + '.patch')).write_bytes(patch)
(out / 'followups/commits.json').write_text(json.dumps(list(fixes.values()),indent=2)+'\n')
text = '# Per-feature VM coverage\n\nThese are results for the combined pinned ISO, not physical hardware certification. Build 5 carries the broad checks; Build 6 repeats installation/acceptance and verifies the only changed package. See [handoff](HANDOFF.md), [final receipt](receipts/final-validation.json), [source reconstruction](integration/sources.json), [logs](logs) and [screenshots](screenshots).\n\n| Feature | Observed VM / fixture evidence | Physical limit |\n| --- | --- | --- |\n'
for row in coverage:
    text += '| '+row['id']+' '+row['scope']+' | '+row['vm_evidence'].replace('|','/')+' | '+row['physical_limit']+' |\n'
text += '\nP14 passes only the stated virtual RTC/fixture checks; three retained defects are confirmed. The baseline factory-reset scenario failed. Neither is erased by the table.\n'
(out / 'COVERAGE.md').write_text(text)
public = 'https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/'
replacements = {
 'P01': [('- [ ] Live Quickshell rendering, IPC timing and actual device events remain untested. Before/after visual captures are still needed.', '- [ ] Real guest keyboard layout changes and EN/DE/EN rendering were verified with screenshots. Physical Apple device identity and hotplug timing still need hardware testing.')],
 'P02': [('- [ ] No real package transaction, wl connection, fallback boot or reboot was tested. Installing headers does not establish a successful DKMS build.', '- [ ] Actual guest package/header repair, dual-kernel DKMS compilation and reboot passed. Physical wl association and hardware fallback boot still need testing.')],
 'P05': [('- [ ] Live rendering, hotplug, dock/undock and before/after visual captures remain unverified.', '- [ ] Guest monitor rendering/reload and preservation of its active virtual output passed with screenshots. Physical hotplug, dock/undock and gmux panels remain unverified.')],
 'P06': [('- [ ] Review a transition before automatic rollout. Encrypted-root input, package hooks, initramfs, Touch Bar/camera/ALS and rollback remain untested.', '- [ ] Review a transition before automatic rollout. Real guest package removal, initramfs generation and repeated migration passed with T1 packages present. Physical encrypted-root input, provider handoff, Touch Bar/camera/ALS and rollback remain untested.')],
 'P13': [('- [ ] The original suite fails on both baseline and candidate at the superseded PTL migration assertion. Later cases in that suite do not run; the 13 supplemental scope assertions do not make the original suite pass.', '- [x] Corrected the stale PTL assertion to check obsolete behavior rather than reject an unrelated reuse of the migration filename. The complete focused migration suite now passes, including later cases. Standalone full-suite failures remain in the linked dated receipt.')],
 'P14': [('complete standalone suspend diagnostics command unchanged.', 'complete standalone suspend diagnostics command, with a follow-up using the required command-presence helper.'),
 ('syntax evidence only, with active-write/recovery limitations disclosed', 'syntax plus virtual RTC/fixture evidence, with active-write/recovery limitations disclosed'),
 ('- [ ] Behavioral verification is absent: bash -n checks syntax only, and no production subcommand ran. The author did not report a complete end-to-end automated diagnose loop.', '- [ ] Installed status/restore and a real 11-second virtual S3/RTC test ran; controlled guest fixtures reproduced the recovery limitations below. A complete physical diagnose/recovery loop remains unverified.'),
 ('- [ ] The full candidate suite also fails bin-style-test.sh: the unchanged source uses command -v rtcwake at line 44 instead of the required Omarchy command helper. This source-specific style failure is separate from the four upstream-control failures; it remains unfixed for the draft.', '- [x] Follow-up uses omarchy-cmd-present for rtcwake; syntax, CLI and bin-style checks pass. Other standalone full-suite failures are retained in the dated receipt.')]
}
audio_old = '- [ ] Prior original-recipe DKMS builds passed on 7.2.3, with qualified download/fakeroot harness adjustments. Target 7.2.5, signed release/ISO delivery, audible sound, capture and rollback remain unverified.'
audio_new = '- [ ] Both audio companions were built into the ISO, installed and compiled with DKMS against 7.2.5-4-omarchy, then rebooted. The 12-inch header-dependency repair passed a fresh final-ISO retest. Signed release delivery, audible sound, capture, speaker safety and physical rollback remain unverified.'
t1_old = '- [ ] Official archive requests returned HTTP 403 in the recorded refresh; cached public archives match pinned hashes. Original-recipe dependency resolution, a new fingerprint-library build and the exact 7.2.5 ABI remain unverified. Prior adapted-recipe builds cannot certify absent guards.'
t1_new = '- [ ] Hash-verified released sources built, including libfprint/fprintd checks; T1 DKMS compiled for 7.2.5-4-omarchy and rebooted. Desktop provider/password fallback passed using the explicitly documented local omarchy-dev dependency adapter. The unchanged stable omarchy>=4.0.1 dependency, physical T1 ABI/provisioning and source guard gaps are not certified by that adapter.'
bodydir = wave / 'pr-followups/bodies';bodydir.mkdir(exist_ok=True)
bodyrecords=[]
prs=json.loads((root/'reviews/publication/published-prs.json').read_text())['prs']
for pr in prs:
    ident=pr['id'];old=json.loads((wave/'pr-update-preflight'/(ident+'.json')).read_text())['body'];body=old
    for a,b in replacements.get(pr['plan_id'],[]):
        assert a in body,(ident,a);body=body.replace(a,b)
    if pr['plan_id']=='P11':
        assert audio_old in body
        body=body.replace(audio_old,audio_new)
        body=body.replace('The package companion contains two unchanged recipes for separate model tracks.', 'The package companion contains two existing recipes for separate model tracks, with the documented VM-observed header-dependency correction for the 12-inch MacBook.')
        body=body.replace('Combine the unchanged omacom/omarchy-pkgs#249 snd-hda-macbookpro-dkms and omacom/omarchy-pkgs#153 macbook12-audio-driver-dkms recipes', 'Combine the existing omacom/omarchy-pkgs#249 snd-hda-macbookpro-dkms and omacom/omarchy-pkgs#153 macbook12-audio-driver-dkms recipes, with the documented VM-observed header-dependency correction for the latter,')
        body=body.replace('Selected unchanged MacBook CS4208 package recipe.', 'Selected MacBook CS4208 recipe, with a VM-observed kernel-header dependency correction in a follow-up commit.')
    if pr['plan_id']=='P12':assert t1_old in body;body=body.replace(t1_old,t1_new)
    if pr['plan_id']=='P04':body=body.replace('Physical lid/display/lock behavior and visual captures remain unverified.','Guest password-lock behavior and visuals passed; physical lid/display/lock behavior remains unverified.')
    start=body.index('## Validation and provenance');end=body.index('## Known gaps and follow-up work',start)
    historical=body[start:end].replace('## Validation and provenance','## Original publication checks (historical)')
    historical=historical.replace('these results belong to the current candidate tree.','these results belong to that original publication tree, before the VM follow-up.')
    body=body[:start]+'<details>\n<summary>Original pre-VM publication checks and provenance</summary>\n\n'+historical+'\n</details>\n\n'+body[end:]
    row=next(x for x in coverage if x['id']==pr['plan_id'])
    section='## ISO / VM validation — 2026-09-21 UTC\n\n'
    section+='Tested as part of the combined 14-feature custom ISO. Fresh encrypted and unencrypted installs booted; the final rebuilt ISO passed all eight desktop acceptance files with the documented test-only OCR correction. The combined live-guest CLI suite and 267 shell files passed, including focused rechecks.\n\n'
    section+='- **This feature:** '+row['vm_evidence']+'\n'
    section+='- **Hardware boundary:** '+row['physical_limit']+' Accepted source gaps below remain.\n'
    section+='- **Overall limits:** the unchanged-baseline shared-ESP factory-reset test failed; the report retains it and the harness interventions. This remains a draft, not release/hardware certification.\n'
    if ident in fixes:
        f=fixes[ident];section+='- **Follow-up commit:** `'+f['prepared_head']+'`; original author commit remains its parent. [Exact follow-up patch]('+public+'followups/'+ident+'.patch).\n'
        if ident in full:section+='- **Standalone follow-up check:** `./test/all` exited '+str(full[ident]['exit'])+'; [full log]('+public+'logs/'+ident+'-test-all.log). Focused changed-area checks passed. This differs from the combined guest result above.\n'
    section+='\n[Results and limits]('+public+'HANDOFF.md) · [Feature coverage]('+public+'COVERAGE.md) · [Exact sources and reproduction]('+public+'REPRODUCE.md) · [Final artifact receipt]('+public+'receipts/final-validation.json).\n\n'
    marker='## Scope and dependencies';assert marker in body;body=body.replace(marker,section+marker,1)
    # Every original source-PR URL must survive, including rejected alternatives.
    refs=set(re.findall(r'https://github.com/[^/\s)]+/[^/\s)]+/pull/\d+',old))
    assert refs<=set(re.findall(r'https://github.com/[^/\s)]+/[^/\s)]+/pull/\d+',body))
    p=bodydir/(ident+'.md');p.write_text(body)
    bodyrecords.append({'id':ident,'repository':pr['repository'],'number':pr['number'],'url':pr['url'],'body_file':str(p),'before_sha256':hashlib.sha256(old.encode()).hexdigest(),'after_sha256':hashlib.sha256(body.encode()).hexdigest(),'original_source_urls_preserved':len(refs),'expected_head':fixes[ident]['prepared_head'] if ident in fixes else pr['commit']})
(local/'prepared-pr-updates.json').write_text(json.dumps(bodyrecords,indent=2)+'\n')
idx=index/'INTEL-MAC-ROLLUPS.md';text=idx.read_text();banner='**ISO / VM follow-up (2026-09-21 UTC):** custom ISOs built and installed; all 14 scopes now have explicit VM/fixture evidence. Read [results and remaining failures](vm-validation/HANDOFF.md), [coverage](vm-validation/COVERAGE.md), and [reproduction](vm-validation/REPRODUCE.md). The baseline factory-reset scenario failed; physical Mac behavior remains unverified. This does not certify release readiness.\n\n'
if banner not in text:text=text.replace('## Feature and package targets',banner+'## Feature and package targets',1)
text=text.replace('Shared installer/manual/lock files require reconciliation in a later optional release branch; there is no claim that all fourteen stack cleanly today.','Shared installer/manual/lock files were reconciled in the recorded local integration source. Its exact merge decisions and source bundles are in the VM handoff; independent feature merges still require review.')
text=text.replace('## Validation status\n\n','## Original publication validation (historical)\n\nThese pre-VM results are retained as historical evidence; the dated VM follow-up above gives the current tested scope.\n\n',1)
idx.write_text(text)
# Hash every published file; bundles are deliberate source-only Git objects.
manifest=[]
for p in sorted(out.rglob('*')):
    if not p.is_file() or p.name=='MANIFEST.json':continue
    data=p.read_bytes()
    if p.suffix not in ('.png','.bundle'):
        for pattern in (rb'apikey_[0-9a-f]{32}',rb'-----BEGIN [A-Z ]*PRIVATE KEY-----',rb'gh[pousr]_[A-Za-z0-9]{30,}'):
            assert not re.search(pattern,data),'Credential pattern found in '+str(p)
    manifest.append({'path':str(p.relative_to(out)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Prepared',len(bodyrecords),'PR bodies and',len(manifest),'public evidence files; no writes to GitHub.')
