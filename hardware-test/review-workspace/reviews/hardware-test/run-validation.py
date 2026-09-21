#!/usr/bin/env python3
"""Run the prepared fresh-image checks; never publish or install host packages."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('build', type=Path)
args = p.parse_args()
build = args.build.resolve()
assert (build / 'build.exit').read_text().strip() == '0'
isos = [path for path in build.glob('omarchy-*-x86_64.iso') if 'intel-mac-local' not in path.name]
assert len(isos) == 1, isos
iso = isos[0]
local_iso = iso.with_name(iso.name.replace('-x86_64.iso', '-intel-mac-local-x86_64.iso'))
if not local_iso.exists():
    local_iso.hardlink_to(iso)
assert local_iso.samefile(iso) and not local_iso.is_symlink()
out = build / 'hardware-validation'
out.mkdir(exist_ok=True)
assert not (out / 'validation.exit').exists(), 'Use a new named recheck; preserve completed runs.'
status = 0

def stage(name, command, critical=False):
    global status
    assert not (out / (name + '.exit')).exists(), 'Do not overwrite a prior stage: ' + name
    print('Starting ' + name, flush=True)
    with (out / (name + '.log')).open('w') as log:
        result = subprocess.run(list(map(str, command)), stdout=log, stderr=subprocess.STDOUT)
    (out / (name + '.exit')).write_text(str(result.returncode) + '\n')
    print(f'{name}: exit {result.returncode}', flush=True)
    if result.returncode:
        status = 1
        if critical:
            (out / 'validation.exit').write_text('1\n')
            sys.exit(result.returncode)

stage('inventory', [sys.executable, HERE / 'verify-inventory.py', '--prepared-prs', HERE / 'prepared-pr-updates.json'], critical=True)
stage('source-integration', [sys.executable, HERE / 'verify-integration-coverage.py'], critical=True)
stage('artifact', [sys.executable, HERE / 'inspect-artifact.py', local_iso], critical=True)
test_sync = build / 'test-sync'
test_sync.mkdir(exist_ok=True)
assert not (test_sync / 'test').exists(), 'Prepare test-sync once, preserving exact inputs.'
shutil.copytree(build / 'sources/omarchy/test', test_sync / 'test')
ocr_patch = ROOT / 'reviews/vm-install/acceptance-ocr-whitespace.patch'
subprocess.run(['git', '-C', str(test_sync), 'apply', '--check', str(ocr_patch)], check=True)
subprocess.run(['git', '-C', str(test_sync), 'apply', str(ocr_patch)], check=True)
(out / 'test-harness.json').write_text(json.dumps({
    'iso_harness_commit': (build / 'omarchy-iso.commit').read_text().strip(),
    'omarchy_tests_commit': (build / 'omarchy.commit').read_text().strip(),
    'test_only_ocr_patch_sha256': hashlib.sha256(ocr_patch.read_bytes()).hexdigest(),
    'dependency_preflight': 'The host omarchy-pkg-add function is replaced only for this harness invocation with pacman -Q. Missing dependencies fail rather than installing or changing host packages.',
    'product_injection': False,
}, indent=2) + '\n')
seed = json.loads((HERE / 'efi-seed.json').read_text())
stage('efi-fresh-install', ['bash', HERE / 'run-efi-install.sh', local_iso,
                          ROOT / seed['seed'], ROOT / seed['manifest']], critical=True)
stage('runtime', ['bash', HERE / 'run-runtime-checks.sh', local_iso])
harness = build / 'sources/omarchy-iso/bin/omarchy-iso-test'
check_only = 'omarchy-pkg-add() { /usr/bin/pacman -Q "$@" >/dev/null; }; export -f omarchy-pkg-add; exec bash "$@"'
for name, extra in [('unencrypted-acceptance', []), ('encrypted-acceptance', ['--encrypt'])]:
    stage(name, ['bash', '-c', check_only, 'dependency-check-only', harness, local_iso,
                 *extra, '--sync-omarchy', test_sync, '--memory', '4096', '--no-preview'])
for scenario in ['camera', 'audio12', 'audio-pro', 't1bridge']:
    stage('packages-' + scenario, ['bash', ROOT / 'reviews/vm-install/run-package-scenario.sh',
                                  local_iso, scenario])
for scenario in ['spi-pio', 'kernel-headers']:
    stage('migration-' + scenario, ['bash', ROOT / 'reviews/vm-install/run-migration-scenario.sh',
                                   local_iso, scenario])
stage('nvme-nonmatching', ['bash', ROOT / 'reviews/vm-install/run-nvme-scenario.sh', local_iso])
(out / 'validation.exit').write_text(str(status) + '\n')
print('Validation finished: ' + str(out), flush=True)
sys.exit(status)
