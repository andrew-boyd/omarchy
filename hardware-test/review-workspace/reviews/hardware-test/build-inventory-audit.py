"""Join the full inventory to explicit dispositions; never equate backlog with delivery."""
import json
from pathlib import Path
from collections import Counter
import shutil

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
read = lambda path: json.loads((ROOT / path).read_text())
plan = read('reviews/grouped-prs/plan.json')
ledger = read('reviews/rollups/2026-09-19T2227Z-brightness-range/ledger.json')
fresh = read('reviews/hardware-test/inventory-refresh.json')
prior = read('reviews/publication/source-decisions.json')
extra = read('reviews/hardware-test/additional-dispositions.json')
current_rationales = read('reviews/hardware-test/current-selection-rationales.json')
families = {f['family']: f for f in ledger['families']}
assigned = {g: p['id'] for p in plan['plans'] for g in p['groups']}
original = {m['url'] for g in plan['groups'] for m in g['members']}

# These are boundaries for independent work, not approvals of code or invented
# hardware fixes. The original source remains the trial/review target.
boundaries = {
    'alpine-ridge': 'Thunderbolt/USB controller recovery is a separate work track: DKMS/kernel correction, PCI removal/rescan, wake-source masking and global USB policy are not interchangeable. Keep model-specific source targets; no universal suspend policy is selected.',
    'apple-fnmode': 'Keep the existing Apple keyboard function-row policy proposal separate from layout-widget device eligibility. Preserve administrator settings and the non-Apple keyboard behavior during eventual review.',
    'applesmc-fans': 'Keep the single-fan applesmc supervisor package as an opt-in package review; no automatic fan-control installation is added to the 14 feature branches.',
    'baffin-capture': 'Keep the existing Baffin CPU-encoding workaround as a distinct capture proposal. It does not establish general Radeon or suspend stability.',
    'battery-limits': 'Keep battery-state display and charge-threshold support as a separate feature. Administrative duplicate closure does not settle threshold parsing, pending-charge behavior or hardware support.',
    'bcm5974-trackpad': 'Keep device recognition and reset error handling separate from SPI PIO and T2 internal-device tagging. Existing source targets retain the older bcm5974 coverage.',
    'bluetooth-audio': 'Retain the ACL-priority and dropout work as distinct Bluetooth policies; similar audio symptoms do not establish compatible controller/transport changes.',
    'bluetooth-discovery': 'Keep pairing-agent lifecycle and USB/controller power policy separate. Preserve the MacBookPro12,1 report and the explicit successor to #8572; Apple Silicon-only reports are adjacent evidence, not Intel validation.',
    'brightness-range': 'A prior local experimental consolidation exists, but it was not one of the 14 published implementation branches. Retain both original patches and their differing minimum/step policies; do not describe the experiment as shipped in the ISO.',
    'brightness-routing': 'Keep AIO kernel-backlight routing, missing-backlight software dimming and Apple Silicon panel preference separate. They require different output-ownership rules; no universal fallback is selected.',
    'cpu-instructions': 'Keep AVX2 and SSE4.2/POPCNT application eligibility as separate older-CPU support. Track #8149 through its explicit #11514 successor; an x86_64 CPU alone does not prove every bundled application can execute.',
    'cpu-power': 'Keep MacBook10,1 RAPL limits, pre-HWP profile mapping and T2 policy/PROCHOT changes separate. Their model-specific power values are not generalized to other Macs.',
    'efi-preservation': 'Full-disk EFI preservation is an ISO delivery dependency, not a runtime driver feature. Both existing source commits are preserved in the revised ISO source; nine unit tests and a fresh VM disk-wipe round trip passed, including all three synthetic file hashes. Physical firmware preservation remains untested and requires an independent external backup. Historical B7 lacks the contribution.',
    'external-modes': 'Retain the existing T2/Studio Display link proposal as a separate external-display test target. The 14 branches do not select link rates or certify 5K DSC behavior.',
    'gmux-brightness': 'Separate reading actual gmux brightness from persistence across reboot. Retain #8205 independently and compare the #8371/#9910 persistence implementations despite duplicate closure.',
    'haswell-voxtype': 'Retain the existing Haswell Vulkan-to-CPU backend proposal independently from CPU instruction gating and general VA-API selection.',
    'imac-5k': 'Retain iMac18,3 documentation and reported gaps as a distinct model record. Adding a model name does not supply the linked patcher or validate all four gaps.',
    'imac-gpu-boot': 'Retain the exact iMac20,2 AMD/Apple PCI-gated UCLK proposal as a separate GPU trial. Do not extend its power-feature mask to the available 13,3 or other iMac GPUs.',
    'image-picker': 'Retain optional picker IPC as an independent desktop integration proposal. It is not required by the selected released T1Bridge provider and does not imply hardware enablement.',
    'intel-video': 'Retain pre-Broadwell VA-API selection as its own installer proposal, including Haswell/Ivy Bridge evidence. No driver-generation correction is supplied by the current detection roll-up.',
    'keyboard-backlight-state': 'Retain saved-state/restore ownership as a separate concern shared by lock, idle and sleep. Do not stack alternate save/restore implementations into T1Bridge automatically.',
    'keyboard-backlight-steps': 'Retain old media bindings and the competing fixed-four-level versus symmetric-step policies separately; these are not the same feature as keyboard-device layout selection.',
    'legacy-gpu': 'Retain the existing MacBookPro11,5 radeon selection as a model-specific driver trial. It is not a generic recommendation to switch or disable GPUs on Intel Macs.',
    'mbp131-bundle': 'Keep the complete MacBookPro13,1 package/runtime bundle visible across camera, audio and SPI retirement. A single feature branch does not supersede all of its delivered behavior.',
    'mbp133-bundle': 'Retain the broader MacBookPro13,3 bundle and its negative Radeon/suspend evidence. Selected calibration or NVMe components do not establish that the whole bundle is included or stable.',
    'model-docs': 'Retain the separate model-list corrections and T2 resource link. Model documentation remains useful across the full Intel scope, independently of which machine is tested first.',
    'older-macs': 'Keep pre-T1 graphics/Wi-Fi/application gaps and the iMac7,1 evidence visible. Core 2 Duo machines are in scope where x86_64-capable; 32-bit-only Intel Macs are not implied by broad year ranges.',
    'outside-scope': 'Generic night-light temperature preference has no established Intel Mac compatibility requirement in the inventory evidence. Retain as excluded context, not as a missing hardware fix.',
    'pre-t2-hibernation': 'Retain delayed GPU initialization during hibernation as a separate boot/resume proposal; normal suspend and NVMe power-state changes do not cover it.',
    'sandy-idle': 'Keep the existing MacBookAir4,1/4,2 C-state cap as a narrow model-specific trial, with its power tradeoff explicit. Do not generalize the cap to all older Intel CPUs.',
    'sd-reader': 'Keep the Apple USB card-reader recovery as a separate peripheral track. Its GPIO and controller assumptions must not be inferred from the first physical test machine.',
    'session-start': 'Keep the existing Macmini7,1 graphical-session cleanup proposal independent of lid handling and output enumeration; it changes session startup ownership.',
    't1-lid-gpu': 'Retain the existing stay-awake lid/GPU bundle separately. Avoiding suspend is a distinct policy with thermal implications, not evidence that suspend has been fixed.',
    't1-pcie': 'Retain the existing T1 PCIe command-line migration as its own upgrade proposal. Removing pcie_ports=compat and adding sleep defaults is not implied by T1Bridge or SPI retirement.',
    't2-alsa': 'Retain T2 overlay-install PipeWire ALSA availability separately from pre-T2 Cirrus packages; the driver stacks and installation paths differ.',
    't2-ethernet': 'Keep the T2 internal NCM exclusion pair as a separate network track, with #10224 closed in favor of #8204. External Ethernet must remain outside that exclusion.',
    't2-gmux': 'Keep the T2 mux/rendering backend as a distinct model-specific graphics trial, including external-display and GPU-power limits. It is not transplanted onto pre-T2 gmux machines.',
    't2-hibernation': 'Retain the existing T2 hibernation refusal policy separately from changes that attempt to enable suspend; an S3 or s2idle report does not validate S4.',
    't2-imac-framebuffer': 'Retain the exact Navi 14 iMac20,x EFI-framebuffer proposal independently of the other iMac UCLK workaround; GPU IDs and failure stages differ.',
    't2-installation': 'Retain the existing T2 overlay ESP/Linux-entry migration as a separate installation track. It is not covered by full-disk T1 firmware preservation.',
    't2-power-docs': 'Retain the MacBookPro16,1 power/graphics guide as model-specific evidence and optional settings. Do not turn its local demand controller into a universal installer policy.',
    't2-repository': 'Retain signature-policy, signed-package replacement and repository-refresh proposals as distinct operations. Select authenticated available delivery before changing T2 package sources; the current roll-ups do not settle that repository migration.',
    't2-suspend': 'Keep model-specific async ordering, deep/s2idle, controller power and Wi-Fi lifecycle trials separate. Positive and contrary reports coexist; no single T2 sleep policy is selected from classifier similarity.',
    't2-trackpad': 'Keep the T2 internal-trackpad proposals together for comparison, preserving product-ID instability and logout/reboot evidence from closed #10890. Do not substitute SPI work for the USB/libinput classification change.',
    'thunderbolt-kernel': 'The supplied reproduction uses an AMD mini PC with an Apple display, not an Intel Mac host. Retain adjacent kernel context until an Intel Mac requirement is established.',
    'trackpad-defaults': 'Retain optional gesture documentation as a customization proposal, separate from input-driver or palm-rejection support.',
    'wifi-country': 'Regulatory hinting remains a distinct P10 follow-up; preserve an existing deliberate country setting rather than deriving calibration policy from signal symptoms.',
    'wifi-firmware': 'Firmware availability for non-T2 brcmfmac Macs remains a separate P10 delivery concern; two selected NVRAM files do not supply every model firmware.',
    'wifi-legacy': 'Preserve BCM4322 b43, BCM43224 wl and BCM4350 upgrade-driver selection as distinct P10 tracks. Their driver/blacklist policies cannot be combined by chip-vendor name alone.',
    'wifi-scanning': 'Retain shared UI scan ownership as a separate network-panel proposal, not a firmware or RF calibration change.',
    'wifi-t2-combo': 'Keep T2 combo-device and simple post-resume recovery separate from the selected pre-T2 hook; inspect complete ordering and known failure reports before any T2 integration.',
    'wifi-t2-connectivity': 'Keep MacBookPro16,1 SAE/WPA3 policy as its own P10 follow-up; current calibration and recovery do not implement it.',
    'picture-in-picture': 'The prior local study retained the source unchanged. Keep the original as the independent desktop proposal; no additional consolidation branch is warranted for this single source.',
    'audio-realtime': 'Keep rtkit activation/retry behavior as an independent shared-audio proposal. The prior local experimental patch is not part of the published Cirrus roll-up.',
    't2-fan-resume': 'Retain the newly discovered iMac20,1 t2fanrd post-resume restart proposal as a separate T2 cooling track. It is not the pre-T2 single-fan afanctl package.',
}
normalize = {'incorporated': 'included', 'partial': 'partial', 'alternative': 'alternative',
             'broader': 'context', 'predecessor': 'superseded', 'already-covered': 'superseded',
             'context': 'context', 'held': 'deferred'}
