# [Intel Mac P11/packages] Consolidate model-specific Cirrus audio packages

Combine the unchanged omacom/omarchy-pkgs#249 snd-hda-macbookpro-dkms and omacom/omarchy-pkgs#153 macbook12-audio-driver-dkms recipes for P11's distinct model tracks. The packages conflict on one machine; this is not an instruction to install both. The iMac CS4208 configuration uses the in-tree driver and needs no third package.

**Draft consolidation for source review and hardware-owner follow-up.** Known defects remain; no hardware or merge-readiness certification is claimed. Part of the [14-feature Intel Mac series](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/INTEL-MAC-ROLLUPS.md) with three package companions.

**Contribute:** open follow-up PRs in `andrew-boyd/omarchy-pkgs` with base **`intel-mac/p11-cirrus-audio`**. Use `[Intel Mac P11/packages]` in the title and a contributor branch such as `intel-mac/p11/describe-change`. Link this feature in the series index. Merging a follow-up into this branch updates its roll-up.

## Scope and dependencies

Review P11/packages first; publish the appropriate package before its model-specific installer/migration trial. Do not install both conflicting audio packages together. The iMac in-tree track has no package prerequisite.

Paired target: [[Intel Mac P11] Consolidate model-specific Cirrus audio support](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p11-cirrus-audio). The feature branch owns Omarchy changes; the package branch owns recipes. Source treatments below describe the pair as a whole. No source is considered fully covered by only one half where both are needed.

## Every reviewed source PR and recommended action

