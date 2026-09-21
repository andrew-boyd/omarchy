#!/usr/bin/python
"""Prepare the evidence narrative from observed receipts, including failures."""
from pathlib import Path
import json, difflib
root=Path(__file__).resolve().parents[2];w=root/'.state/vm-install/2026-09-20';p=w/'remediation'
out=w/'pr-followups/review-index/vm-remediation'
r=json.loads((root/'reviews/remediation/results.json').read_text())
def result(n):
 v=r['stages'].get(n)
 return 'pending' if v is None else ('passed' if v==0 else 'failed (exit '+str(v)+')')
text='''# Rebuilt ISO and software follow-up — 2026-09-21 UTC

This packet follows ISO/VM testing of the 14 Intel Mac feature drafts and three package companions. It preserves their source contributions and appends repairs to demonstrated software behavior. It does not establish physical Mac compatibility or release readiness. The [earlier packet](../vm-validation/HANDOFF.md) remains historical evidence.

**The rebuilt ISO is not entirely green.** Its installed Neovim configuration still requests an unavailable Monokai repository and fails a strict startup-error check. That recipe is unchanged from the upstream package base and outside these Mac feature diffs. A guest-only replacement-source experiment passed; it is not included in the ISO. See the [source diagnosis](receipts/editor-source-diagnosis.json) and [unbuilt baseline candidate](baseline-editor-candidate.patch). The ordinary acceptance suite can pass without detecting this error.

The Mac software checks establish package/build, dispatch, configuration-preservation, migration and recovery behavior in a VM. DMI inputs, device attribute files and virtual PCI controllers are fixtures; they are not Apple hardware emulation. No new hardware quirks or device tuning were invented.

## Exact artifact and sources

'''
a=r['artifact'];text+=f"- ISO SHA256: `{a['sha256']}`; build exit `{a['build_exit']}`.\n"
for name,head in a['source_commits'].items():text+=f'- Built {name}: `{head}`.\n'
text+='''- Kernel: `7.2.5-4-omarchy`; runtime: `omarchy-dev 4.0.0.r6542.gf19b35f-1`.
- All 13 embedded local archives were read from the ISO and matched against their build receipts. All 52 changed runtime payloads matched source bytes; the installed guest also passed those payload hashes.
- During the package build, libfprint passed 131/131 tests and fprintd passed 560/560. P12's 12 repository self-test groups passed separately. These do not stand in for maintainer-controlled signed delivery or release CI.
- The local optional T1 desktop package is `0.2.1-2.1`, adapting its dependency to this exact dev runtime. The published package branch keeps stable `omarchy>=4.0.1` and release `0.2.1-2`.

[Verified Git bundles and aggregate patches](integration/sources.json) reconstruct the built trees. [Feature follow-ups](followups/commits.json) identify original and final heads; all original author commits remain ancestors. The [production comparison](receipts/branch-runtime-equivalence.json) records two deliberate differences: standalone P07 retains its legacy package until combined with P06, and the published T1 package keeps its stable dependency. The original contributions do not imply their authors approved later agent-assisted fixes.

## Observed validation

| Check | Result |
| --- | --- |
'''
labels={'build7-artifact':'Embedded archives and runtime payloads','build7-integration':'Fresh unattended install and full factory reset','build7-runtime':'Initial combined runtime invocation (see split results below)','build7-runtime-followups':'Fresh installed desktop/recovery checks and separate editor experiment','build7-audio-pro':'Actual CS8409 setup, matching-kernel DKMS and reboot','build7-t1bridge':'T1 packages, desktop/password fallback and prepared SPI retirement','build7-spi-pio':'SPI/PIO migration, initramfs and reboot with model fixture','build7-nvme':'Actual virtual non-Apple NVMe exclusion','old-snapshot-guard':'Old unsafe factory snapshot refusal','P12-packages-self-tests':'P12 package repository self-tests','missing-rechecks':'Five omitted P07/P10 failed-file rechecks','build7-acceptance-clean-rerun':'Clean unencrypted installed-base acceptance rerun','build7-encrypted-acceptance':'Fresh encrypted installation/reboot and acceptance'}
for name,label in labels.items():
 link='receipts/missing-rechecks.json' if name=='missing-rechecks' else 'stages/'+name+'.log'
 text+=f'| {label} | [{result(name)}]({link}) |\n'
