#!/usr/bin/env python3
"""Read fresh PR metadata for every registered source; never mutate a PR or snapshot."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
GH = '/home/boyd/.local/share/mise/installs/gh/2.101.0/gh_2.101.0_linux_amd64/bin/gh'
sources = json.loads((HERE / 'source-registry.json').read_text())['sources']

def inspect(source):
    path = f'repos/{source["repository"]}/pulls/{source["number"]}'
    live = json.loads(subprocess.check_output([GH, 'api', path], text=True))
    current = {'head_sha': live['head']['sha'], 'state': 'merged' if live['merged'] else live['state'],
               'updated_at': live['updated_at']}
    previous = {key: source[key] for key in current}
    if current != previous:
        return {'source_key': source['source_key'], 'url': source['url'],
                'previous': previous, 'current': current}

with ThreadPoolExecutor(max_workers=6) as pool:
    changes = [row for row in pool.map(inspect, sources) if row]
report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'sources_checked': len(sources),
          'changed': changes, 'unchanged': len(sources) - len(changes),
          'method': 'Fresh authenticated REST PR metadata for every registered source; no cached response reuse; no remote writes.'}
(HERE / 'prepublication-source-delta.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
sys.exit(bool(changes))
