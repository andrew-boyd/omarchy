"""Read-only GitHub refresh of the complete known inventory, not a selected subset."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.state/hardware-test/2026-09-21/inventory'
GH = '/home/boyd/.local/share/mise/installs/gh/2.101.0/gh_2.101.0_linux_amd64/bin/gh'
read = lambda path: json.loads((ROOT / path).read_text())
plan = read('reviews/grouped-prs/plan.json')
ledger = read('reviews/rollups/2026-09-19T2227Z-brightness-range/ledger.json')
publication = read('.state/publication/2026-09-20-ready/publication-sources.json')
sources = {}

def add(url, origin, group=None, previous=None):
    row = sources.setdefault(url, {'url': url, 'origins': [], 'groups': [], 'prior_snapshots': []})
    if origin not in row['origins']:
        row['origins'].append(origin)
    if group and group not in row['groups']:
        row['groups'].append(group)
    if previous:
        row['prior_snapshots'].append(previous)

for group in plan['groups']:
    for member in group['members']:
        add(member['url'], 'original-group-inventory', group['group'],
            {key: member.get(key) for key in ['head_sha', 'state']})
for family in ledger['families']:
    for url in family['source_urls']:
        add(url, 'expanded-family-ledger', family['family'])
for source in publication['sources']:
    add(source['url'], 'published-source-table', previous={
        key: source.get(key) for key in ['head_sha', 'state', 'updated_at']})
extra_path = ROOT / 'reviews/hardware-test/additional-sources.json'
if extra_path.exists():
    for source in json.loads(extra_path.read_text()):
        add(source['url'], source['origin'], source['group'])

def api(path, paginate=False):
    args = [GH, 'api', path]
    if paginate:
        args += ['--paginate', '--slurp']
    result = subprocess.run(args, text=True, capture_output=True, check=True)
    data = json.loads(result.stdout)
    return [item for page in data for item in page] if paginate else data

def refresh(row):
    parts = row['url'].split('/')
    repo, number = '/'.join(parts[3:5]), int(parts[-1])
    stem = repo.replace('/', '--') + '--' + str(number)
    path = OUT / (stem + '.json')
    if path.exists():
        value = json.loads(path.read_text())
    else:
        prefix = f'repos/{repo}/pulls/{number}'
        pr = api(prefix)
        value = {**row, 'repository': repo, 'number': number,
                 'checked_at': datetime.now(timezone.utc).isoformat(),
                 'title': pr['title'], 'author': pr['user']['login'],
                 'head_sha': pr['head']['sha'], 'base_sha': pr['base']['sha'],
                 'base_ref': pr['base']['ref'], 'updated_at': pr['updated_at'],
                 'state': 'merged' if pr['merged'] else pr['state'],
                 'body': pr['body'] or '', 'draft': pr['draft'],
                 'files': api(prefix + '/files?per_page=100', True),
                 'comments': api(f'repos/{repo}/issues/{number}/comments?per_page=100', True),
                 'reviews': api(prefix + '/reviews?per_page=100', True),
                 'inline': api(prefix + '/comments?per_page=100', True)}
        # Recheck so discussion and file reads cannot silently straddle a push.
        after = api(prefix)
        if after['head']['sha'] != value['head_sha'] or after['updated_at'] != value['updated_at']:
            raise RuntimeError('PR changed during snapshot: ' + row['url'])
        path.write_text(json.dumps(value, indent=2) + '\n')
    return {**row, **{k: value[k] for k in ['repository', 'number', 'title', 'author',
            'head_sha', 'base_sha', 'base_ref', 'state', 'updated_at', 'checked_at']},
            'snapshot': str(path.relative_to(ROOT)),
            'snapshot_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'changed_from_prior': any(p['head_sha'] != value['head_sha'] or p['state'] != value['state']
                                      for p in row['prior_snapshots'])}

OUT.mkdir(parents=True, exist_ok=True)
results, errors = [], []
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(refresh, row): url for url, row in sources.items()}
    for future in as_completed(futures):
        url = futures[future]
        try:
            results.append(future.result())
        except Exception as error:
            errors.append({'url': url, 'error': str(error)})
        if (len(results) + len(errors)) % 20 == 0:
            print(f'{len(results)} snapshots complete; {len(errors)} errors', flush=True)
report = {'checked_at': datetime.now(timezone.utc).isoformat(),
          'scope': 'Known inventory: all 64-bit Intel Macs; first physical test model does not filter sources.',
          'expected_sources': len(sources), 'sources': sorted(results, key=lambda s: s['url']),
          'errors': errors, 'remote_writes': False,
          'limitations': ['This refresh covers known source PRs; new discovery is a separate gate.',
                         'GitHub file patches may be truncated; full blobs/diffs are required before code selection.']}
(ROOT / 'reviews/hardware-test/inventory-refresh.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'expected': len(sources), 'collected': len(results), 'errors': errors}))
raise SystemExit(bool(errors))
