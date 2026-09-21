#!/usr/bin/env python3
"""Stage and independently reconstruct the pinned build sources; no remote writes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser()
p.add_argument('build', type=Path)
args = p.parse_args()
build = args.build.resolve()
out = ROOT / '.state/vm-install/2026-09-20/pr-followups/review-index/hardware-test/integration'
out.mkdir(parents=True, exist_ok=True)
bases = json.loads((ROOT / 'reviews/hardware-test/prebuild-upstream-check.json').read_text())['heads']

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.PIPE)

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

rows = []
for name, branch in [('omarchy', 'quattro'), ('omarchy-pkgs', 'master'), ('omarchy-iso', 'quattro')]:
    repo = build / 'sources' / name
    head = (build / (name + '.commit')).read_text().strip()
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == head
    base = bases['omacom/' + name + ':' + branch]
    tree = git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip()
    bundle, patch = out / (name + '.bundle'), out / (name + '.patch')
    git(repo, 'bundle', 'create', str(bundle), 'HEAD', '^' + base)
    patch.write_bytes(git(repo, 'diff', '--binary', base, head))
    with tempfile.TemporaryDirectory(prefix='vintage-source-verify-') as temporary:
        target = Path(temporary)
        git(target, 'init', '--quiet')
        # The pinned ISO checkout has explicit shallow boundaries. Accept its
        # existing base boundary and connect that base before bundle verify.
        git(target, 'fetch', '--quiet', '--no-tags', '--update-shallow', str(repo), base)
        git(target, 'checkout', '--quiet', '--detach', base)
        git(target, 'bundle', 'verify', str(bundle))
        git(target, 'fetch', '--quiet', str(bundle), 'HEAD')
        assert git(target, 'rev-parse', 'FETCH_HEAD').decode().strip() == head
        assert git(target, 'rev-parse', 'FETCH_HEAD^{tree}').decode().strip() == tree
        git(target, 'checkout', '--quiet', '--detach', base)
        git(target, 'apply', '--index', str(patch))
        assert git(target, 'write-tree').decode().strip() == tree
    rows.append({'repository': 'omacom/' + name, 'base': base, 'build_commit': head,
                 'tree': tree, 'bundle': bundle.name, 'bundle_sha256': digest(bundle),
                 'bundle_fresh_base_checkout_verified': True,
                 'patch': patch.name, 'patch_sha256': digest(patch), 'patch_reconstruction_verified': True,
                 'build_validation': 'pending; reconstruction verification is not an ISO/VM pass'})
    print(name + ': bundle and patch reconstruct the pinned source tree', flush=True)
(out / 'sources.json').write_text(json.dumps(rows, indent=2) + '\n')
(ROOT / 'reviews/hardware-test/source-reconstruction.json').write_text(json.dumps(rows, indent=2) + '\n')
