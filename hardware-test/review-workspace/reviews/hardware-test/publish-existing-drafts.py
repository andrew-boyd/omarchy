#!/usr/bin/env python3
"""Verify, then optionally update only the 17 already-authorized draft PRs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
INDEX = ROOT / '.state/vm-install/2026-09-20/pr-followups/review-index'
GH = '/home/boyd/.local/share/mise/installs/gh/2.101.0/gh_2.101.0_linux_amd64/bin/gh'
p = argparse.ArgumentParser()
p.add_argument('--publish', action='store_true', help='Remote writes; requires complete final validation and prepared evidence.')
args = p.parse_args()
records = json.loads((HERE / 'prepared-pr-updates.json').read_text())
branches = {r['id']: r for r in json.loads((HERE / 'branch-preparation.json').read_text())}
old = {r['id']: r for r in json.loads((ROOT / 'reviews/remediation/published-pr-updates.json').read_text())['prs']}
assert len(records) == len(branches) == len(old) == 17
audit = runpy.run_path(str(HERE / 'verify-inventory.py'))
audit['validate_bodies'](json.loads((HERE / 'source-registry.json').read_text()), records)

def run(*args):
    return subprocess.check_output(list(map(str, args)), text=True).strip()

def git(repo, *args):
    return run('git', '-C', repo, *args)

def api(path):
    return json.loads(run(GH, 'api', path))

def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()

def inspect(row):
    branch = branches[row['id']]
    parts = row['url'].split('/')
    repository, number = '/'.join(parts[3:5]), parts[-1]
    assert repository in {'omacom/omarchy', 'omacom/omarchy-pkgs'}
    live = api(f'repos/{repository}/pulls/{number}')
    assert live['state'] == 'open' and live['draft'] and not live['merged'], row['id']
    assert live['head']['repo']['owner']['login'] == 'andrew-boyd'
    assert live['head']['ref'] == row['head_branch']
    assert live['head']['sha'] in {row['old_head'], row['expected_head']}, (row['id'], 'intervening head')
    assert sha(live['body'] or '') in {old[row['id']]['body_sha256'], row['body_sha256']}, (row['id'], 'intervening body')
    assert live['base']['ref'] == ('master' if row['id'].endswith('-packages') else 'quattro')
    # Later upstream movement must be assessed explicitly; do not silently
    # turn a previously tested base into a claim about a different one.
    # GitHub's PR record can retain the base SHA from an earlier comparison.
    # Read the actual target branch ref rather than treating that stale field
    # as either proof of freshness or a reason to roll back reconciliation.
    target_ref = 'refs/heads/' + live['base']['ref']
    target = run('git', 'ls-remote', 'https://github.com/' + repository + '.git', target_ref).split()
    assert len(target) == 2 and target[1] == target_ref
    assert target[0] == branch['base_head'], (row['id'], 'upstream base moved', target[0])
    assert git(branch['path'], 'rev-parse', 'HEAD') == row['expected_head']
    assert not git(branch['path'], 'status', '--porcelain')
    subprocess.run(['git', '-C', branch['path'], 'merge-base', '--is-ancestor', row['old_head'], row['expected_head']], check=True)
    body = Path(row['body_file']).read_text()
    assert sha(body) == row['body_sha256']
    return row['id'], live

with ThreadPoolExecutor(max_workers=4) as pool:
    live = dict(pool.map(inspect, records))
report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'existing_drafts_checked': len(live),
          'remote_writes': False, 'all_open_drafts': True, 'current_bases_match_prepared': True,
          'bodies_and_heads_unchanged_or_already_expected': True,
          'ready_to_publish': all(r['publish_ready'] for r in records)}
(HERE / 'publication-preflight.json').write_text(json.dumps(report, indent=2) + '\n')
if not args.publish:
    print(json.dumps(report))
    raise SystemExit(0)

assert report['ready_to_publish'], 'Bodies still marked validation pending'
readiness = json.loads((HERE / 'FINAL-READINESS.json').read_text())
assert readiness['all_required_checks_passed'] and readiness['physical_install_ready']
assert readiness['original_source_prs_modified'] is False and readiness['basecamp_or_chat_posted'] is False
assert {r['id']: r['expected_head'] for r in records} == readiness['published_candidate_heads']
assert not git(INDEX, 'status', '--porcelain'), 'Evidence must be committed for review first'
index_head = git(INDEX, 'rev-parse', 'HEAD')
assert index_head == readiness['evidence_commit']
assert (INDEX / 'hardware-test/HANDOFF.md').is_file()
remote = run('git', 'ls-remote', 'https://github.com/andrew-boyd/omarchy.git', 'refs/heads/intel-mac/review-index').split()[0]
subprocess.run(['git', '-C', str(INDEX), 'merge-base', '--is-ancestor', remote, index_head], check=True)
subprocess.run(['git', '-C', str(INDEX), 'push', 'git@github.com:andrew-boyd/omarchy.git', 'HEAD:refs/heads/intel-mac/review-index'], check=True)
assert api('repos/andrew-boyd/omarchy/contents/hardware-test/HANDOFF.md?ref=intel-mac/review-index')['type'] == 'file'

completed = []
for row in records:
    branch = branches[row['id']]
    inspect(row)
    repo_name = 'omarchy-pkgs' if row['id'].endswith('-packages') else 'omarchy'
    # Use the existing authenticated SSH identity. The CLI OAuth token can
    # edit PR bodies but lacks workflow scope for reconciled package history.
    subprocess.run(['git', '-C', branch['path'], 'push', f'git@github.com:andrew-boyd/{repo_name}.git', 'HEAD:refs/heads/' + row['head_branch']], check=True)
    for attempt in range(15):
        _, before = inspect(row)
        if before['head']['sha'] == row['expected_head']:
            break
        time.sleep(2)
    assert before['head']['sha'] == row['expected_head']
    number = row['url'].split('/')[-1]
    if sha(before['body'] or '') != row['body_sha256']:
        subprocess.run([GH, 'pr', 'edit', number, '--repo', 'omacom/' + repo_name,
                        '--body-file', row['body_file']], check=True, capture_output=True)
    _, after = inspect(row)
    assert sha(after['body']) == row['body_sha256'] and after['head']['sha'] == row['expected_head']
    completed.append({'id': row['id'], 'url': row['url'], 'head': after['head']['sha'],
                      'body_sha256': sha(after['body']), 'still_open_draft': True,
                      'verified_at': datetime.now(timezone.utc).isoformat()})
    (HERE / 'published-pr-updates.json').write_text(json.dumps({
        'evidence_commit': index_head, 'completed_count': len(completed), 'expected_count': 17,
        'prs': completed, 'original_source_prs_modified': False, 'basecamp_or_chat_posted': False,
    }, indent=2) + '\n')
    print(row['id'] + ' updated and verified', flush=True)
