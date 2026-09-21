# Resume the reconciled hardware-test candidate

The pinned candidate is ready for an attended hardware trial. Read `STATUS.json`, `final-validation.json` and `runtime-rechecks.json`: required checks are satisfied, while original failed build/runtime results remain preserved. Publication status is recorded separately.

## Coverage and source receipts

- `source-registry.json` and `source-snapshots/`: all 188 known/intake PRs, pinned heads, fresh discussion snapshots and dispositions. `INVENTORY.md` distinguishes feature tables from unimplemented separate work tracks.
- `coverage-audit.json`: the 13 missing references and original assigned-group coverage. `verify-inventory.py` derives required members from the original grouping, not a narrowed selected list.
- `discovery-screening.json`: decisions for all 52 distinct results returned by the dated discovery queries. It is not an exhaustive-search claim.
- `branch-preparation.json`: all 17 existing draft heads, reconciled upstream and published-history ancestry. `integration-coverage.json` compares every changed production file with the combined source and retains the full diff for each intentional difference.
- `source-preflight.json`: revised Broadcom source checks and nine EFI unit tests inside a disposable guest installed from B7. These are **not** tests of a newly built ISO.

From the review repository:

```bash
python reviews/hardware-test/verify-inventory.py --negative-controls --prepared-prs reviews/hardware-test/prepared-pr-updates.json
python reviews/hardware-test/verify-integration-coverage.py
```

The old B7 artifact and its results remain dated evidence. Do not relabel that ISO as the revised candidate. The updated ISO source also carries the existing Apple EFI preservation commits and a test-only option for a synthetic initial virtual disk; neither touches physical storage during preparation.

## Build and fresh-image validation

The integration repositories are under `.state/vm-install/2026-09-20/repos/`, on `hardware-test/2026-09-21`. `STATUS.json` records the current exact commits and immutable prepared snapshot. Check clean trees and source freshness before launching. A new upstream change needs an explicit decision and updated pin; it does not silently change a running build.

The existing helper may be run by the user through interactive sudo to renew the four-hour Docker-only grant. Do not renew it unattended or use another privilege mechanism to bypass the expired grant.

```bash
bash reviews/vm-install/start-build.sh
```

The launcher creates fresh immutable source clones and starts Docker detached. Confirm the actual container/process before waiting; a directory or incomplete log is not proof a build is still running. After `latest-build/build.exit` is `0`, invoke:

```bash
python reviews/hardware-test/run-validation.py .state/vm-install/2026-09-20/latest-build
```

Run this long validation command under a named user service or equivalent detached process if the terminal may disconnect. Do not restart it solely because observation times out; inspect its process and per-stage logs first. It preserves stage exit codes under the build's `hardware-validation/` and refuses to overwrite completed stages.

The runner verifies the embedded local archives and changed production payloads, both EFI-preservation source files, and the corrected/pinned Neovim plugin. It then installs onto a synthetic pre-existing EFI disk, verifies every synthetic firmware file by SHA-256 and checks the unrelated old marker was wiped. The seed remains unchanged behind a QCOW2 overlay. Its synthetic bytes are **not Apple firmware**.

Further stages run the combined CLI/shell suite, installed payload checks, password lock/unlock, virtual monitor/keyboard behavior, strict Neovim startup and explicit theme load, privileged recovery/virtual RTC checks, and ISO Python unit tests inside a disposable guest. Fresh unencrypted and encrypted interactive installations each run the desktop acceptance suite. The host dependency helper is replaced only for those harness invocations by `pacman -Q`; missing host prerequisites stop the harness rather than trigger package installation.

Separate fresh overlays repeat camera, both conflicting audio tracks, and T1 package installation/DKMS/reboot checks; T1 also exercises password fallback and the legacy-SPI removal transaction. SPI-PIO and kernel/header migration checks and exclusion of a real virtual non-Apple NVMe controller are repeated against this image. Model inputs are fixtures, not physical hardware tests. Archive hashes and installed payload checks use this build's receipts, never a previous image's manifest.

The test-only OCR patch is copied with its SHA-256 into the validation receipt. It normalizes screenshot OCR whitespace and retries native resolution; it does not alter the product. The current source already includes the earlier SIGPIPE test correction and spare-console harness fix: **do not apply those old patches again**. Every functional test runs in a VM. Do not execute the complete source suites against the live Mac desktop.

If a stage fails, preserve its result. Diagnose it, create a separately named recheck, and record exactly which failures it covers. A zero wrapper exit or passing subset does not turn an earlier aggregate failure into a pass. Inspect the generated desktop screenshots in addition to reading test output, especially the reconciled lock and display surfaces.

The current candidate's source suite passed 273 files with two skips but triggered a PAM lockout through repeated NetworkManager Polkit requests. Its subsequent installed checks failed; all three passed in a separate clean overlay. `runtime-rechecks.json` and `inspect-failed-runtime.sh` preserve the diagnosis and unchanged-password check. In future runs, keep the full suite and installed authentication/desktop checks in separate overlays. The historical runner is retained as executed; do not disable authentication policy or silently change its failed aggregate result.

## Final publication and physical handoff

Only after the final build/VM gates pass should the prepared PR bodies lose their pending banner. Re-read upstream refs and the 17 existing drafts, preserve any intervening edits, and verify all required source references again. Push only fast-forward changes to the existing feature/package branches and the existing review-index evidence branch. Update those same PR bodies; do not modify original source PRs, open extra PRs or post to Basecamp/chat.

The public evidence packet must identify the final ISO hash, all three integrated source commits, exact installed package versions, test/harness revisions, raw pass/failure results, retained hardware limitations and branch-versus-combined differences. Include reconstructable source history with author/co-author metadata; patches alone do not preserve commit credit. Exclude VM disks, SSH keys, real firmware, private host captures and credentials.

Finish `HARDWARE-INSTALL.md` and stage the exact verified ISO/checksum for the first MacBookPro13,3 trial. Keep `HARDWARE-MATRIX.md` and every other Intel Mac work track visible. Do not flash media or install hardware during this preparation goal.
