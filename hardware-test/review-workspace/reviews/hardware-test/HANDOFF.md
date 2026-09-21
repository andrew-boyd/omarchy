# Intel Mac ISO: ready for the first attended hardware trial

The reconciled ISO has completed fresh encrypted and unencrypted VM installations and the required software checks. **Physical Mac behavior remains untested by this effort.** The original failed build and runtime aggregate remain recorded alongside their qualified reruns. This is a test candidate, not a release or a claim that every Intel Mac is supported.

## Artifact and exact sources

Use `omarchy-intel-mac-20260921-9e6288ef.iso` (6,215,624,704 bytes):

```text
SHA-256 9e6288ef5cc1eadce519cdd7384c8030286eb938a6288eb218f025a61b433252
```

The builder's equivalent filename is `omarchy-2026.09.21-intel-mac-local-x86_64.iso`. The private handoff also supplies `SHA256SUMS`, the matching companion package bundle, and the installation guide. Both complete downloads were hash-verified over the private tailnet; the ISO is not a public release attachment.

| Source | Built commit | Assessed upstream base |
| --- | --- | --- |
| Omarchy | `6096d649643d0d0e0bae65c7949e5043bf2cc338` | `8f324c90b82790d31ab33565441e07cbdb8d2308` (`quattro`) |
| Packages | `25712c910f80fdf5989c6434e3e2fa8830ec2581` | `e40f5a5da918e8b923115ebb4c335b6c4828fefe` (`master`) |
| ISO | `d692d24f95c6611f86beef7e4d7c6e23a7d2f42a` | `7cfb7111a06873d61c45d37034577d4ba08d3f4f` (`quattro`) |

The ISO source pins archiso `424e78130db2af6c1ceb55b442d7914b1109ff2b`. Installed versions include `omarchy-dev`/`omarchy-settings-dev` `4.0.0.r6578.g6096d64-1`, `linux-omarchy` `7.2.5-4`, and `omarchy-nvim` `2026.8.13-1.1`. The artifact check verifies all 13 embedded local archives, 74 changed runtime files, both EFI preservation source files and the Neovim plugin pin. [Exact artifact receipt](receipts/artifact.json).

The companion archive contains ten packages for separate hardware tracks; install only the matching track. Its SHA-256 is `2a56569086336894aaeb6892217fba57d65cbcec8f14dcb0faa549e4112df1ec`. The two audio tracks conflict. T1 setup remains manual. [Package manifest](companion-download.json) and [installation guide](HARDWARE-INSTALL.md).

## What was tested

| Check | Observed result and boundary |
| --- | --- |
| Fresh build and ISO contents | Final build passed; exact embedded archives and runtime payloads match the pinned sources. The first build's libfprint failure is retained below. |
| Fresh EFI disk-wipe installation | Passed: all three synthetic firmware files retained identical hashes; unrelated old marker removed; original seed unchanged. Synthetic bytes, not Apple firmware. |
| Fresh unencrypted installation | Install, reboot and all eight desktop acceptance files passed. |
| Fresh encrypted installation | Install, reboot and all eight desktop acceptance files passed. Installer logs establish LUKS2 and mapped-root use; no negative encryption-password test is claimed. |
| Full source suite | 273 files completed without failures; two checks skipped: no valid `/dev/hiddev*` cache fixture, and no Kitty executable for its native configuration parser. |
| ISO unit suite | 78 tests passed, including nine EFI preservation tests. |
| Neovim | Strict startup returned an empty error message and explicit Monokai theme loading passed. The unavailable baseline plugin reference was replaced with a pinned source; this was not caused by a Mac feature patch. |
| Installed password, desktop and recovery checks | The original shared-suite invocation failed after a confirmed PAM lockout. All three checks passed in a clean overlay of the same installed ISO; details below. |
| Camera, audio12, audio-pro and T1 package tracks | All four separate package/install/DKMS/reboot scenarios passed. T1 also passed password fallback and repeated legacy-SPI removal while retaining native input and replacement packages. No device was emulated as a functioning camera, codec or T1 bridge. |
| SPI-PIO and retained-kernel/header migrations | Both passed. The kernel test retained stock `linux` `7.2.6.arch2-1` and `linux-omarchy` `7.2.5-4`, matching headers and Broadcom DKMS. |
| Non-Apple NVMe | A real virtual controller at `0000:01:00.0` was excluded; its power setting and customized unit were preserved. No Apple NVMe hardware test. |

