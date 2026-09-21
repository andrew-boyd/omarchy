# Reproduce the inventory audit and integrated test candidate

Start with [HANDOFF.md](HANDOFF.md) for the exact ISO, source commits and observed results. A source reconstruction is not a fresh build or a hardware pass. The ISO checksum identifies the actual tested artifact; rebuilding later can resolve different distribution packages. This is not a claim of bit-for-bit reproducible builds.

## Independent inventory coverage

Check out `intel-mac/review-index` from `andrew-boyd/omarchy`. Its review workspace contains the original grouping, expanded ledger, previous publication index, additional intake, all 188 public source snapshots, corrected dispositions and the 17 prepared PR bodies. No credentials or ignored local state are needed for this check:

```bash
cd hardware-test/review-workspace
python reviews/hardware-test/verify-inventory.py \
  --negative-controls \
  --prepared-prs reviews/hardware-test/prepared-pr-updates.json
```

Both negative controls must be rejected: deleting package PR #422, and retaining it without its required P10 disposition. The source union and each plan's required members are derived from the original inventories. Matching a previously narrowed source list is insufficient.

The source registry distinguishes selected contributions, alternatives, context and deferred work. Its 188 entries are not 188 implemented PRs. The original PRs remain unchanged by this initiative.

## Reconstruct the exact integration sources

`integration/sources.json` records three upstream bases, built commits, trees and SHA-256 hashes. Each Git bundle preserves contribution history and author/co-author metadata. Each aggregate patch is independently verified to reconstruct the same tree but is not a substitute for that history.

For each of `omarchy`, `omarchy-pkgs` and `omarchy-iso`, clone its `omacom` repository into a new dedicated directory, check out the recorded base, then fetch the corresponding bundle:

```bash
# Substitute the repository, base and absolute bundle path from sources.json.
git checkout --detach <recorded-base>
git bundle verify /absolute/path/to/hardware-test/integration/<repository>.bundle
git fetch /absolute/path/to/hardware-test/integration/<repository>.bundle HEAD
git checkout --detach FETCH_HEAD
git rev-parse HEAD HEAD^{tree}
```

Both printed hashes must match `sources.json`. For the ISO repository, initialize its pinned `archiso` submodule with `git submodule update --init --recursive`. Use the repository's documented Docker/QEMU dependencies. Keep sources and build caches separate from a live desktop installation.

Run the reconstructed ISO builder with `--local-source` pointing at the reconstructed runtime and package repositories. The recorded launch uses `--detach --keep-pkg-cache --no-boot-offer --debug` and the stable mirror. The historical build used dedicated task caches and a verified package-reuse receipt; a new environment should build and run package checks normally. Do not copy the old reuse receipt without its exact archives and matching source commits. A failed package or test must stop the build.

The runtime, package and ISO source commits are pinned. Resolved archive hashes are in `build/package-sha256sums`; `receipts/artifact.json` verifies the 13 embedded local packages, changed runtime payloads, Apple EFI source files, Neovim plugin pin and reconciled desktop dependency versions. Preserve these distinctions when comparing a later rebuild.

## VM test contract

The public logs under `stages/` and `vm-runs/` record the actual commands and results. The audit tools under `review-workspace/reviews/hardware-test/` document the local runner. Its absolute historical paths identify this run and must be adapted deliberately for another machine.

The required checks are:

1. Verify the ISO itself and its installed runtime hashes against the pinned source and archive receipts.
2. Install fresh over a synthetic virtual EFI partition. Check all three synthetic files by SHA-256 after the destructive installer path, require an unrelated old marker to be gone, and verify the seed is unchanged behind its QCOW2 overlay. `prepare-efi-seed.sh` constructs this fixture in an already-installed disposable guest; it contains no real Apple firmware.
3. Run the combined source suite, installed virtual monitor/keyboard checks, wrong-password/correct-password lock test, strict Neovim startup and explicit Monokai load, root-state/retry checks and virtual RTC sleep/resume inside the new guest.
4. Run separate fresh unencrypted and encrypted interactive installs with the desktop acceptance suite.
5. In separate overlays, install the actual camera, two mutually exclusive audio tracks and T1 packages; require matching-kernel DKMS and reboot. Exercise prepared legacy SPI removal, SPI-PIO and retained-kernel header migrations, and non-Apple virtual NVMe exclusion.

Keep every functional test inside a disposable VM or build container. Do not run the source suites or package/migration commands against the live host. Model files, virtual controllers and synthetic firmware are explicit fixtures; none validates Apple hardware.

For subsequent runs, use separate overlays for the full source suite and installed password/desktop/recovery checks. The recorded combined invocation passed the source suite but its NetworkManager Polkit requests triggered a PAM account lockout before those installed checks. `run-runtime-rechecks.sh` exercises the affected checks in a fresh overlay; the preserved failed guest's journal and unchanged-password comparison establish why the original result remains failed. Do not disable or reset authentication policy to manufacture a pass. The original runners and logs remain available as executed; the recheck does not claim the shared-suite isolation problem was repaired.

The recorded test-only OCR whitespace patch does not change the product. The host package helper is replaced by a read-only dependency query during the desktop test harness; missing host prerequisites stop the run. Do not replace a failed aggregate result with a passing subset. Preserve any failure and identify exactly what a separate recheck establishes.

## Physical trial

Use [HARDWARE-INSTALL.md](HARDWARE-INSTALL.md) and [HARDWARE-MATRIX.md](HARDWARE-MATRIX.md). The first available MacBookPro13,3 is one test target within the wider Intel Mac effort. Keep independent data/EFI backups, password fallback and local recovery access. The selected T1Bridge release's documented suspend/resume limitation remains unresolved. No USB flashing or physical installation was performed during this preparation.
