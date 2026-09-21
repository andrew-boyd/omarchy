"""Prepare corrected existing-draft bodies locally. Never publish pending validation."""
import json
from pathlib import Path
import re
import hashlib
import runpy
import argparse
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
read = lambda path: json.loads((ROOT / path).read_text())
registry = read('reviews/hardware-test/source-registry.json')
branches = {r['id']: r for r in read('reviews/hardware-test/branch-preparation.json')}
previous = read('.state/vm-install/2026-09-20/remediation/prepared-pr-updates.json')
PUBLIC = 'https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index'
OUT = ROOT / '.state/hardware-test/2026-09-21/bodies'
OUT.mkdir(parents=True, exist_ok=True)
assert len(branches) == len(previous) == 17
records = []
parser = argparse.ArgumentParser()
parser.add_argument('--validated', action='store_true', help='Use the completed fresh-image receipt; default remains pending.')
args = parser.parse_args()
validation = None
if args.validated:
    validation = read('reviews/hardware-test/final-validation.json')
    assert validation['required_checks_satisfied'] and not validation['physical_hardware_tested']
    assert len(validation['required_stage_exits']) == 14
    assert not any(code for name, code in validation['required_stage_exits'].items() if name != 'runtime')
    if validation['required_stage_exits']['runtime']:
        assert validation['runtime_rechecks']['cause_confirmed']
        assert not any(validation['runtime_rechecks']['recheck_exits'].values())
    for name, head in validation['source_commits'].items():
        repo = ROOT / '.state/vm-install/2026-09-20/repos' / name
        assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == head

limits = {
 'P01': 'Shared keyboard UI applies to genuine typing devices across Intel Mac generations. Physical SPI/USB/T2 input remains hardware-owner validation.',
 'P02': 'Repair retained stock-kernel headers separately from P13 kernel policy. Closed predecessor and merged release-backport history remain referenced.',
 'P03': 'Sysfs detection is shared plumbing. Do not interpret recognizing hardware as a claim that its graphics, camera, input or sleep behavior is validated.',
 'P04': 'The accepted code remains the lid-lock component. Lid-open brightness, lock-resume focus, debounce and controller recovery remain explicitly distinct follow-ups; sources reported on MacBook10,1, T1 and T2 systems all remain visible.',
 'P05': 'Output enumeration/recovery preserves real displays. Physical hotplug, Touch Bar identity and other brightness/graphics proposals remain separate work; the VM only exercises virtual outputs.',
 'P06': 'Complete P12 manual firmware/provider setup before retiring legacy SPI. Software guards require replacement packages/native applespi for retained kernels; a package presence check does not prove a working live hardware transition.',
 'P07': 'Preserve the source MacBook8,1 SPI-PIO parameters and administrator configuration. Coordinate package ownership with P06; no new timing or electrical workaround is invented.',
 'P08': 'Use the P08 package companion before installer trials. This is the Broadcom PCIe camera track; USB/iBridge cameras use a different path. Keep the complete MacBookPro13,1 bundle visible as an alternative.',
 'P09': 'Selected NVMe behavior remains a provisional controller/model-specific target. The actual PCI device must be verified; no physical suspend success follows from a VM fixture.',
 'P10': 'Selected calibration remains split between MacBookPro13,3 and MacBookPro14,2/14,3. The recovery hook now uses the existing BCM4350/BCM43602 boundary from omacom/omarchy#7333. T2 recovery, legacy wl/b43 devices, regulatory hinting and other firmware delivery remain explicit alternatives/follow-ups. omacom/omarchy-pkgs#422 is a separate kernel trial and is not silently stacked into this ISO.',
 'P11': 'Preserve separate CS8409, MacBook CS4208 and iMac CS4208 tracks. The two DKMS package tracks conflict on one machine. Source closures do not erase iMac coverage or the MacBookPro13,2 speaker report.',
 'P12': 'T1Bridge remains the accepted T1 provider; setup and hardware handoff remain manual. Its selected 0.1.9 release reports system suspend/resume as not working on its tested machine; that limitation is unresolved here. Shared fingerprint UI is independently useful. EFI-preservation PR omarchy-iso#174 is an integrated-ISO dependency, not code carried by this runtime branch. Preserve an independent firmware backup before a physical disk wipe.',
 'P13': 'The Apple kernel-upgrade exception does not choose every custom kernel. BCM43602 cold resume (omacom/omarchy-pkgs#422) and ACPICA resume latency (omacom/omarchy-pkgs#544) are separately reviewed kernel alternatives, with no automatic adoption.',
 'P14': 'Diagnostics remain an explicit command, not an automatic sleep policy. Inspect device identity and recovery instructions before attended physical trials; never infer universal causes from a single model.'
}

def action(source, decision):
    if source['state'] != 'open':
        return 'Already ' + source['state'] + '; retain evidence and credit. No action requested.'
    if decision['treatment'] == 'included':
        return 'Consider closure only after maintainers accept preserved behavior and hardware coverage.'
    if decision['treatment'] == 'partial':
        return 'Keep uncovered work open; this feature alone does not fully supersede it.'
    if decision['treatment'] == 'alternative':
        return 'Retain for comparison; do not stack competing implementations automatically.'
    if decision['treatment'] == 'superseded':
        return 'Maintainers may assess the named successor before closure.'
    return 'Keep the original as its review/test target; no closure recommendation here.'