| Source and author | State | Treatment and rationale | Recommended original action |
| --- | --- | --- | --- |
| [omacom/omarchy#10458](https://github.com/omacom/omarchy/pull/10458) — @inspiretelapps | open | **incorporated**: Complete iMac CS4208 configuration using the in-tree codec; inherited overwrite/route-reset/failure behavior retained. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [omacom/omarchy#11625](https://github.com/omacom/omarchy/pull/11625) — @andyholst | open | **alternative**: Unpinned direct-clone CS8409 delivery with differing installer/migration gates. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#12286](https://github.com/omacom/omarchy/pull/12286) — @teomurgi | open | **alternative**: Complete conflicting MacBook proposal includes automatic EFI writes and freeze sleep policy; preserve separately. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#6921](https://github.com/omacom/omarchy/pull/6921) — @sunoxen-lab | open | **incorporated**: MacBook CS4208 baseline combined with the existing linked mixer/current-kernel upgrade contribution; uses package omacom/omarchy-pkgs#153. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [omacom/omarchy#7140](https://github.com/omacom/omarchy/pull/7140) — @shawnyeager | open | **predecessor**: CS8409 predecessor credited through omacom/omarchy#9516; narrower model coverage retained as comparison. | Credit the successor; recommend closure after maintainers accept the represented scope. |
| [omacom/omarchy#8285](https://github.com/omacom/omarchy/pull/8285) — @jack-lech | open | **alternative**: Different CS8409 -git package name and installer/cache ownership; not stacked. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#9516](https://github.com/omacom/omarchy/pull/9516) — @j7j7 | open | **incorporated**: Selected complete CS8409 installer; paired with package omacom/omarchy-pkgs#249 and original model/header policy. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [omacom/omarchy-pkgs#153](https://github.com/omacom/omarchy-pkgs/pull/153) — @doctor | open | **incorporated**: Selected unchanged MacBook CS4208 package recipe. The two audio packages serve separate model paths and conflict on one machine. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [omacom/omarchy-pkgs#155](https://github.com/omacom/omarchy-pkgs/pull/155) — @shawnyeager | open | **predecessor**: CS8409 package predecessor credited through omacom/omarchy-pkgs#249; preserved independently, not an additional companion PR. | Credit the successor; recommend closure after maintainers accept the represented scope. |
| [omacom/omarchy-pkgs#249](https://github.com/omacom/omarchy-pkgs/pull/249) — @j7j7 | open | **incorporated**: Selected unchanged CS8409 package recipe; package companion combines it with omacom/omarchy-pkgs#153. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [sunoxen-lab/omarchy#1](https://github.com/sunoxen-lab/omarchy/pull/1) — @doctor | open | **partial**: Existing mixer/service/current-kernel upgrade work included. Its separate s2idle proposal is retained as an unselected alternative. | Keep uncovered portions open; consider closure only after author/maintainer agreement on complete coverage. |
| [leifliddy/macbook12-audio-driver#60](https://github.com/leifliddy/macbook12-audio-driver/pull/60) — @doctor | merged | **context**: Merged driver preparation/DKMS changes underpin package omacom/omarchy-pkgs#153. Its preparation files match, while the older pinned Makefiles differ; the package does not contain every change in this driver PR. | Already merged; retain attribution and context. No action proposed. |

These are recommendations for original authors and maintainers. No original PR is closed, edited or automatically linked for closure. Complete source diffs, pinned heads and authors—including unselected alternatives—are in the [source inventory](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/source-coverage.json).

## Validation and provenance

- Base: `omacom/omarchy-pkgs:master` at `bda2a070f4641fd44e5d02bd9cbf7da3fce4e345`.
- Prepared commit: `65c17cb1a24626945c273e55ab9a0d1698fdcff9`; tree: `6d084ddd8be492d394135e050e046c1a5a98c39e`.
- [Exact patch](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/patches/P11-packages.patch), SHA-256 `f5584a507810d4fb66a0ae327fd53faa1343699c7963aafc0f859c3700f51050`. The candidate tree matches the already-reviewed consolidation; publication preparation changes no implementation.
- Available package CI self-tests: **10/10 command groups passed**, including the workflow-approval tests; changed recipe syntax/JSON checks recorded. These ran on this actual tree in a disconnected disposable filesystem.
- Unrun: publish-artifact fixture (`rclone` unavailable), Docker build-isolation job, remote build-pr approval and fresh signed target-kernel delivery. The local subset does not equal passing upstream CI.
- [Check logs and receipts](https://github.com/andrew-boyd/omarchy/tree/intel-mac/review-index/checks) and [focused evidence / hardware checklist](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/evidence/P11/README.md). Observations reproducing defects are not successful hardware behavior. No real module load, firmware write, suspend or host configuration change occurred.
- Tests ran at `bd6bc96b69a9eb793ef651ac81f52d344054b4ea`. Results are reused for this identical tree after an authorship-only metadata correction; no new code or test result is implied.

## Known gaps and follow-up work

- [ ] The two DKMS audio packages conflict on one machine. The iMac CS4208 track needs no new DKMS package. Existing model gates are retained; the CS8409 regex is unanchored and can match unsupported suffixes.
- [ ] The MacBook follow-up's s2idle policy and omacom/omarchy#12286's freeze/EFI policy are both excluded. Contradictory sleep reports remain separate; no EFI changes are included.
- [ ] iMac setup replaces same-name rules and saved routes, tolerates mixer errors, and can fail after configuration changes. Preserve custom configuration before any trial.
- [ ] Original omacom/omarchy#6921 migration contents are retained under 1789869577.sh because its original name collides with an unrelated target migration; only matching test references were adjusted.
- [ ] Prior original-recipe DKMS builds passed on 7.2.3, with qualified download/fakeroot harness adjustments. Target 7.2.5, signed release/ISO delivery, audible sound, capture and rollback remain unverified.

Hardware reports should include the exact commit, model, relevant device/codec IDs, kernel/headers, package/provider versions, existing configuration and reproducible results. Use the feature-specific checklist and recovery preparation in the evidence. Keep author reports distinct from independently reproduced outcomes.

## Attribution

The source table names PR authors. The prepared commit uses **Shawn Yeager** as Git Author, with native co-author credit for **J7, Jake Pillai**. Source-declared co-author trailers are retained too. Andrew Boyd is the consolidating committer; this does not imply source-author approval or sign-off. See [verified commit attribution](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/AUTHORSHIP.md).

Jev supplied advisory classification; agent work compared sources, consolidated compatible existing contributions, reconciled target collisions and recorded checks. Software observations do not establish hardware support.
