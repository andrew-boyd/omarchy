# Rebuilt ISO and software follow-up — 2026-09-21 UTC

**Publication verified:** all 17 existing draft bodies were updated and read back; ten feature/package branches advanced by ordinary fast-forward pushes. [Exact publication receipts](receipts/published-pr-updates.json) retain their heads and body hashes. Every source-reference row and original contribution commit remains preserved.

This packet follows ISO/VM testing of the 14 Intel Mac feature drafts and three package companions. It preserves their source contributions and appends repairs to demonstrated software behavior. It does not establish physical Mac compatibility or release readiness. The [earlier packet](../vm-validation/HANDOFF.md) remains historical evidence.

**The rebuilt ISO is not entirely green.** Its installed Neovim configuration still requests an unavailable Monokai repository and fails a strict startup-error check. That recipe is unchanged from the upstream package base and outside these Mac feature diffs. A guest-only replacement-source experiment passed; it is not included in the ISO. See the [source diagnosis](receipts/editor-source-diagnosis.json) and [unbuilt baseline candidate](baseline-editor-candidate.patch). The ordinary acceptance suite can pass without detecting this error.

The Mac software checks establish package/build, dispatch, configuration-preservation, migration and recovery behavior in a VM. DMI inputs, device attribute files and virtual PCI controllers are fixtures; they are not Apple hardware emulation. No new hardware quirks or device tuning were invented.

## Exact artifact and sources

- ISO SHA256: `af492738c40df1314f08262c042f1fc1fda6fc964b8be1c366966050b45f9b9d`; build exit `0`.
- Built omarchy: `f19b35f0c381b3178acdab049ebf035214a0e6ad`.
- Built omarchy-pkgs: `4ae1c3dabe4833c5a065fd56fd28262428376f34`.
- Built omarchy-iso: `935915cbefaeb3593f5a262647b2df2c2d9604eb`.
- Kernel: `7.2.5-4-omarchy`; runtime: `omarchy-dev 4.0.0.r6542.gf19b35f-1`.
- All 13 embedded local archives were read from the ISO and matched against their build receipts. All 52 changed runtime payloads matched source bytes; the installed guest also passed those payload hashes.
- During the package build, libfprint passed 131/131 tests and fprintd passed 560/560. P12's 12 repository self-test groups passed separately. These do not stand in for maintainer-controlled signed delivery or release CI.
- The local optional T1 desktop package is `0.2.1-2.1`, adapting its dependency to this exact dev runtime. The published package branch keeps stable `omarchy>=4.0.1` and release `0.2.1-2`.

[Verified Git bundles and aggregate patches](integration/sources.json) reconstruct the built trees. [Feature follow-ups](followups/commits.json) identify original and final heads; all original author commits remain ancestors. The [production comparison](receipts/branch-runtime-equivalence.json) records two deliberate differences: standalone P07 retains its legacy package until combined with P06, and the published T1 package keeps its stable dependency. The original contributions do not imply their authors approved later agent-assisted fixes.

## Observed validation

| Check | Result |
| --- | --- |
| Embedded archives and runtime payloads | [passed](stages/build7-artifact.log) |
| Fresh unattended install and full factory reset | [passed](stages/build7-integration.log) |
| Initial combined runtime invocation (see split results below) | [failed (exit 1)](stages/build7-runtime.log) |
| Fresh installed desktop/recovery checks and separate editor experiment | [passed](stages/build7-runtime-followups.log) |
| Actual CS8409 setup, matching-kernel DKMS and reboot | [passed](stages/build7-audio-pro.log) |
| T1 packages, desktop/password fallback and prepared SPI retirement | [passed](stages/build7-t1bridge.log) |
| SPI/PIO migration, initramfs and reboot with model fixture | [passed](stages/build7-spi-pio.log) |
| Actual virtual non-Apple NVMe exclusion | [passed](stages/build7-nvme.log) |
| Old unsafe factory snapshot refusal | [passed](stages/old-snapshot-guard.log) |
| P12 package repository self-tests | [passed](stages/P12-packages-self-tests.log) |
| Five omitted P07/P10 failed-file rechecks | [passed](receipts/missing-rechecks.json) |
| Clean unencrypted installed-base acceptance rerun | [passed](stages/build7-acceptance-clean-rerun.log) |
| Fresh encrypted installation/reboot and acceptance | [passed](stages/build7-encrypted-acceptance.log) |

The initial combined runtime invocation passed the complete CLI/shell suite (270 shell files), but its subsequent desktop check began with a locked session and sudo authentication failed before the privileged recovery checks. The separate fresh overlay passed monitor/keyboard operation, root-private state/locking, failed restore retention/retry, failed RTC propagation, actual virtual S3/RTC and the installed Broadcom hook's pending-state behavior. Its original editor startup still failed; the later guest-only experiment is separately labeled. An aggregate exit of 1 remains 1.

Fresh factory reset passed all eight staging assertions and nine final assertions, including foreign boot entries, directories and UKI byte preservation, automatic first boot, provisioning and the new installation identity. The old-snapshot guard refused the unsafe saved provisioner before account, identity or ESP changes. These baseline repairs belong to the integration source, not unrelated Mac feature branches.

### Standalone source suites

These full invocations preceded a test-only SIGPIPE assertion correction. Later focused results are separate evidence, not green reruns of the entire final tree.

| Scope | Full-suite commit | Original aggregate exit | Observed failed files |
| --- | --- | --- | --- |
| integration | `f19b35f0c381b3178acdab049ebf035214a0e6ad` | [1](source-suites/integration.log) | runtime-smoke-test.sh |
| P03 | `45c4b83a1c53135aed21a70dadad69872eb3d888` | [0](source-suites/P03.log) | none |
| P05 | `e266107021a09c046485e89090fa9f7caa1b45db` | [1](source-suites/P05.log) | preinstalls-test.sh |
| P06 | `eab1ef35fed37698dba4d73d621a243cd781ee46` | [0](source-suites/P06.log) | none |
| P07 | `0014e68e7a4e415aed0eac17ce6741aa39b4d915` | [1](source-suites/P07.log) | manifest-entrypoints-test.sh, runtime-smoke-test.sh, screenshot-sanity-test.sh |
| P09 | `fb6876de4b7f74f23e07660c9a10850e03687f1d` | [0](source-suites/P09.log) | none |
| P10 | `ff6115657d989429ded0a9e4a99570fb9691f578` | [1](source-suites/P10.log) | runtime-smoke-test.sh, screenshot-sanity-test.sh |
| P11 | `62f4540c449b8948716754a3d4e9a998e07bf75b` | [0](source-suites/P11.log) | none |
| P13 | `ddaff2019d2ca19d30ce8c5a27a0f7b18bc9b7ba` | [0](source-suites/P13.log) | none |
| P14 | `05b45a69b30a59c9adcb2248d7f74ec4e9c5d82f` | [0](source-suites/P14.log) | none |

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