records = []
for source in fresh['sources']:
    source = dict(source)
    # Keep the public GitHub evidence portable with this audit instead of
    # depending on an ignored machine-local cache for future verification.
    cached_snapshot = ROOT / source['snapshot']
    archived_snapshot = HERE / 'source-snapshots' / cached_snapshot.name
    archived_snapshot.parent.mkdir(exist_ok=True)
    shutil.copyfile(cached_snapshot, archived_snapshot)
    source['snapshot'] = str(archived_snapshot.relative_to(ROOT))
    key = f"{source['repository']}#{source['number']}"
    dispositions = []
    for pid, table in prior.items():
        if key in table:
            treatment, rationale = table[key]
            rationale = current_rationales.get(key, rationale)
            dispositions.append({'target': pid, 'treatment': normalize[treatment],
                                 'rationale': rationale, 'basis': 'previous-published-selection',
                                 'review_depth': 'retained prior source comparison; later software repairs recorded separately'})
    if key in extra:
        decision = extra[key]
        for pid in decision['plans']:
            dispositions = [d for d in dispositions if d['target'] != pid]
            dispositions.append({'target': pid, 'treatment': decision['treatment'],
                                 'rationale': decision['rationale'], 'basis': 'current-inventory-audit',
                                 'review_depth': 'source scope, production changes and relevant discussion'})
    # Every unassigned original family remains visible even where one source is
    # also referenced by a narrower feature body.
    tracks = []
    for group in source['groups']:
        if group in assigned:
            continue
        if group not in boundaries:
            raise ValueError('Unreviewed family boundary: ' + group)
        tracks.append({'target': 'backlog/' + group,
                       'treatment': 'out_of_scope' if group == 'outside-scope' else 'deferred',
                       'rationale': boundaries[group], 'original_target': source['url'],
                       'review_depth': 'scope triage; not a completed implementation comparison',
                       'previous_work': families.get(group, {}).get('artifacts', [])})
    if not dispositions and not tracks:
        raise ValueError('Unexplained source omission: ' + key)
    required = {assigned[group] for group in source['groups'] if group in assigned}
    if not required <= {d['target'] for d in dispositions}:
        raise ValueError('Assigned family source lacks per-plan disposition: ' + key)
    records.append({**source, 'source_key': key, 'original_inventory_member': source['url'] in original,
                    'dispositions': dispositions, 'separate_work_tracks': tracks,
                    'state_note': 'Current state is administrative history, not proof of equivalent code or hardware coverage.',
                    'hardware_validation': 'No new physical hardware test by this audit.'})

