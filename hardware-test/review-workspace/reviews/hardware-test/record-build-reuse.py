#!/usr/bin/env python3
"""Record verified artifacts after the failed ISO build and unchanged-source recheck."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
WAVE = ROOT / '.state/vm-install/2026-09-20'
build = Path(sys.argv[1]).resolve()
evidence = build / 'libfprint-recheck'
assert (build / 'build.exit').read_text().strip() == '1'
assert (evidence / 'recheck.exit').read_text().strip() == '0'

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def run(*args):
    return subprocess.check_output(list(map(str, args)), text=True)

results = {}
for name, count in [('original-testlog', 131), ('isolated-recheck', 3),
                    ('full-serial-recheck', 262), ('testlog', 131)]:
    path = evidence / (name + '.json')
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    assert len(rows) == count, (name, len(rows))
    counts = dict(Counter(row['result'] for row in rows))
    if name == 'original-testlog':
        assert counts == {'OK': 130, 'FAIL': 1}, counts
        assert [row['name'] for row in rows if row['result'] != 'OK'] == ['drivers+custom - libfprint:egis_etu905']
    else:
        assert counts == {'OK': count}, (name, counts)
    results[name] = {'counts': counts, 'log_sha256': sha(path)}

cache = WAVE / 'cache/companions/libfprint-t1bridge'
recipe = build / 'sources/omarchy-pkgs/pkgbuilds/libfprint-t1bridge'
for source in recipe.iterdir():
    if source.is_file():
        assert sha(source) == sha(cache / source.name), source
log = (build / 'build.log').read_text()
assert 'failed companion builds: libfprint-t1bridge' in log
mirror = WAVE / 'cache/iso/airootfs/var/cache/omarchy/mirror/offline'
lib_artifacts = list(cache.glob('libfprint-t1bridge-*.pkg.tar.zst'))
assert len(lib_artifacts) == 1
artifact = lib_artifacts[0]
assert sha(artifact) in (evidence / 'package.sha256').read_text()
subprocess.run(['sudo', '-n', 'install', '-m', '0644', str(artifact), str(mirror / artifact.name)], check=True)
start = datetime.strptime(build.name.split('-')[1], '%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc).timestamp()
names = ['omarchy-dev', 'omarchy-settings-dev', 'omarchy-nvim']
names += (build / 'sources/omarchy-iso/builder/intel-mac.packages').read_text().splitlines()
names = [n for n in names if n and not n.startswith('#')]
assert len(names) == 13
packages = {}
for name in names:
    matches = []
    for path in mirror.glob(name + '-*.pkg.tar.zst'):
        actual, version = run('pacman', '-Qp', path).strip().split(' ', 1)
        if actual != name:
            continue
        metadata = run('bsdtar', '-xOf', path, '.PKGINFO')
        date = int(re.search(r'^builddate = (\d+)$', metadata, re.M)[1])
        assert date >= start, (name, 'stale build date')
        if name != 'libfprint-t1bridge':
            assert 'Finished making: ' + name + ' ' + version + ' (' in log
        matches.append({'filename': path.name, 'sha256': sha(path), 'version': version,
                        'builddate': date})
    assert len(matches) == 1, (name, matches)
    packages[name] = matches
receipt = {'recorded_at': datetime.now(timezone.utc).isoformat(),
           'origin_build': str(build), 'origin_build_exit': 1,
           'input_commits': {name: (build / (name + '.commit')).read_text().strip()
                             for name in ['omarchy', 'omarchy-pkgs']},
           'packages': packages, 'libfprint_recheck': results,
           'reuse_basis': 'Twelve packages completed in the failed ISO attempt; libfprint completed a separate unchanged-source build with all checks after isolated and full-suite repeats. Exact source commits and archive hashes are required for reuse. No failed build is relabeled successful.',
           'libfprint_limitation': 'The original USB replay failure occurred with serial tests too. Reruns establish intermittence, not its cause or a hardware pass. No test, timeout or driver was changed or skipped.'}
target = WAVE / 'cache/companions/verified-reuse.json'
shutil.copy2(target, evidence / 'prior-verified-reuse.json')
target.write_text(json.dumps(receipt, indent=2) + '\n')
(ROOT / 'reviews/hardware-test/build-reuse.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'packages': len(packages), 'libfprint_results': results}))
