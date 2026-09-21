"""Advance all existing draft candidates locally, preserving published ancestry."""
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
W = ROOT / '.state/vm-install/2026-09-20'
OUT = ROOT / '.state/hardware-test/2026-09-21/branches'
read = lambda path: json.loads((ROOT / path).read_text())
manifest = read('reviews/publication/packet/manifest.json')
published = {r['id']: r for r in read('reviews/remediation/published-pr-updates.json')['prs']}
previous = {r['id']: Path(r['path']) for r in read('.state/vm-install/2026-09-20/remediation/branch-preparation.json')}
previous['P11-packages'] = W / 'pr-followups/P11-packages'
published_repos = {r['id']: ROOT / r['local_repo'] for r in read('.state/publication/2026-09-20-ready/branches.json')['entries']}
entries = []
receipt = ROOT / 'reviews/hardware-test/branch-preparation.json'
completed = {r['id']: r for r in json.loads(receipt.read_text())} if receipt.exists() else {}

def git(path, *args, check=True):
    result = subprocess.run(['git', '-C', str(path), *args], capture_output=True, text=True)
    if check and result.returncode:
        raise RuntimeError(f'{path}: {args}: {result.stderr} {result.stdout}')
    return result

OUT.mkdir(parents=True, exist_ok=True)
for entry in manifest['entries']:
    pid = entry['id']
    source = previous.get(pid, published_repos[pid])
    original = published[pid]['head']
    git(source, 'cat-file', '-e', original + '^{commit}')
    repo = 'omarchy-pkgs' if pid.endswith('-packages') else 'omarchy'
    base_branch = 'master' if repo == 'omarchy-pkgs' else 'quattro'
    integrated = W / 'repos' / repo
    target = git(integrated, 'rev-parse', 'refs/remotes/hardware-lock/' + base_branch).stdout.strip()
    path = OUT / pid
    if path.exists():
        if pid in completed:
            assert git(path, 'rev-parse', 'HEAD').stdout.strip() == completed[pid]['head']
            assert not git(path, 'status', '--porcelain').stdout
            entries.append(completed[pid])
            continue
        assert git(path, 'rev-parse', 'HEAD').stdout.strip() == original
        assert git(path, 'rev-parse', 'MERGE_HEAD').stdout.strip() == target
        merged = subprocess.CompletedProcess([], 0, '', '')
    else:
        git(source, 'worktree', 'add', '--detach', str(path), original)
        git(path, 'fetch', '--no-tags', str(integrated), 'refs/remotes/hardware-lock/' + base_branch)
        merged = git(path, 'merge', '--no-ff', '--no-commit', target, check=False)
    conflicts = git(path, 'diff', '--name-only', '--diff-filter=U').stdout.splitlines()
    if merged.returncode or conflicts:
        allowed = {'test/shell.d/locate-test.sh', 'test/shell.d/omarchy-kernel-migration-test.sh'}
        reported = re.findall(r'CONFLICT \(content\): Merge conflict in (.+)', merged.stdout)
        assert (conflicts or reported) and set(conflicts + reported) <= allowed, (pid, merged.stderr, merged.stdout)
        for name in conflicts:
            f = path / name
            data, count = re.subn(r'^<<<<<<< HEAD\n.*?^=======\n^>>>>>>> [^\n]+\n', '', f.read_text(), flags=re.M | re.S)
            assert count == 1, (pid, name, count)
            f.write_text(data)
            git(path, 'add', name)
    git(path, 'diff', '--cached', '--check')
    git(path, 'commit', '-m', 'Merge current ' + base_branch + ' into ' + pid)
    if pid == 'P10':
        git(path, 'fetch', '--no-tags', str(integrated), 'HEAD')
        git(path, 'cherry-pick', '-x', '6096d649')
    head = git(path, 'rev-parse', 'HEAD').stdout.strip()
    git(path, 'merge-base', '--is-ancestor', original, head)
    git(path, 'merge-base', '--is-ancestor', target, head)
    assert not git(path, 'status', '--porcelain').stdout, pid
    entries.append({'id': pid, 'repository': entry['repository'], 'url': entry['pr_url'],
                    'branch': entry['branch'], 'path': str(path), 'original_head': original,
                    'base_head': target, 'head': head, 'resolved_test_conflicts': conflicts,
                    'published_history_preserved': True, 'vm_checks_pending': True})
    (ROOT / 'reviews/hardware-test/branch-preparation.json').write_text(json.dumps(entries, indent=2) + '\n')
    print(pid, head, flush=True)