counts = {'all_known_and_added_sources': len(records), 'original_inventory_sources': len(original),
          'sources_referenced_by_rollups': sum(bool(s['dispositions']) for s in records),
          'sources_only_in_separate_work_tracks': sum(not s['dispositions'] for s in records),
          'source_states': dict(Counter(s['state'] for s in records)),
          'rollup_table_rows': sum(len(s['dispositions']) for s in records),
          'unique_sources_with_included_or_partial_claim': sum(any(d['treatment'] in ['included', 'partial'] for d in s['dispositions']) for s in records)}
validation_file = HERE / 'final-validation.json'
publication_file = HERE / 'published-pr-updates.json'
validation = json.loads(validation_file.read_text()) if validation_file.exists() else {}
publication = json.loads(publication_file.read_text()) if publication_file.exists() else {}
result = {'scope': 'All 64-bit Intel Macs; pre-T1, T1 and T2. MacBookPro13,3 is only the first physical test target.',
          'counts': counts, 'sources': records,
          'qualification': 'Inventory/disposition coverage is not implementation completion. Separate work tracks remain unimplemented by P01–P14; alternative/deferred/context rows are not ISO content.',
          'publication_updated': publication.get('completed_count') == 17,
          'iso_rebuilt': validation.get('required_checks_satisfied', False)}
