#!/usr/bin/env python3
"""Verify the final ISO itself against build receipts and pinned source."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser()
p.add_argument('iso', type=Path)
args = p.parse_args()
iso = args.iso.resolve()
b = iso.parent
out = b / 'verification'
out.mkdir(exist_ok=True)
assert (b / 'build.exit').read_text().strip() == '0'
unsquashfs = ROOT / '.state/vm-install/2026-09-20/remediation/tools/usr/bin/unsquashfs'

def run(*argv):
    return subprocess.check_output(list(map(str, argv)))

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def extract_sfs(path):
    return run(unsquashfs, '-cat', sfs, path)

sfs = out / 'airootfs.sfs'
if not sfs.exists():
    temporary = out / 'airootfs.sfs.partial'
    with temporary.open('wb') as stream:
        subprocess.run(['bsdtar', '-xOf', str(iso), 'arch/x86_64/airootfs.sfs'], stdout=stream, check=True)
    assert temporary.stat().st_size > 1_000_000_000
    temporary.rename(sfs)

# Receipts must be identical inside the ISO; a correct external receipt alone
# cannot establish what the shipped filesystem contains.
for name in ['package-sha256sums', 'local-packages']:
    assert extract_sfs('usr/share/omarchy-iso/' + name) == (b / name).read_bytes(), name
expected = {name: sha for sha, name in
            (line.split(maxsplit=1) for line in (b / 'package-sha256sums').read_text().splitlines())}
local_names = set((b / 'local-packages').read_text().splitlines())
assert {'omarchy-dev', 'omarchy-settings-dev', 'omarchy-nvim'} <= local_names
selected = {name: sha for name, sha in expected.items() if name.rsplit('-', 3)[0] in local_names}
assert len(selected) == len(local_names), 'Missing/duplicate local package archives'
rows = []
for filename, expected_sha in selected.items():
    assert '/' not in filename and filename.endswith('.pkg.tar.zst'), filename
    archive = out / filename
    with archive.open('wb') as stream:
        subprocess.run([str(unsquashfs), '-cat', str(sfs), 'var/cache/omarchy/mirror/offline/' + filename],
                       stdout=stream, check=True)
    actual = digest(archive)
    assert actual == expected_sha, filename
    name, version = run('pacman', '-Qp', archive).decode().strip().split(' ', 1)
    assert name in local_names
    rows.append({'name': name, 'version': version, 'filename': filename, 'sha256': actual,
                 'embedded_matches_receipt': True})
assert {r['name'] for r in rows} == local_names
archives = {r['name']: out / r['filename'] for r in rows}
upstream = json.loads((ROOT / 'reviews/hardware-test/upstream-check.json').read_text())
# Include reconciled upstream changes as well as feature contributions. Using
# the new upstream head here would omit the very OWE/desktop changes we merged.
base = next(r['previous_base'] for r in upstream['repositories'] if r['repository'] == 'omacom/omarchy')
repo = b / 'sources/omarchy'
paths = run('git', '-C', repo, 'diff', '--name-only', '--diff-filter=ACM', base, 'HEAD').decode().splitlines()
payload = []
for rel in paths:
    if not rel.startswith(('bin/', 'config/', 'default/', 'install/', 'migrations/', 'shell/', 'themes/')):
        continue
    settings_owned = rel.startswith(('config/', 'default/')) or rel in {'bin/omarchy-debug', 'bin/omarchy-debug-idle', 'bin/omarchy-upload-log'}
    archive = archives['omarchy-settings-dev' if settings_owned else 'omarchy-dev']
    package_path = 'usr/' + rel if rel.startswith('bin/') else 'usr/share/omarchy/' + rel
    data = run('bsdtar', '-xOf', archive, package_path)
    sha = hashlib.sha256(data).hexdigest()
    assert sha == digest(repo / rel), rel
    listing = run('bsdtar', '-tvf', archive, package_path).decode().split()
    assert listing[2:4] == ['root', 'root'] and listing[0][7] == 'r', (rel, listing)
    if rel.startswith('bin/'):
        assert listing[0][9] == 'x', (rel, listing)
    payload.append({'source': rel, 'path': '/' + package_path, 'sha256': sha,
                    'package_mode': listing[0], 'root_owned': True})
assert len(payload) > 45

efi = []
for rel in ['orchestrator/apple_efi.py', 'orchestrator/phases_impl.py']:
    installed = 'usr/share/omarchy-iso/' + rel
    source = b / 'sources/omarchy-iso/configs/airootfs' / installed
    sha = hashlib.sha256(extract_sfs(installed)).hexdigest()
    assert sha == digest(source), installed
    efi.append({'path': '/' + installed, 'sha256': sha})
nvim_archive = archives['omarchy-nvim']
for installed in ['usr/share/omarchy-nvim/config/lua/plugins/all-themes.lua',
                  'etc/skel/.config/nvim/lua/plugins/all-themes.lua']:
    data = run('bsdtar', '-xOf', nvim_archive, installed)
    assert data == (b / 'sources/omarchy-pkgs/pkgbuilds/omarchy-nvim/lua/plugins/all-themes.lua').read_bytes()
    assert b'gthelding/monokai-pro.nvim' not in data and b'loctvl842/monokai-pro.nvim' in data
lock = json.loads(run('bsdtar', '-xOf', nvim_archive, 'etc/skel/.config/nvim/lazy-lock.json'))
assert lock['monokai-pro.nvim']['commit'] == 'a68e38b8e55d69a215d0f02598900a79c356da9d'

# These upstream dependencies changed alongside the reconciled lock lifecycle.
# Record exact resolved versions; the guest checks verify installed behavior.
dependency_files = {name: [f for f in expected if f.rsplit('-', 3)[0] == name]
                    for name in ['owe', 'owe-lockfeed', 'omasnap']}
assert all(len(files) == 1 for files in dependency_files.values()), dependency_files
(b / 'installed-runtime-payload.json').write_text(json.dumps(payload, indent=2) + '\n')
receipt = {'iso': iso.name, 'bytes': iso.stat().st_size, 'sha256': digest(iso), 'build_exit': 0,
           'source_commits': {n: (b / (n + '.commit')).read_text().strip()
                              for n in ['omarchy', 'omarchy-pkgs', 'omarchy-iso']},
           'runtime_comparison_base': base, 'embedded_packages': rows,
           'changed_runtime_files': payload, 'embedded_efi_sources': efi,
           'neovim_plugin_commit': lock['monokai-pro.nvim']['commit'],
           'upstream_dependency_archives': dependency_files}
(out / 'artifact.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'iso_sha256': receipt['sha256'], 'packages': len(rows),
                  'changed_runtime_files': len(payload), 'efi_source_files': len(efi)}))
