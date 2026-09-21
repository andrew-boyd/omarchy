# Intel Mac ISO / VM validation handoff

Scope: the 14 Intel Mac feature drafts and three package companions. These remain consolidation and hardware-testing targets. VM results establish build, installation and software behavior; they do not certify physical Mac support or release readiness.

## Tested artifacts

Build 5 (`build-20260921T014550Z-X4tHsG`) built the combined series, installed through both encrypted interactive and unencrypted unattended paths, and rebooted from the installed disk. Its SHA256 is `0026b7df063f20ebbe4f56bca1d19c3920dbb00807539127ba32703489a44c7d`. The encrypted install confirmed a LUKS partition containing the Btrfs root.

Build 6 (`build-20260921T030051Z-m0fg6D`) repairs an observed audio-package dependency. Its SHA256 is `4c76334deab6c999b55814122132f95c8d9fe8e61be9f06a0e7ebd3fd8e073bb`. All 13 embedded local archives were streamed from the ISO filesystem and hash-verified. Twelve are byte-identical to Build 5; only `macbook12-audio-driver-dkms` changes, from `0.1-1` to `0.1-2`. The runtime, settings, kernel and other Mac packages are unchanged. The final install/retest receipt identifies results completed on Build 6 separately from the broader Build 5 coverage.

The installed runtime is `omarchy-dev 4.0.0.r6529.g8ffe7ac-1`, with `linux-omarchy` and matching headers `7.2.5-4`. All 49 changed installed runtime/default/setup files matched their source hashes in Build 5. No product checkout was dev-linked into the guest.

Build 6 completed a fresh interactive unencrypted install and installed-disk boot. Its eight desktop acceptance files passed in 94 seconds. The original SSH bootstrap targeted a virtual terminal occupied by SDDM; selecting the confirmed tty4 and executing the existing bootstrap corrected the harness path. The repaired audio package then installed in an independent overlay, compiled for the running kernel and rebooted. Stock `linux`/`linux-headers` remained absent, the prior orphan-kernel hook error disappeared, PAM files were unchanged, and all 49 installed changed payload files again matched their expected hashes.

## What the VM checks establish

- The combined CLI suite and all 267 shell test files passed in the live Build 5 guest, including focused rechecks after staging missing companion source checkouts. The graphical/QML tests ran in its actual desktop. Native Kitty configuration parsing passed after adding Kitty to the guest. The physical `/dev/hiddev*` cache case remains skipped.
- All eight graphical acceptance files passed. The original OCR failures are retained: one visible phrase split across lines, and one title misread at 2x scale. A test-only patch normalizes whitespace and retries native resolution. It changes no installed product files.
- Real package transactions, target-kernel DKMS compilation and reboot passed for camera, CS8409 audio and T1Bridge. The 12-inch audio transaction revealed the dependency defect described below. Libfprint's 131 and fprintd's 560 package tests passed during building; serial execution resolved a reproduced resource-sensitive replay failure.
- Guest desktop checks exercised keyboard layout labels (EN → DE → EN), monitor watcher reload, T1 volume/mute/OSD and fallback notification. Actual lock-screen input rejected a wrong password and accepted the guest password, including with T1 packages installed. Screenshots were inspected.
- Upgrade scenarios exercised stock kernel/header repair, retained-kernel policy, repeated legacy SPI package removal, MacBook8,1 PIO setup and boot-image regeneration, and non-Apple virtual NVMe exclusion. Model/vendor inputs are explicitly identified as fixtures; package transactions and boot generation were real guest operations.
- The installed suspend diagnostic completed a real virtual RTC-triggered 11-second deep/S3 sleep/resume. Its known recovery limitations were reproduced separately with controlled guest fixtures.

See the per-feature coverage table and linked receipts for the exact boundaries. The package tests use independent guest overlays: conflicting audio stacks were not combined into one claimed working hardware configuration.

