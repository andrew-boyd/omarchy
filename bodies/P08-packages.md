# [Intel Mac P08/packages] Consolidate FaceTime PCIe camera packages

Propose the existing facetimehd-dkms, facetimehd-firmware and facetimehd-data recipes as the delivery companion for P08. Preserve the pinned AUR/upstream implementations; only their established packaging/repository adaptations are included. USB/iBridge cameras are outside this package proposal.

**Draft consolidation for source review and hardware-owner follow-up.** Known defects remain; no hardware or merge-readiness certification is claimed. Part of the [14-feature Intel Mac series](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/INTEL-MAC-ROLLUPS.md) with three package companions.

**Contribute:** open follow-up PRs in `andrew-boyd/omarchy-pkgs` with base **`intel-mac/p08-facetime-camera`**. Use `[Intel Mac P08/packages]` in the title and a contributor branch such as `intel-mac/p08/describe-change`. Link this feature in the series index. Merging a follow-up into this branch updates its roll-up.

## Scope and dependencies

Review P08/packages first. Build, approve and make its matching packages available before installer/migration or offline-ISO acceptance. No new ISO PR is planned; ISO delivery remains an integration check.

Paired target: [[Intel Mac P08] Consolidate FaceTime PCIe camera support](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p08-facetime-camera). The feature branch owns Omarchy changes; the package branch owns recipes. Source treatments below describe the pair as a whole. No source is considered fully covered by only one half where both are needed.

## Every reviewed source PR and recommended action

| Source and author | State | Treatment and rationale | Recommended original action |
| --- | --- | --- | --- |
| [omacom/omarchy#11381](https://github.com/omacom/omarchy/pull/11381) — @rand0mdud3 | open | **partial**: Apple DMI gate incorporated. AUR delivery, nonfatal package-failure policy, live module load and second migration remain separate alternatives. | Keep uncovered portions open; consider closure only after author/maintainer agreement on complete coverage. |
| [omacom/omarchy#12067](https://github.com/omacom/omarchy/pull/12067) — @MrBazzieB | open | **incorporated**: Packaged FaceTime PCIe delivery, detector, installer wiring, original migration, manual and tests; exact Apple DMI predicate added from omacom/omarchy#11381. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |

These are recommendations for original authors and maintainers. No original PR is closed, edited or automatically linked for closure. Complete source diffs, pinned heads and authors—including unselected alternatives—are in the [source inventory](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/source-coverage.json).

## Validation and provenance

- Base: `omacom/omarchy-pkgs:master` at `4b60e4cd95972c16fbf3da634522a955cf7bf36c`.
- Prepared commit: `6c1cecc4e49978745ebb57062b83c828b610238f`; tree: `41e8fa815c18dcfddbb458611a3c49b8f68b5fee`.
- [Exact patch](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/patches/P08-packages.patch), SHA-256 `ac24d299ba8e87d641b71ec57cd715b3dd33608d3eec07d431ac89dd67f0a354`. The contribution diff matches the accepted consolidation; the [upstream refresh](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/UPSTREAM-REFRESH.md) advances its base without changing that contribution.
- Available package CI self-tests: **12/12 command groups passed**, including the workflow-approval tests; changed recipe syntax/JSON checks recorded. These ran on this actual tree in a disconnected disposable filesystem.
- Unrun: publish-artifact fixture (`rclone` unavailable), Docker build-isolation job, remote build-pr approval and fresh signed target-kernel delivery. The local subset does not equal passing upstream CI.
- [Check logs and receipts](https://github.com/andrew-boyd/omarchy/tree/intel-mac/review-index/checks) and [focused evidence / hardware checklist](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/evidence/P08/README.md). Observations reproducing defects are not successful hardware behavior. No real module load, firmware write, suspend or host configuration change occurred.
- Tests ran at this rebased commit, `6c1cecc4e49978745ebb57062b83c828b610238f`. The prior commits remain audit evidence; these results belong to the current candidate tree.

## Known gaps and follow-up work

- [ ] PCIe 14e4:1570 cameras are the scope; USB/iBridge cameras are separate. omacom/omarchy#11381's AUR delivery, nonfatal failure policy, live module load and duplicate migration are excluded.
- [ ] Prior private build/DKMS checks used available 7.2.3 headers. Matching Omarchy 7.2.5 headers, signed distribution delivery, real package hooks and ISO availability were not verified.
- [ ] Camera frames, calibration/image quality, reboot, suspend and rollback require hardware. Firmware/calibration source redistribution and delivery require review.

Hardware reports should include the exact commit, model, relevant device/codec IDs, kernel/headers, package/provider versions, existing configuration and reproducible results. Use the feature-specific checklist and recovery preparation in the evidence. Keep author reports distinct from independently reproduced outcomes.

## Attribution

The source table names PR authors. The prepared commit uses **xiota** as Git Author, with native co-author credit for **Harrison, Hugo Osvaldo Barrera**. Source-declared co-author trailers are retained too. Andrew Boyd is the consolidating committer; this does not imply source-author approval or sign-off. See [verified commit attribution](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/AUTHORSHIP.md).

Jev supplied advisory classification; agent work compared sources, consolidated compatible existing contributions, reconciled target collisions and recorded checks. Software observations do not establish hardware support.

Package provenance also credits the pinned AUR/upstream recipes, driver and firmware/data sources; see the P08 recipe/source receipts.
