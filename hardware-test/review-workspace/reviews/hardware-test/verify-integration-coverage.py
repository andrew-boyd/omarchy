#!/usr/bin/env python3
"""Compare every feature-owned production path against the combined source."""
import difflib
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
repos = ROOT / '.state/vm-install/2026-09-20/repos'
branches = json.loads((HERE / 'branch-preparation.json').read_text())
exceptions = {
    ('P06', 'install/hardware/apple/fix-spi-keyboard.sh'): 'Combined source also incorporates P07 model-specific PIO, anchored gating and configuration preservation. Standalone P06 retains its source installer behavior; combined tests do not prove that differing file independently.',
    ('P07', 'install/hardware/apple/fix-spi-keyboard.sh'): 'Standalone P07 retains the legacy SPI package; the combined candidate removes that package through P06 and retains P07 module/PIO configuration.',
    ('P12-packages', 'pkgbuilds/t1bridge-omarchy/PKGBUILD'): 'Published companion retains stable omarchy>=4.0.1. The combined build explicitly substitutes the exact local omarchy-dev dependency and local pkgrel when the builder opts in.',
}
for pid in ['P06', 'P08', 'P11']:
    exceptions[pid, 'install/omarchy-other.packages'] = 'Combined optional-package list merges P06 legacy SPI retirement, P08 FaceTime packages and P11 MacBook audio packages. Hardware selection remains in the individual installer leaves.'
for pid in ['P08', 'P10', 'P11']:
    exceptions[pid, 'install/hardware/all.sh'] = 'Combined installer invokes all three selected camera, Broadcom and audio feature leaves; the standalone branch adds only its own feature wiring.'

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

def sha(data):
    return hashlib.sha256(data).hexdigest()

rows = []
seen_exceptions = set()
heads = {}
for branch in branches:
    pid = branch['id']
    repo_name = 'omarchy-pkgs' if pid.endswith('-packages') else 'omarchy'
    combined = repos / repo_name
    feature = Path(branch['path'])
    assert git(feature, 'rev-parse', 'HEAD').decode().strip() == branch['head']
    assert not git(feature, 'status', '--porcelain').strip()
    assert not git(combined, 'status', '--porcelain').strip()
    heads[repo_name] = git(combined, 'rev-parse', 'HEAD').decode().strip()
    for ancestor in [branch['original_head'], branch['base_head']]:
        subprocess.run(['git', '-C', str(feature), 'merge-base', '--is-ancestor', ancestor, branch['head']], check=True)
    paths = git(feature, 'diff', '--name-only', branch['base_head'], 'HEAD').decode().splitlines()
    for path in paths:
        if not path.startswith(('bin/', 'default/', 'install/', 'migrations/', 'shell/', 'lib/', 'pkgbuilds/')):
            continue
        assert (feature / path).is_file() and (combined / path).is_file(), (pid, path, 'unsupported missing/deleted path')
        left, right = (feature / path).read_bytes(), (combined / path).read_bytes()
        same = left == right
        if not same:
            assert (pid, path) in exceptions, ('Unexplained integration difference', pid, path)
            seen_exceptions.add((pid, path))
        rows.append({'id': pid, 'feature_head': branch['head'], 'path': path,
                     'same_production_bytes': same, 'feature_sha256': sha(left), 'combined_sha256': sha(right),
                     'reason': None if same else exceptions[pid, path],
                     'diff': '' if same else ''.join(difflib.unified_diff(left.decode().splitlines(True), right.decode().splitlines(True), fromfile=pid + '/' + path, tofile='combined/' + path))})
assert seen_exceptions == set(exceptions), {'unused_exception': sorted(set(exceptions) - seen_exceptions)}
report = {'combined_heads': heads, 'feature_branch_count': len(branches),
          'production_path_comparisons': len(rows), 'byte_identical_comparisons': sum(r['same_production_bytes'] for r in rows),
          'explained_differences': len(seen_exceptions), 'unexplained_differences': 0,
          'published_history_and_reconciled_base_preserved': True,
          'qualification': 'Source comparison, not a test pass. Combined VM results establish behavior only for the exact combined source. Differing standalone files retain their separate validation requirements.',
          'files': rows}
(HERE / 'integration-coverage.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k not in ['files', 'combined_heads']}))