The separate P13/P14 follow-up branches also received their required `./test/all` runs. They exited 1 (five and six failing files respectively), with missing sibling source checkouts, file-mode/environment checks and P14's unchanged baseline migration assertion recorded in full. Their changed-area checks passed. Do not substitute the combined guest's passing result for a claim that these standalone runs passed.

## Observed corrections

1. **P11 packages:** the 12-inch audio recipe required stock `linux-headers` even on a system with only the Omarchy kernel. Pacman exited successfully, but its DKMS hook reported a missing stock-kernel modules tree. Release `0.1-2` makes the two kernel-specific header packages optional dependencies, matching the existing CS8409 recipe pattern. Target headers must still be installed. No driver source changed.
2. **P14:** use the existing `omarchy-cmd-present` helper for optional `rtcwake` detection. The diagnostic's original author commit and behavioral limitations remain.
3. **P13:** correct a test that treated reuse of a migration filename for unrelated Mise work as proof that obsolete PTL installation remained. The focused original migration suite now reaches and passes its later cases. No kernel policy behavior changed.
4. **Combined integration only:** reconcile P07's test with P06's removal of the obsolete package. The standalone P07 branch still has its own source context; this combined expectation must not be copied there blindly.
5. **Local ISO tooling:** build actual companion archives, retain their checks, collect real output filenames, replace stale cache entries and verify any reused artifact's source and SHA256. The T1 desktop package's normal `omarchy>=4.0.1` release dependency is unchanged; the local ISO explicitly builds a `0.2.1-1.1` adapter pinned to its exact `omarchy-dev` package version. Its tested desktop compatibility does not establish compatibility with arbitrary runtime versions.
6. **Baseline build input:** the offline repository lacked `apple-bcm-firmware 14.0-1`; the build pins the original maintainer's published archive and release-asset hash. This is a build-input reconciliation, not new T2 hardware behavior.

## Failures and limits that remain

**The overall ISO test run is not fully green.** The existing shared-ESP factory-reset scenario failed: Windows/foreign-Linux menu entries and a foreign machine-ID directory were removed. The reset command is byte-identical to the pinned upstream baseline. Its UKI assertion also uses a filename inconsistent with the fixture's actual `linux-omarchy` filename, so that assertion cannot prove UKI deletion. The test stopped before first boot after the failed preservation checks. This was recorded, not redesigned as part of Mac aggregation.

Build logs also retain an attempted stock-kernel initramfs preset whose `/boot/vmlinuz-linux` is absent from the live image. The build returned zero and the actual Omarchy-kernel installs booted. This warning must not be hidden behind the successful exit code.

P14 retains source defects: failed restore writes can clear saved state; `rtcwake` failure can yield a successful command exit; TERM can restore settings then continue diagnosis and disable them again. The virtual RTC result does not certify its full diagnose/recovery loop.

Previously accepted scope gaps remain: P04 connector/debounce follow-up, P06 manually prepared replacement before retirement, P09 custom-unit/fixed-address limits, P10 customized-hook/retry-state handling, and P12 manual provisioning/no automatic installer. These are still documented in their feature bodies. No physical camera capture, Broadcom association/rebind, speaker safety, Apple NVMe power behavior, SPI PIO reliability, gmux panel handling, fingerprint enrollment, Touch Bar/ALS or physical Mac sleep recovery was established by QEMU.

## Instructions for the next agent

Read the feature's current PR body, source dispositions and coverage row first. Preserve author commits and original PR references. Use the integration source bundles/patches and recorded base commits to reproduce the tested combination; do not infer that separately merging every draft needs no conflict resolution. Keep original failing logs and distinguish harness corrections from product changes.

Run these tests only in disposable VM guests. The original host is a working T1 Mac, not a test target. Do not run candidate hardware setup or migration scripts against it. Physical test reports should name the exact feature/commit, Mac model, device IDs, kernel/header versions and pre-existing configuration. A passing software fixture is not a physical-device report.

Final PR updates are authorized. Basecamp/chat posting, releases and modifications to original source PRs are not part of this handoff. The existing drafts remain drafts.
