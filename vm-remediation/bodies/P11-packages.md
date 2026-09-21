# [Intel Mac P11/packages] Consolidate model-specific Cirrus audio packages

Consolidate the existing CS8409 and 12-inch MacBook audio recipes as separate, conflicting hardware tracks. The earlier VM-observed 12-inch header-dependency repair is retained; this validation adds no new audio-driver implementation.

**Draft consolidation for source review and hardware-owner follow-up.** Known defects remain; no hardware or merge-readiness certification is claimed. Part of the [14-feature Intel Mac series](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/INTEL-MAC-ROLLUPS.md) with three package companions.

**Contribute:** open follow-up PRs in `andrew-boyd/omarchy-pkgs` with base **`intel-mac/p11-cirrus-audio`**. Use `[Intel Mac P11/packages]` in the title and a contributor branch such as `intel-mac/p11/describe-change`. Link this feature in the series index. Merging a follow-up into this branch updates its roll-up.

## Published series

This draft: [omacom/omarchy-pkgs#557](https://github.com/omacom/omarchy-pkgs/pull/557). [All feature and package drafts](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/INTEL-MAC-ROLLUPS.md).

Feature draft: [omacom/omarchy#12689](https://github.com/omacom/omarchy/pull/12689). Keep the merge/setup dependencies below.

## Rebuilt ISO and software follow-up — 2026-09-21 UTC

Current draft head: `f2e815619d90ba8ba5e7f819ccdc7640386b16fb`. Original contribution commits and attribution are preserved.

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

- **This feature:** CS8409 companion built/installed, DKMS compiled and reboot passed in Build 5. Final Build 6 fresh install verified 12-inch audio 0.1-2, matching Omarchy headers, no stock kernel/header pull, no orphan-kernel hook error, successful target DKMS build and reboot, unchanged PAM. Driver sources unchanged; no physical speaker-safety claim.
- **Hardware boundary:** Virtual audio cannot validate speaker safety, channel mapping or hardware mixer behavior. Accepted source gaps below remain.
- **Overall limits:** the unchanged-baseline shared-ESP factory-reset test failed; the report retains it and the harness interventions. This remains a draft, not release/hardware certification.
- **Follow-up commit:** `f2e815619d90ba8ba5e7f819ccdc7640386b16fb`; original author commit remains its parent. [Exact follow-up patch](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/followups/P11-packages.patch).

[Results and limits](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/HANDOFF.md) · [Feature coverage](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/COVERAGE.md) · [Exact sources and reproduction](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/REPRODUCE.md) · [Final artifact receipt](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/receipts/final-validation.json).


</details>

## Scope and dependencies

Review P11/packages first; publish the appropriate package before its model-specific installer/migration trial. Do not install both conflicting audio packages together. The iMac in-tree track has no package prerequisite.

Paired target: [[Intel Mac P11] Consolidate model-specific Cirrus audio support](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p11-cirrus-audio). The feature branch owns Omarchy changes; the package branch owns recipes. Source treatments below describe the pair as a whole. No source is considered fully covered by only one half where both are needed.

## Every reviewed source PR and recommended action

| Source and author | State | Treatment and rationale | Recommended original action |
| --- | --- | --- | --- |
| [omacom/omarchy#10458](https://github.com/omacom/omarchy/pull/10458) — @inspiretelapps | open | **incorporated**: Complete iMac CS4208 configuration using the in-tree codec; original configuration/route risks recorded. Follow-ups preserve customized files and routes and make repeated setup safe. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [omacom/omarchy#11625](https://github.com/omacom/omarchy/pull/11625) — @andyholst | open | **alternative**: Unpinned direct-clone CS8409 delivery with differing installer/migration gates. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#12286](https://github.com/omacom/omarchy/pull/12286) — @teomurgi | open | **alternative**: Complete conflicting MacBook proposal includes automatic EFI writes and freeze sleep policy; preserve separately. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#6921](https://github.com/omacom/omarchy/pull/6921) — @sunoxen-lab | open | **incorporated**: MacBook CS4208 baseline combined with the existing linked mixer/current-kernel upgrade contribution; uses package omacom/omarchy-pkgs#153. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [omacom/omarchy#7140](https://github.com/omacom/omarchy/pull/7140) — @shawnyeager | open | **predecessor**: CS8409 predecessor credited through omacom/omarchy#9516; narrower model coverage retained as comparison. | Credit the successor; recommend closure after maintainers accept the represented scope. |
| [omacom/omarchy#8285](https://github.com/omacom/omarchy/pull/8285) — @jack-lech | open | **alternative**: Different CS8409 -git package name and installer/cache ownership; not stacked. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#9516](https://github.com/omacom/omarchy/pull/9516) — @j7j7 | open | **incorporated**: Selected complete CS8409 installer; paired with package omacom/omarchy-pkgs#249. The follow-up anchors the documented model set and uses matching kernel headers. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [omacom/omarchy-pkgs#153](https://github.com/omacom/omarchy-pkgs/pull/153) — @doctor | open | **incorporated**: Selected MacBook CS4208 recipe, with a VM-observed kernel-header dependency correction in a follow-up commit. The two audio packages serve separate model paths and conflict on one machine. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [omacom/omarchy-pkgs#155](https://github.com/omacom/omarchy-pkgs/pull/155) — @shawnyeager | open | **predecessor**: CS8409 package predecessor credited through omacom/omarchy-pkgs#249; preserved independently, not an additional companion PR. | Credit the successor; recommend closure after maintainers accept the represented scope. |
| [omacom/omarchy-pkgs#249](https://github.com/omacom/omarchy-pkgs/pull/249) — @j7j7 | open | **incorporated**: Selected unchanged CS8409 package recipe; package companion combines it with omacom/omarchy-pkgs#153. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [sunoxen-lab/omarchy#1](https://github.com/sunoxen-lab/omarchy/pull/1) — @doctor | open | **partial**: Existing mixer/service/current-kernel upgrade work included. Its separate s2idle proposal is retained as an unselected alternative. | Keep uncovered portions open; consider closure only after author/maintainer agreement on complete coverage. |
| [leifliddy/macbook12-audio-driver#60](https://github.com/leifliddy/macbook12-audio-driver/pull/60) — @doctor | merged | **context**: Merged driver preparation/DKMS changes underpin package omacom/omarchy-pkgs#153. Its preparation files match, while the older pinned Makefiles differ; the package does not contain every change in this driver PR. | Already merged; retain attribution and context. No action proposed. |

These are recommendations for original authors and maintainers. No original PR is closed, edited or automatically linked for closure. Complete source diffs, pinned heads and authors—including unselected alternatives—are in the [source inventory](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/source-coverage.json).

<details>
<summary>Original pre-VM publication checks and provenance</summary>

## Original publication checks (historical)

- Base: `omacom/omarchy-pkgs:master` at `4b60e4cd95972c16fbf3da634522a955cf7bf36c`.
- Prepared commit: `dd91732c68a4bce5b26af7a5ad15aacd41601ca9`; tree: `eb633a12f0c9774db16f1cff529a2e7fc449b0e4`.
- [Exact patch](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/patches/P11-packages.patch), SHA-256 `f5584a507810d4fb66a0ae327fd53faa1343699c7963aafc0f859c3700f51050`. The contribution diff matches the accepted consolidation; the [upstream refresh](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/UPSTREAM-REFRESH.md) advances its base without changing that contribution.
- Available package CI self-tests: **12/12 command groups passed**, including the workflow-approval tests; changed recipe syntax/JSON checks recorded. These ran on this actual tree in a disconnected disposable filesystem.
- Unrun: publish-artifact fixture (`rclone` unavailable), Docker build-isolation job, remote build-pr approval and fresh signed target-kernel delivery. The local subset does not equal passing upstream CI.
- [Check logs and receipts](https://github.com/andrew-boyd/omarchy/tree/intel-mac/review-index/checks) and [focused evidence / hardware checklist](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/evidence/P11/README.md). Observations reproducing defects are not successful hardware behavior. No real module load, firmware write, suspend or host configuration change occurred.
- Tests ran at this rebased commit, `dd91732c68a4bce5b26af7a5ad15aacd41601ca9`. The prior commits remain audit evidence; these results belong to that original publication tree, before the VM follow-up.


</details>

## Known gaps and follow-up work

- [ ] These two DKMS audio packages conflict and must be tested on their separate model tracks. The iMac CS4208 configuration track needs no new package.
- [ ] The packages have local ISO, matching 7.2.5-4-omarchy header/DKMS and reboot evidence. Signed distribution delivery remains unverified.
- [ ] Audible sound, capture, speaker safety, repeated suspend and physical rollback require hardware. No EFI or new sleep policy is included.
- [ ] The associated P11 runtime draft carries model-gate/custom-configuration/setup repairs; package compilation alone does not validate those physical configurations.

Hardware reports should include the exact commit, model, relevant device/codec IDs, kernel/headers, package/provider versions, existing configuration and reproducible results. Use the feature-specific checklist and recovery preparation in the evidence. Keep author reports distinct from independently reproduced outcomes.

## Attribution

The source table names PR authors. The prepared commit uses **Shawn Yeager** as Git Author, with native co-author credit for **J7, Jake Pillai**. Source-declared co-author trailers are retained too. Andrew Boyd is the consolidating committer; this does not imply source-author approval or sign-off. See [verified commit attribution](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/AUTHORSHIP.md).

Jev supplied advisory classification; agent work compared sources, consolidated compatible existing contributions, reconciled target collisions and recorded checks. Software observations do not establish hardware support.

Software repairs and test-harness corrections are subsequent agent-assisted commits by the consolidating contributor; original author credit does not imply approval of those follow-ups.
