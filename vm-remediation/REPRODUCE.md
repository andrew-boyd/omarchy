# Reproduce the software-remediation checks

This follow-up retains the original feature contributions and appends software repairs. It does not add model quirks or certify physical Mac behavior. The older `vm-validation/` packet remains historical evidence; the new source/artifact receipts identify the repaired candidate.

## Exact source reconstruction

`integration/sources.json` identifies each pinned base, tested commit, tree hash, Git bundle and aggregate patch. In a full clone of the corresponding upstream repository, fetch the bundle and check out its tested commit:

```bash
git fetch /absolute/path/to/vm-remediation/integration/omarchy.bundle HEAD
git checkout --detach <tested_commit_from_sources.json>
```

Repeat for `omarchy-pkgs` and `omarchy-iso`, then initialize the ISO's archiso submodule at `424e78130db2af6c1ceb55b442d7914b1109ff2b`. Full history is needed for equivalent package revision generation. The bundles retain contribution authors and commits; the aggregate patches reproduce trees but do not preserve commit attribution by themselves. Every bundle and patch was independently checked from its pinned base.

The named feature branches also retain their original author commits. Their follow-up patches are in `followups/`; production comparison against the combined source records the two deliberate differences: standalone P07 still installs its baseline legacy package until combined with P06, and the published T1 desktop recipe keeps its stable dependency instead of the combined ISO's exact local-dev dependency adapter.

## Build, install and desktop acceptance

Use the ISO repository's documented build dependencies and local-source command. A normal interactive Docker sudo invocation suffices; the original machine's temporary permission rule is not a prerequisite.

```bash
umask 022
./bin/omarchy-iso-make --no-boot-offer --local-source ../omarchy ../omarchy-pkgs
```

Use a hardlink whose name contains `local` for the generated ISO; the test harness uses this name to select the local runtime package. A symlink is resolved and loses the distinction. Preserve the ISO SHA256, build log/exit and all local package hashes. Source hashes do not promise byte-identical rebuilds while external package/plugin repositories move.

Apply `integration/acceptance-tty4.patch` to a separate harness copy. It selects among spare consoles and confirms an actual login prompt before entering credentials; a fixed console can hold the graphical greeter. It changes no ISO payload. Copy only the Omarchy `test/` directory to a test-sync folder and apply the supplied OCR whitespace/native-resolution correction there. Run the real installer without reusing an old base:

```bash
./bin/omarchy-iso-test /absolute/path/to/intel-mac-local.iso --sync-omarchy /absolute/path/to/test-sync --no-preview
./test/integration /absolute/path/to/intel-mac-local.iso --no-preview
```

The second command performs a fresh unattended install and runs the shared-ESP reset scenario through provisioning. The repaired reset deliberately refuses an old factory snapshot whose saved provisioner would erase foreign entries. Installing a new reset command into the running system does not update that immutable snapshot. The separate old-snapshot test uses a disposable overlay and verifies refusal without account, identity or ESP changes.

## Source suites and real guest operations

Run complete source suites in disposable guests. Preserve the first aggregate run; when rechecking observed GUI failures, use a new overlay per failed file to exclude state left by earlier tests. Apply `preinstalls-sigpipe.patch` only to the copied test suite: it repairs a reproduced assertion pipeline race and changes no ISO payload. A source suite inherited real XDG paths during an earlier host run; the accidental config and route move were restored, and that fixture now isolates XDG paths explicitly. Do not run these full suites against an agent's working desktop.

The supplied runners use this original layout, which can be adjusted to another checkout deliberately:

```text
reviews/vm-install/                 shared original guest helpers
reviews/remediation/               new inspection and guest runners
.state/vm-install/2026-09-20/
  builds/<build>/sources/{omarchy,omarchy-pkgs,omarchy-iso}
  remediation/branches/<feature>
```

Every guest mutation first checks the synthetic hostname `omarchy-test`, KVM virtualization and `/dev/vda`. The synthetic guest account/password are `omarchy`/`omarchy`; no real credentials or SSH private keys are part of the evidence. QEMU does not emulate T1/T2, gmux, physical Apple audio, camera, SPI input or real Broadcom Wi-Fi.

- `run-branch-suites.sh`: full CLI/shell suite for each repaired feature branch, with matching sibling sources, in an isolated guest.
- `inspect-artifact.py`: reads the ISO itself, verifies all 13 embedded local archives against the build receipt and compares changed runtime payloads with the pinned source. Its original layout uses an extracted `unsquashfs` binary from the cached Arch package; a normally installed `unsquashfs` can be substituted.
- `run-runtime-checks.sh`: verifies installed payload hashes, runs the full source and desktop checks, and exercises the actual privileged P14 state directory, lock, failed restore/retry and virtual RTC sleep. USB attribute fixtures are explicitly synthetic.
- `run-package-scenario.sh`: actual companion package transactions, target-kernel DKMS and reboot. The CS8409 case enters through the installed positive hardware leaf using an explicit DMI fixture and checks that no unrelated stock kernel/headers were installed. The T1 case tests the installed desktop provider/password fallback and actual SPI retirement with replacement packages and native modules present.
- `run-migration-scenario.sh` and `run-nvme-scenario.sh`: real initramfs/boot operations with an explicit model fixture, and a real virtual non-Apple NVMe controller at the selected PCI address. These establish software behavior, not hardware applicability.
- `run-old-snapshot-guard.sh`: refusal of an older unsafe factory snapshot using a disposable overlay of the earlier ISO.
- `run-runtime-followups.sh`: repeats the installed desktop and privileged recovery checks in a fresh guest, then records the original editor failure separately from a guest-only source-replacement experiment. The full source suite left the first guest locked and unable to authenticate sudo; those follow-up operations had not reached their intended checks. The rebuilt ISO still contains the broken baseline editor source, so the passing experiment is not an ISO pass.

The first failed-file recheck loop let an SSH child consume the remaining stdin list. Its zero wrapper exit covered only the integration smoke file. The corrected runner disconnects child stdin; the five missing P07/P10 files are recorded individually in fresh overlays. Recheck coverage is validated against the original failed-file lists before preparing PR bodies.

Keep original failures, harness interventions and focused reruns. A passing subset must not be presented as a green aggregate suite. Signed distribution delivery, actual hardware acceptance and the retained source-policy gaps remain separate work.
