# Intel Mac inventory correction — completed audit

The project covers 64-bit Intel Macs, including pre-T1, T1 and T2 hardware. MacBookPro13,3 is the first available physical test machine, not an inclusion filter. Neither a VM pass nor a pass on that machine validates other models.

## Why package PR #422 disappeared

The original classifier inventory included omacom/omarchy-pkgs#422 in `wifi-pre-t2-resume`. P10's detailed plan selected a smaller `sources` list without recording an individual disposition for #422. Canonical completion copied that selected list. Publication assembled its tables from another selected list, and `reviews/publication/verify-packet.py` checked those tables against canonical completion, not the original group membership. Its fixed 73-source assertion could pass while inventory sources were missing.

No documented technical rejection or hardware-based exclusion of #422 has been found. This was a selection-to-publication coverage failure. It was not justified by the model available for testing. An older family ledger also explicitly identified missing audio PR #11064, but that warning was not enforced by publication verification.

The original inventory has 163 unique PRs in 74 classifier groups. The groups assigned to the 14 detailed plans contain 69 unique PRs. Thirteen of those were missing from the previously published bodies: three header PRs, two lid/wake PRs, seven Wi-Fi PRs and one audio PR. Other groups were not part of the 14 detailed implementation plans; they must remain visible as unimplemented scope, not be described as consolidated merely because they have been inventoried.

Combining the original inventory, expanded family ledger and published source tables yields 182 previously known sources. A fresh paginated read completed without collection errors. Six additional sources from discovery and explicit successor links bring the current registry to 188. All 188 now have dispositions: 101 appear in feature tables, and 87 remain only in separate work tracks. All 69 sources from the original groups assigned to P01–P14 are covered in their relevant tables. This is a dated, bounded discovery result, not proof of exhaustive GitHub coverage or 188 implemented PRs.

## Current upstream changes

Compared with the most recent saved source snapshots, 17 PRs changed from open to closed; two heads changed, with one of those also closing. Most closures include upstream automated similarity comments. Preserve the actual source differences and hardware reports: an administrative closure does not prove equivalent coverage or authorize dropping attribution. Source PRs remain untouched by this effort.

Omarchy's target is `quattro`, not the branch named `main`. The first refresh found 33 new Omarchy commits and 23 package commits, including merges; the ISO target was unchanged. All 17 existing draft branches and the integrated source trees are now reconciled locally. Original published commits remain ancestors; only two obsolete test assertions required merge resolution. Exact refs, merge previews and prepared branch heads are adjacent JSON receipts. The reconciled combined image has completed fresh installation and required software checks; branch-versus-combined differences remain explicit. The later prebuild check also reconciled three additional Hype package commits.

## Findings affecting decisions

- #422 is a distinct BCM43602 kernel cold-resume alternative, scoped to Apple subsystem 106b:0133, with author-reported MacBookPro12,1 tests. Its patch/config hashes match the current recipe; the linked review comment's SKIP concern does not match those current entries. Kernel review and independent hardware validation remain outstanding. It must be referenced by P10 and kernel-policy coordination, without claiming it is in the ISO or stacking it with a sleep recovery hook.
- P10's selected #12314 used broad T2/chip detection copied from a supplicant workaround. Omitted #7333 explicitly excludes T2 chips, and #11536 reports a BCM4377 combo-device failure requiring different ordering and delayed reload. The local P10 correction takes #7333's existing BCM4350/BCM43602 four-ID boundary, with native source-author credit; it does not invent a T2 recovery sequence. Its revised source checks passed in a disposable B7 guest. This fresh-install candidate does not automatically remove a broader hook already installed on a T2 machine by an older trial; that prior-install transition remains a documented manual reconciliation boundary.
- P04's omitted #9637 concerns the lid-open brightness path on MacBook10,1; #9211 concerns lock wake/input on MacBookPro16,1. Both remain relevant even though neither is the first physical test model.
- P11's missing #11064 includes a reported MacBookPro13,2 speaker test and a distinct model/package selection. Preserve that evidence and explain the selected packaged alternative; do not copy its claimed codec exclusions without reconciliation.

## Completed local preparation

- Corrected all 17 draft bodies locally, with every affected source's state, author, disposition and recommended action. Publication is gated on the completed fresh-image receipts and an immediate live-PR preflight.
- Added an independent original-group coverage gate to publication. Removing #422 or its P10 disposition is now rejected; the old incomplete packet also fails. Portable public-source snapshots and a 52-result discovery-screening ledger accompany the audit.
- Included both source-authored ISO #174 commits with attribution. Its nine EFI-preservation unit tests passed in a disposable guest. A fresh disk-wipe/reinstall preserved all three synthetic EFI files byte-for-byte, wiped an unrelated marker, and left the seed unchanged; no real firmware was used.
- Corrected the demonstrated baseline Neovim plugin reference in the package source, pinned its replacement commit and added strict startup/theme checks. The rebuilt package and fresh installed guest pass strict startup and explicit Monokai theme checks.
- Prepared a [physical installation/recovery guide](HARDWARE-INSTALL.md), [cross-model validation matrix](HARDWARE-MATRIX.md), ISO-content verifier and fresh-image VM runners. The first physical trial remains a separate, attended step.

## Validation outcome and retained failures

The new ISO passed content verification for all 13 local packages, 74 changed runtime files and both Apple EFI source files. Fresh unattended EFI-preservation, unencrypted and encrypted installs passed. Both interactive installs passed all eight desktop acceptance files. All four camera/audio/T1 package scenarios, SPI-PIO and retained-kernel/header migrations, and virtual non-Apple NVMe exclusion passed. The combined source suite completed 273 files without failures, with two explicit skips; the ISO unit suite passed 78 tests.

The first build attempt failed one libfprint USB replay test. Three isolated repeats, two complete serial suites and the normal package check passed without driver/test changes; that failure's cause remains unestablished. The full source suite also provoked repeated NetworkManager Polkit failures and a recorded PAM account lockout. The subsequent installed password/desktop/recovery checks failed there and passed in a clean overlay of the same image. The original aggregate remains failed. See `build-reuse.json`, `runtime-rechecks.json` and `final-validation.json` rather than interpreting a passing subset as a green original run.

The prior B7 ISO is historical evidence. The current image, exact sources, reproduction, retained limitations and physical-trial instructions are in `HANDOFF.md`. Existing-draft publication is tracked separately in `published-pr-updates.json`; no original source PR, Basecamp/chat thread or physical installation is changed by this preparation.
