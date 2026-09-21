# [Intel Mac P08/packages] Consolidate FaceTime PCIe camera packages

Propose the existing facetimehd-dkms, facetimehd-firmware and facetimehd-data recipes as the delivery companion for P08. Preserve the pinned AUR/upstream implementations; only their established packaging/repository adaptations are included. USB/iBridge cameras are outside this package proposal.

**Draft consolidation for source review and hardware-owner follow-up.** Known defects remain; no hardware or merge-readiness certification is claimed. Part of the [14-feature Intel Mac series](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/INTEL-MAC-ROLLUPS.md) with three package companions.

**Contribute:** open follow-up PRs in `andrew-boyd/omarchy-pkgs` with base **`intel-mac/p08-facetime-camera`**. Use `[Intel Mac P08/packages]` in the title and a contributor branch such as `intel-mac/p08/describe-change`. Link this feature in the series index. Merging a follow-up into this branch updates its roll-up.

## Published series

This draft: [omacom/omarchy-pkgs#556](https://github.com/omacom/omarchy-pkgs/pull/556). [All feature and package drafts](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/INTEL-MAC-ROLLUPS.md).

Feature draft: [omacom/omarchy#12686](https://github.com/omacom/omarchy/pull/12686). Keep the merge/setup dependencies below.

## Rebuilt ISO and software follow-up — 2026-09-21 UTC

Current draft head: `6c1cecc4e49978745ebb57062b83c828b610238f`. Original contribution commits and attribution are preserved.

The repaired combined ISO built and completed fresh unencrypted and encrypted installation/reboot checks. All 13 embedded local package archives and 52 changed runtime payloads were verified against the pinned source. Clean desktop acceptance reruns passed all eight files. The original interrupted/failed harness runs remain in the report; focused reruns are not relabeled as green original aggregates.

**The ISO is not entirely green:** the stricter editor-startup check still fails because the unchanged baseline Neovim package requests an unavailable theme repository. A guest-only replacement-source experiment passed, but that repair is not in this ISO or these feature branches. The earlier acceptance suite did not catch that error.

- **This branch:** no additional runtime changes in this remediation. Earlier per-feature checks remain dated evidence; inclusion in the new combined ISO does not silently repeat every earlier hardware-specific scenario.
- **Combined baseline:** shared-ESP factory reset now passes staging, unattended first boot and provisioning while preserving foreign entries/files. An older unsafe factory snapshot is refused. These baseline repairs are supplied in the integration evidence, not inserted into unrelated feature branches.
- **Boundary:** physical Intel Mac behavior and signed distribution delivery remain unverified. DMI/device input fixtures and virtual RTC/NVMe checks do not emulate Apple hardware.

[Current handoff](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-remediation/HANDOFF.md) · [Exact test/artifact receipts](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-remediation/receipts/results.json) · [Reproduction](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-remediation/REPRODUCE.md) · [Pinned source bundles](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-remediation/integration/sources.json).

<details>
<summary>Earlier ISO/VM validation, before these software repairs</summary>

## ISO / VM validation — 2026-09-21 UTC

Tested as part of the combined 14-feature custom ISO. Fresh encrypted and unencrypted installs booted; the final rebuilt ISO passed all eight desktop acceptance files with the documented test-only OCR correction. The combined live-guest CLI suite and 267 shell files passed, including focused rechecks.

- **This feature:** All three exact camera archives installed from the ISO; facetimehd/0.7.2 built against 7.2.5-4-omarchy, reboot passed, and PAM files were unchanged. Actual nonmatching PCI detection and calibration/model fixtures passed.
- **Hardware boundary:** Camera streaming and calibration require the Broadcom camera. Accepted source gaps below remain.
- **Overall limits:** the unchanged-baseline shared-ESP factory-reset test failed; the report retains it and the harness interventions. This remains a draft, not release/hardware certification.

[Results and limits](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/HANDOFF.md) · [Feature coverage](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/COVERAGE.md) · [Exact sources and reproduction](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/REPRODUCE.md) · [Final artifact receipt](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/receipts/final-validation.json).


</details>

## Scope and dependencies

Review P08/packages first. Build, approve and make its matching packages available before installer/migration or offline-ISO acceptance. No new ISO PR is planned; ISO delivery remains an integration check.

Paired target: [[Intel Mac P08] Consolidate FaceTime PCIe camera support](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p08-facetime-camera). The feature branch owns Omarchy changes; the package branch owns recipes. Source treatments below describe the pair as a whole. No source is considered fully covered by only one half where both are needed.

## Every reviewed source PR and recommended action

| Source and author | State | Treatment and rationale | Recommended original action |
| --- | --- | --- | --- |
| [omacom/omarchy#11381](https://github.com/omacom/omarchy/pull/11381) — @rand0mdud3 | open | **partial**: Apple DMI gate incorporated. AUR delivery, nonfatal package-failure policy, live module load and second migration remain separate alternatives. | Keep uncovered portions open; consider closure only after author/maintainer agreement on complete coverage. |
| [omacom/omarchy#12067](https://github.com/omacom/omarchy/pull/12067) — @MrBazzieB | open | **incorporated**: Packaged FaceTime PCIe delivery, detector, installer wiring, original migration, manual and tests; exact Apple DMI predicate added from omacom/omarchy#11381. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |

These are recommendations for original authors and maintainers. No original PR is closed, edited or automatically linked for closure. Complete source diffs, pinned heads and authors—including unselected alternatives—are in the [source inventory](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/source-coverage.json).

<details>
<summary>Original pre-VM publication checks and provenance</summary>

## Original publication checks (historical)

- Base: `omacom/omarchy-pkgs:master` at `4b60e4cd95972c16fbf3da634522a955cf7bf36c`.
- Prepared commit: `6c1cecc4e49978745ebb57062b83c828b610238f`; tree: `41e8fa815c18dcfddbb458611a3c49b8f68b5fee`.
- [Exact patch](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/patches/P08-packages.patch), SHA-256 `ac24d299ba8e87d641b71ec57cd715b3dd33608d3eec07d431ac89dd67f0a354`. The contribution diff matches the accepted consolidation; the [upstream refresh](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/UPSTREAM-REFRESH.md) advances its base without changing that contribution.
- Available package CI self-tests: **12/12 command groups passed**, including the workflow-approval tests; changed recipe syntax/JSON checks recorded. These ran on this actual tree in a disconnected disposable filesystem.
- Unrun: publish-artifact fixture (`rclone` unavailable), Docker build-isolation job, remote build-pr approval and fresh signed target-kernel delivery. The local subset does not equal passing upstream CI.
- [Check logs and receipts](https://github.com/andrew-boyd/omarchy/tree/intel-mac/review-index/checks) and [focused evidence / hardware checklist](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/evidence/P08/README.md). Observations reproducing defects are not successful hardware behavior. No real module load, firmware write, suspend or host configuration change occurred.
- Tests ran at this rebased commit, `6c1cecc4e49978745ebb57062b83c828b610238f`. The prior commits remain audit evidence; these results belong to that original publication tree, before the VM follow-up.


</details>

## Known gaps and follow-up work

- [ ] PCIe 14e4:1570 cameras are the scope; USB/iBridge cameras are separate. omacom/omarchy#11381’s AUR delivery, nonfatal failure policy, live module load and duplicate migration remain excluded.
- [ ] Matching Omarchy 7.2.5-4 headers, real package hooks/DKMS and local ISO inclusion were verified in the earlier pinned VM artifact. Signed distribution delivery remains unverified.
- [ ] Camera frames, calibration/image quality, physical reboot/suspend and rollback require hardware. Firmware/calibration source redistribution and delivery need review.

Hardware reports should include the exact commit, model, relevant device/codec IDs, kernel/headers, package/provider versions, existing configuration and reproducible results. Use the feature-specific checklist and recovery preparation in the evidence. Keep author reports distinct from independently reproduced outcomes.

## Attribution

The source table names PR authors. The prepared commit uses **xiota** as Git Author, with native co-author credit for **Harrison, Hugo Osvaldo Barrera**. Source-declared co-author trailers are retained too. Andrew Boyd is the consolidating committer; this does not imply source-author approval or sign-off. See [verified commit attribution](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/AUTHORSHIP.md).

Jev supplied advisory classification; agent work compared sources, consolidated compatible existing contributions, reconciled target collisions and recorded checks. Software observations do not establish hardware support.

Package provenance also credits the pinned AUR/upstream recipes, driver and firmware/data sources; see the P08 recipe/source receipts.

Software repairs and test-harness corrections are subsequent agent-assisted commits by the consolidating contributor; original author credit does not imply approval of those follow-ups.