The clean installed checks covered wrong-password rejection followed by correct-password unlock, virtual monitor preservation, US/DE keyboard switching, private root-state permissions, failed restore retention/retry, RTC failure propagation, virtual RTC sleep/wake, and retained failed Broadcom recovery state. [Final results](receipts/results.json), [stage logs](stages), and [VM logs/screenshots](vm-runs).

Selected screenshots were inspected, including lock/unlock, keyboard layout, Neovim and the encrypted-install desktop. Two frames named as first-boot LUKS prompts actually show the bootloader menu; their filenames are not visual proof of that dialog. [Visual-review receipt](receipts/visual-review.json).

## Failures preserved, not relabeled as passes

The first build failed the libfprint USB replay test `egis_etu905` (130 of 131 tests passed). With unchanged compiled source and tests, three isolated repeats, two complete serial suites (262 tests), and the normal package check (131 tests) passed. No test was skipped and no timeout or driver fix was invented. The original failure's cause remains unestablished. The final build reused only 13 archives whose source commits and hashes were verified. [Reuse receipt](receipts/build-reuse.json), [failed build log](build/first-attempt-failed.log), and [recheck log](build/libfprint-recheck/recheck.log).

The full source suite triggered repeated NetworkManager Polkit authentication failures and a journal-confirmed temporary PAM account lockout before the installed password/desktop/recovery checks. Those three checks failed in that guest, then passed in a clean overlay with the same installed payload. Inspection of the preserved failed guest confirmed the original test password was unchanged; the exact individual source test initiating the requests was not isolated. **The original runtime stage and validation aggregate remain exit 1.** No product or authentication-policy change was made to produce the rerun. Future runs should keep the full source suite and installed authentication checks in separate overlays. [Diagnosis and exact rerun coverage](receipts/runtime-rechecks.json).

These qualified reruns satisfy the required individual software checks. They do not turn the original aggregate green or establish physical suspend, firmware, Wi-Fi, audio, graphics, input or fingerprint behavior.

## Inventory, consolidation and attribution

Scope remains **all 64-bit Intel Macs: pre-T1, T1 and T2**. The audit accounts for 188 known/intake PRs: 101 have dispositions in feature tables, while 87 remain only in separate work tracks. There are 14 feature targets and three package companions. These counts describe references and decisions, not 188 implemented PRs or 188-to-14 compression.

All 69 sources from the original groups assigned to P01–P14 are represented in the relevant tables. The audit corrected 13 previously missing references, including package #422. The independent coverage check derives its requirements from the original grouping and rejects both deleting #422 and dropping its P10 disposition. [Audit and cause](AUDIT.md), [complete inventory](INVENTORY.md), and [latest source freshness](receipts/prepublication-source-delta.json).

#422 remains a separate BCM43602 kernel alternative, including its MacBookPro12,1 evidence; it is not in this ISO. P10 uses the existing #7333 BCM4350/BCM43602 boundary with source-author credit. Different T2 recovery proposals remain visible without automatically stacking competing implementations. A prior broad hook on an earlier T2 trial needs manual reconciliation.

All 17 candidate branches preserve their original published commits as ancestors. Bundles retain contribution history and author/co-author metadata. The combined candidate has 87 production-file comparisons with standalone feature branches: 78 identical and nine explicitly explained differences, none unexplained. Combined-image passes do not certify every standalone variant. [Branch receipt](receipts/branch-preparation.json), [differences](receipts/integration-coverage.json), and [source reconstruction/reproduction](REPRODUCE.md).

## Physical test handoff

The first available machine is **MacBookPro13,3**, one T1 model within the wider effort. Follow [HARDWARE-INSTALL.md](HARDWARE-INSTALL.md) for independent data/EFI backups, recovery, matching package installation and ordered tests. The selected T1Bridge release documents system suspend/resume as not working on its tested machine; this remains unresolved here. Preserve same-machine FDR data, password fallback and a local recovery path. The build host's custom Touch Bar runtime and tuning are not silently included in the ISO.

No USB drive has been flashed and no physical installation has been performed. The next step is to identify the attended test machine and USB device, verify backups, then explicitly proceed with media creation and installation. Record results per model using [HARDWARE-MATRIX.md](HARDWARE-MATRIX.md).

## Existing draft publication

All **17 existing drafts** (14 Omarchy features and three package companions) were updated and read back successfully. Every expected commit and complete PR-body hash matches, and all remain open drafts. [Verified publication receipts](receipts/published-pr-updates.json) identify each URL, head and verification time. The package history required the machine's existing GitHub SSH login because the CLI OAuth token lacks workflow scope; no credentials, source commits or workflow files were changed to resolve transport. Original source PRs remain untouched, and nothing was posted to Basecamp/chat.
