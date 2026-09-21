#!/usr/bin/env python3
"""Stage an allowlisted public packet only after the required fresh-image gates pass."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
build = Path(sys.argv[1]).resolve()
out = ROOT / '.state/vm-install/2026-09-20/pr-followups/review-index/hardware-test'
validation = build / 'hardware-validation'
stages = ['inventory', 'source-integration', 'artifact', 'efi-fresh-install', 'runtime',
          'unencrypted-acceptance', 'encrypted-acceptance', 'packages-camera',
          'packages-audio12', 'packages-audio-pro', 'packages-t1bridge',
          'migration-spi-pio', 'migration-kernel-headers', 'nvme-nonmatching']
assert (build / 'build.exit').read_text().strip() == '0'
raw_exits = {name: int((validation / (name + '.exit')).read_text()) for name in stages}
assert all(code == 0 for name, code in raw_exits.items() if name != 'runtime'), raw_exits
assert raw_exits['runtime'] in {0, 1}
assert int((validation / 'validation.exit').read_text()) == int(any(raw_exits.values()))
artifact = json.loads((build / 'verification/artifact.json').read_text())
assert len(artifact['embedded_packages']) == 13
rechecks = None
if raw_exits['runtime']:
    rechecks = json.loads((HERE / 'runtime-rechecks.json').read_text())
    assert rechecks['cause_confirmed'] and not rechecks['production_changes']
    assert rechecks['iso_sha256'] == artifact['sha256']
    original, repeated = [ROOT / rechecks[key] for key in ['original_run', 'recheck_run']]
    failed = {p.stem for p in original.glob('*.exit')
              if p.stem != 'scenario' and p.read_text().strip() != '0'}
    assert failed == set(rechecks['original_failed_checks']) == {'password-lock', 'desktop', 'recovery'}
    assert (original / 'test-all.exit').read_text().strip() == '0'
    assert all((repeated / (name + '.exit')).read_text().strip() == '0' for name in failed)
    assert (repeated / 'scenario.exit').read_text().strip() == '0'

def copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    destination.chmod(0o644)

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

# Keep independent input provenance and the coverage verifier executable from
# this review workspace, without requiring the original machine-local cache.
workspace = out / 'review-workspace'
for source in HERE.rglob('*'):
    if source.is_file() and '__pycache__' not in source.parts and source.suffix in {'.py', '.sh', '.md', '.json', '.patch', '.txt'}:
        copy(source, workspace / source.relative_to(ROOT))
for rel in ['reviews/grouped-prs/plan.json',
            'reviews/rollups/2026-09-19T2227Z-brightness-range/ledger.json']:
    copy(ROOT / rel, workspace / rel)
helpers = ['guest-session.sh', 'guest-full-suite.sh', 'guest-mac-desktop.sh',
           'guest-t1-desktop.sh', 'run-guest-lock-check.py', 'run-package-scenario.sh',
           'run-migration-scenario.sh', 'run-nvme-scenario.sh',
           'acceptance-ocr-whitespace.patch', 'start-build.sh']
for name in helpers:
    rel = Path('reviews/vm-install') / name
    copy(ROOT / rel, workspace / rel)
rel = Path('reviews/remediation/guest-runtime-recovery.sh')
copy(ROOT / rel, workspace / rel)
records = json.loads((HERE / 'prepared-pr-updates.json').read_text())
for row in records:
    source = Path(row['body_file'])
    copy(source, workspace / 'bodies' / source.name)
    row['body_file'] = 'bodies/' + source.name
(workspace / 'reviews/hardware-test/prepared-pr-updates.json').write_text(json.dumps(records, indent=2) + '\n')
for name in ['HANDOFF.md', 'AUDIT.md', 'INVENTORY.md', 'HARDWARE-MATRIX.md', 'HARDWARE-INSTALL.md', 'companion-download.json']:
    copy(HERE / name, out / name)
copy(HERE / 'PUBLIC-REPRODUCE.md', out / 'REPRODUCE.md')
for source in (HERE / 'provider-docs').rglob('*'):
    if source.is_file():
        copy(source, out / source.relative_to(HERE))
for name in ['artifact.json']:
    copy(build / 'verification' / name, out / 'receipts' / name)
for source in HERE.glob('*.json'):
    copy(source, out / 'receipts' / source.name)
for source in validation.iterdir():
    if source.is_file() and source.suffix in {'.log', '.exit', '.json'}:
        copy(source, out / 'stages' / source.name)
for name in ['build.log', 'build.exit', 'package-sha256sums', 'local-packages']:
    copy(build / name, out / 'build' / name)

failed = Path(json.loads((HERE / 'build-reuse.json').read_text())['origin_build'])
copy(failed / 'build.log', out / 'build/first-attempt-failed.log')
copy(failed / 'build.exit', out / 'build/first-attempt-failed.exit')
for name in ['recheck.log', 'recheck.exit', 'container-packages.txt', 'package.sha256']:
    copy(failed / 'libfprint-recheck' / name, out / 'build/libfprint-recheck' / name)

runs = build / 'sources/omarchy-iso/test-runs'
copied = []
for source in runs.rglob('*'):
    if not source.is_file() or source.is_symlink():
        continue
    # Never include disks, firmware/OVMF, cidata or SSH key material.
    relative = source.relative_to(runs)
    if 'runs' not in relative.parts or any(part in {'packages', 'cidata'} for part in relative.parts):
        continue
    if source.suffix not in {'.log', '.exit', '.txt', '.json', '.sha256', '.png'}:
        continue
    copy(source, out / 'vm-runs' / relative)
    copied.append(str(relative))

result = {'recorded_at': datetime.now(timezone.utc).isoformat(),
          'build': str(build.relative_to(ROOT)), 'artifact': artifact['iso'],
          'sha256': artifact['sha256'], 'source_commits': artifact['source_commits'],
          'required_stage_exits': raw_exits,
          'required_checks_satisfied': True, 'runtime_rechecks': rechecks,
          'qualification': 'Original aggregate/stage failures remain failures. The three installed checks affected by a confirmed suite-time PAM lockout have separate clean-overlay passes; no production change was made.',
          'physical_hardware_tested': False,
          'prior_failed_build_preserved': True, 'vm_evidence_files': copied}
(out / 'receipts/results.json').write_text(json.dumps(result, indent=2) + '\n')
(HERE / 'final-validation.json').write_text(json.dumps(result, indent=2) + '\n')
copy(HERE / 'final-validation.json', out / 'receipts/final-validation.json')
copy(HERE / 'final-validation.json', workspace / 'reviews/hardware-test/final-validation.json')
copy(HERE / 'source-reconstruction.json', out / 'integration/sources.json')
print(json.dumps({'public_directory': str(out), 'stages': len(stages), 'vm_evidence_files': len(copied)}))
