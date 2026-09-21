"""Verify independent inventory coverage before any existing draft is updated."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def validate_registry(registry):
    plan = json.loads((ROOT / 'reviews/grouped-prs/plan.json').read_text())
    ledger = json.loads((ROOT / 'reviews/rollups/2026-09-19T2227Z-brightness-range/ledger.json').read_text())
    publication = json.loads((ROOT / 'reviews/hardware-test/inputs/publication-source-index.json').read_text())
    intake = json.loads((ROOT / 'reviews/hardware-test/additional-sources.json').read_text())
    expected = {m['url'] for group in plan['groups'] for m in group['members']}
    expected |= {url for family in ledger['families'] for url in family['source_urls']}
    expected |= {source['url'] for source in publication['sources']}
    expected |= {source['url'] for source in intake}
    rows = registry['sources']
    actual = {row['url'] for row in rows}
    assert len(rows) == len(actual), 'Duplicate registry sources'
    assert actual == expected, {'missing': sorted(expected - actual), 'unexpected': sorted(actual - expected)}
    sources = {row['url']: row for row in rows}
    groups = {group['group']: group['members'] for group in plan['groups']}
    for proposal in plan['plans']:
        # This set comes directly from original group membership, not from a
        # previously selected or published list that can repeat an omission.
        for name in proposal['groups']:
            for member in groups[name]:
                row = sources[member['url']]
                assert any(d['target'] == proposal['id'] for d in row['dispositions']), (proposal['id'], member['url'])
    allowed = {'included', 'partial', 'alternative', 'deferred', 'superseded', 'out_of_scope', 'context'}
    for row in rows:
        decisions = row['dispositions'] + row['separate_work_tracks']
        assert decisions, 'Unexplained omission: ' + row['url']
        for decision in decisions:
            assert decision['treatment'] in allowed
            assert decision['rationale'].strip() and decision['review_depth'], row['url']
            if decision['target'].startswith('backlog/'):
                assert decision['treatment'] not in {'included', 'partial'}
                assert decision['original_target'] == row['url']
        snapshot = ROOT / row['snapshot']
        assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == row['snapshot_sha256'], row['url']
        stored = json.loads(snapshot.read_text())
        assert all(stored[key] == row[key] for key in ['url', 'head_sha', 'state', 'author']), row['url']
    return sources

def required_by_plan(sources):
    required = {f'P{n:02d}': set() for n in range(1, 15)}
    for row in sources.values():
        for decision in row['dispositions']:
            required[decision['target']].add(row['url'])
    return required

def validate_bodies(registry, records):
    sources = validate_registry(registry)
    bodies = {row['id']: Path(row['body_file']).read_text() for row in records}
    missing = {}
    for pid, urls in required_by_plan(sources).items():
        assert pid in bodies, 'Missing prepared body: ' + pid
        absent = sorted(url for url in urls if url not in bodies[pid])
        if absent:
            missing[pid] = absent
    assert not missing, {'required_inventory_references_missing_from_bodies': missing}
    return {'registry_sources': len(sources), 'required_feature_bodies': 14, 'passed': True}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepared-prs', type=Path)
    parser.add_argument('--negative-controls', action='store_true')
    args = parser.parse_args()
    registry = json.loads((ROOT / 'reviews/hardware-test/source-registry.json').read_text())
    sources = validate_registry(registry)
    if args.negative_controls:
        import copy
        # Regression: deleting #422 entirely, or retaining it without a P10
        # disposition, must fail despite the rest of the selected list matching.
        for mode in ['delete-source', 'drop-required-plan']:
            broken = copy.deepcopy(registry)
            url = 'https://github.com/omacom/omarchy-pkgs/pull/422'
            if mode == 'delete-source':
                broken['sources'] = [s for s in broken['sources'] if s['url'] != url]
            else:
                row = next(s for s in broken['sources'] if s['url'] == url)
                row['dispositions'] = [d for d in row['dispositions'] if d['target'] != 'P10']
            try:
                validate_registry(broken)
            except AssertionError:
                print(mode + ': correctly rejected')
            else:
                raise AssertionError('Coverage regression accepted: ' + mode)
    if args.prepared_prs:
        print(json.dumps(validate_bodies(registry, json.loads(args.prepared_prs.read_text()))))
    else:
        print(json.dumps({'registry_sources': len(sources), 'dispositions_accounted_for': True,
                          'implementation_complete': False, 'published_bodies_verified': False}))