for old in previous:
    pid = old['id']
    feature = pid.removesuffix('-packages')
    branch = branches[pid]
    old_text = Path(old['body_file']).read_text()
    intro = old_text.split('## Published series', 1)[0].rstrip()
    if pid == 'P10':
        intro = intro.replace('The selected model/driver policy is unchanged.',
                              'The recovery chip boundary is now narrowed using the existing BCM4350/BCM43602 scope from #7333; T2 alternatives remain separately documented. An older broad hook already installed on a T2 trial is not automatically removed by this fresh-install selection; reconcile that existing hook manually.')
    rows = []
    for source in registry['sources']:
        decision = next((d for d in source['dispositions'] if d['target'] == feature), None)
        if decision:
            rows.append((source, decision))
    text = intro + f'\n\nThis existing draft: [{branch["url"]}]({branch["url"]}).\n\n'
    text += '## Full Intel Mac scope and current revision\n\n'
    text += 'The project covers **all 64-bit Intel Macs: pre-T1, T1 and T2**. MacBookPro13,3 is only the first available physical test machine. Each feature has its own hardware boundary; one model\'s success does not validate the rest.\n\n'
    text += f'Candidate head: `{branch["head"]}`; reconciled upstream: `{branch["base_head"]}`. Published contribution commits and author/co-author metadata remain in the history.\n\n'
    if validation:
        text += f'**Ready for attended physical testing; Mac hardware remains untested by this effort.** The reconciled combined ISO passed fresh unencrypted/encrypted VM installations, desktop/password-lock checks, strict Neovim startup/theme checks, synthetic Apple EFI preservation through a disk wipe, and affected package/DKMS/migration checks. ISO SHA-256: `{validation["sha256"]}`.\n\n'
        text += f'[Exact sources, results, retained failures and reproduction]({PUBLIC}/hardware-test/HANDOFF.md). These results cover the pinned combined image; [standalone-versus-combined differences]({PUBLIC}/hardware-test/receipts/integration-coverage.json) remain explicit. [Full inventory and retained work tracks]({PUBLIC}/hardware-test/INVENTORY.md).\n\n'
    else:
        text += '**Local preparation — refreshed ISO validation pending. Do not publish this prepared body yet.** The previous B7 ISO passed the documented VM install/desktop checks but failed a stricter baseline Neovim startup check. The new local integration source repairs that plugin reference, adds existing Apple EFI-preservation commits and corrects P10 scope. A new build, fresh installs and final artifact verification are still required.\n\n'
        text += f'[Previous dated results]({PUBLIC}/vm-remediation/HANDOFF.md) are historical evidence, not a pass for this new head. [Full inventory and retained work tracks]({PUBLIC}/hardware-test/INVENTORY.md).\n\n'
    text += '## Scope and dependencies\n\n' + limits[feature] + '\n\n'
    text += 'The inventory now records 188 source/context PRs: 101 have dispositions in feature tables and 87 remain only in separate work tracks. **This is not 188 implemented PRs or 188-to-14 compression.** The 14 feature PRs and three package companions remain the published coordination targets; retained backlog is not claimed complete.\n\n'
    text += '## Every affected source PR and recommended action\n\n'
    text += 'Current open/closed/merged state is administrative history, not proof that two patches preserve identical behavior. Included/partial identifies selected contributions; alternatives, deferred work and context are not automatically ISO content.\n\n'
    text += '| Source and author | State | Treatment and rationale | Recommended action |\n| --- | --- | --- | --- |\n'
    for source, decision in rows:
        rationale = decision['rationale']
        rationale = re.sub(r'\bpackage #(\d+)', r'package omacom/omarchy-pkgs#\1', rationale)
        # This package predecessor explicitly credits another package PR.
        if source['source_key'] == 'omacom/omarchy-pkgs#155':
            rationale = rationale.replace('through #249', 'through omacom/omarchy-pkgs#249')
        rationale = re.sub(r'(?<![\w/.-])#(\d+)', lambda m: 'omacom/omarchy#' + m[1], rationale)
        rationale = rationale.replace('|', '\\|').replace('\n', ' ')
        text += f'| [{source["source_key"]}]({source["url"]}) — @{source["author"]} | {source["state"]} | **{decision["treatment"]}**: {rationale} | {action(source, decision)} |\n'
    text += '\n## Validation and attribution\n\n'
    if validation:
        text += 'Required fresh-image checks are satisfied, with qualified reruns. The full source suite passed 273 files with two disclosed skips, but repeated NetworkManager Polkit failures during that suite temporarily locked its test account. The following password/desktop/recovery checks failed there and passed separately in a clean overlay of the same ISO; the original aggregate remains failed. The first build attempt also failed one libfprint USB-emulation test; unchanged-source isolated repeats, two complete suites and normal package checks passed afterward. That intermittent build-test failure remains documented, and its cause is not established. VM fixtures and DKMS builds do not establish physical device behavior. '
    else:
        text += 'The revised Broadcom source checks and nine EFI-preservation unit tests passed in a disposable guest installed from B7. That is source validation, not a fresh-ISO installation pass. '
    text += 'Physical Wi-Fi, audio, camera, Touch Bar, fingerprint, graphics and suspend behavior remain unverified by this effort.\n\n'
    text += f'Original source histories remain linked above. Source-authored commits already included in the roll-ups remain ancestors of this revision; additional copied contributions receive native attribution. [Original attribution mapping]({PUBLIC}/AUTHORSHIP.md). No original PR is edited or closed by this effort.\n'
    path = OUT / (pid + '.md')
    path.write_text(text)
    records.append({'id': pid, 'url': branch['url'], 'body_file': str(path),
                    'body_sha256': hashlib.sha256(text.encode()).hexdigest(),
                    'head_branch': branch['branch'], 'old_head': branch['original_head'],
                    'expected_head': branch['head'], 'source_rows': len(rows), 'publish_ready': bool(validation)})
(HERE / 'prepared-pr-updates.json').write_text(json.dumps(records, indent=2) + '\n')
audit = runpy.run_path(str(HERE / 'verify-inventory.py'))
print(json.dumps(audit['validate_bodies'](registry, records)))