(HERE / 'source-registry.json').write_text(json.dumps(result, indent=2) + '\n')
lines = ['# Full Intel Mac inventory', '', result['scope'], '', result['qualification'], '',
         'This is the current audited inventory. The dated test report and publication receipts identify the tested ISO and the state of the 17 existing draft updates.', '',
         '| Source | Current state | Roll-up disposition | Separate work track |', '| --- | --- | --- | --- |']
for s in records:
    targets = '; '.join(d['target'] + ': ' + d['treatment'] for d in s['dispositions']) or 'None'
    tracks = ', '.join(t['target'].removeprefix('backlog/') for t in s['separate_work_tracks']) or 'None'
    lines.append(f"| [{s['source_key']}]({s['url']}) — {s['title'].replace('|', '/')} | {s['state']} | {targets} | {tracks} |")
lines += ['', '## Separate work tracks', '', 'These are retained scope, not completed consolidation PRs. Each source keeps its existing PR as the review/test target until the feature comparison is complete.', '']
for group in sorted(boundaries):
    members = [s for s in records if any(t['target'] == 'backlog/' + group for t in s['separate_work_tracks'])]
    if not members:
        continue
    lines += ['### ' + group, '', boundaries[group], '', ', '.join(f"[{s['source_key']}]({s['url']})" for s in members), '']
(HERE / 'INVENTORY.md').write_text('\n'.join(lines).rstrip() + '\n')
print(json.dumps(counts))