text+='''
The initial combined runtime invocation passed the complete CLI/shell suite (270 shell files), but its subsequent desktop check began with a locked session and sudo authentication failed before the privileged recovery checks. The separate fresh overlay passed monitor/keyboard operation, root-private state/locking, failed restore retention/retry, failed RTC propagation, actual virtual S3/RTC and the installed Broadcom hook's pending-state behavior. Its original editor startup still failed; the later guest-only experiment is separately labeled. An aggregate exit of 1 remains 1.

Fresh factory reset passed all eight staging assertions and nine final assertions, including foreign boot entries, directories and UKI byte preservation, automatic first boot, provisioning and the new installation identity. The old-snapshot guard refused the unsafe saved provisioner before account, identity or ESP changes. These baseline repairs belong to the integration source, not unrelated Mac feature branches.

### Standalone source suites

These full invocations preceded a test-only SIGPIPE assertion correction. Later focused results are separate evidence, not green reruns of the entire final tree.

| Scope | Full-suite commit | Original aggregate exit | Observed failed files |
| --- | --- | --- | --- |
'''
for s in r['original_full_suites']:
 failures=', '.join(Path(x).name for x in s['failed_files']) or 'none'
 text+=f"| {s['id']} | `{s['tested_commit']}` | [{s['aggregate_exit']}](source-suites/{s['id']}.log) | {failures} |\n"
text+='''
All nine final feature heads have separate passing checks of the corrected preinstall assertion. The original P05 failure was reproduced as `printf` receiving SIGPIPE after `grep -q` exited early; a consuming grep repairs the fixture. Other observed failed files were scheduled in individual fresh guest overlays. Original shared-guest UI cleanup, IPC and screenshot failures remain in their logs. Their passing isolated reruns do not by themselves prove that all shared-session interactions have been repaired.

The first recheck loop let SSH consume its input list and skipped five P07/P10 files despite returning zero. [The correction](receipts/focused-recheck-stdin-correction.json) and [individual completion receipts](receipts/missing-rechecks.json) retain that distinction. Body preparation checks the actual failed-file coverage, not merely the wrapper exit.

## Software follow-ups and remaining boundaries

- P03 reads disappearing PCI attributes quietly and safely. P05 keeps an identityless external connector available in the monitor panel; it cannot certify that another physical panel shows an image.
- P06 checks T1Bridge packages and native applespi for every retained kernel before retirement. Firmware, live provider transition and initramfs preparation remain manual. P07 preserves customized SPI/PIO configuration and retry markers without altering source hardware parameters.
- P09 preserves custom/symlinked units and keeps unknown PCI identity pending. Its fixed model/PCI applicability still needs hardware evidence. P10 preserves customized hooks and failed/partial rebind state; actual Broadcom sleep behavior remains unverified.
- P11 anchors model gates, uses the matching kernel headers and preserves audio/user service configuration and saved routes. Codec, speaker and mixer tuning are unchanged.
- P12's optional brightness controller rejects powered-off/disabled/external-only/unknown panels. Automatic keyboard lighting, manual T1 provisioning/provider setup and physical whole-system suspend remain outside this verified scope.
- P13 retains the installed kernel when DMI vendor identity is unreadable. Its original Apple-prefix exemption remains; it does not roll back already migrated systems.
- P14 serializes privileged state, retains failed restoration records, propagates failures and preserves existing rules. Virtual RTC proves software flow; physical wake causality and cancellation during an actual interrupted Mac suspend remain unverified.
- P01/P02/P08 have no additional demonstrated runtime defect from this audit. Their earlier dated VM evidence still applies within its bounds. P04's rejected debounce and blanket USB-exclusion alternatives remain excluded; compatible future contributions can target its existing draft.

## Evidence integrity and known test incidents

The first Build 7 desktop acceptance failed after an agent bootstrap intervention left the graphical session on an inactive VT. [The receipt](receipts/build7-first-acceptance-vt-failure.json) identifies this as a test intervention, not an established product defect. The revised harness confirms a spare console login prompt before typing credentials. It is a separate patch; it does not change the ISO hash.

ISO reader retries corrected multi-extent extraction and archive ownership mapping. The earlier failures remain under `diagnostics/`. A previous full suite accidentally inherited host XDG paths; the exact accidental config/route change was restored byte-for-byte, with [restoration hashes](receipts/host-test-isolation-restoration.json). All later full suites ran in VMs. Private host files, VM disks and SSH private keys are excluded from this packet.

Use [the reproduction guide](REPRODUCE.md), [machine-readable results](receipts/results.json), and [file hashes](SHA256SUMS). The 17 existing drafts remain the contribution targets. No original PRs were modified or closed; this follow-up creates no additional PR, release or chat message. Original source-reference tables remain in every draft body. Physical hardware reports and maintainer-controlled integration/delivery remain future work.
'''
(out/'HANDOFF.md').write_text(text)
recipe=w/'repos/omarchy-pkgs/pkgbuilds/omarchy-nvim/lua/plugins/all-themes.lua'
original=recipe.read_text();replacement=original.replace('gthelding/monokai-pro.nvim','loctvl842/monokai-pro.nvim')
(out/'baseline-editor-candidate.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),replacement.splitlines(True),fromfile='a/pkgbuilds/omarchy-nvim/lua/plugins/all-themes.lua',tofile='b/pkgbuilds/omarchy-nvim/lua/plugins/all-themes.lua')))
print('Prepared handoff with actual results and explicit unresolved editor defect; no remote writes.')
