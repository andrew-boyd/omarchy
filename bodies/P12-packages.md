# [Intel Mac P12/packages] Package the existing T1Bridge stack

Import the existing T1Bridge core/driver 0.1.9, optional desktop consumer 0.2.1 and matched libfprint/fprintd recipes. Preserve the five-package design, runtime code, patches and defaults. Adapt only three archive locations and one license path for this repository; manual setup remains required.

**Draft consolidation for source review and hardware-owner follow-up.** Known defects remain; no hardware or merge-readiness certification is claimed. Part of the [14-feature Intel Mac series](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/INTEL-MAC-ROLLUPS.md) with three package companions.

**Contribute:** open follow-up PRs in `andrew-boyd/omarchy-pkgs` with base **`intel-mac/p12-t1bridge`**. Use `[Intel Mac P12/packages]` in the title and a contributor branch such as `intel-mac/p12/describe-change`. Link this feature in the series index. Merging a follow-up into this branch updates its roll-up.

## Scope and dependencies

Shared fingerprint UI can be reviewed independently. T1 hardware trials require P12/packages and the released manual setup on a prepared system. This is the replacement direction for P06, not an automatic migration supplied by either PR.

Paired target: [[Intel Mac P12] Consolidate T1Bridge support and fingerprint UI](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p12-t1bridge). The feature branch owns Omarchy changes; the package branch owns recipes. Source treatments below describe the pair as a whole. No source is considered fully covered by only one half where both are needed.

## Every reviewed source PR and recommended action

| Source and author | State | Treatment and rationale | Recommended original action |
| --- | --- | --- | --- |
| [omacom/omarchy#10331](https://github.com/omacom/omarchy/pull/10331) — @shawnyeager | open | **broader**: Legacy panel and automatic keyboard lighting retained separately. Selected T1Bridge consumer is optional, panel-only; scope is not equivalent. | Keep uncovered scope open. This narrower roll-up does not fully supersede it. |
| [omacom/omarchy#10582](https://github.com/omacom/omarchy/pull/10582) — @fresh3nough | open | **context**: First-run user-unit fix remains independent; accepted manual T1Bridge setup enables named units directly. | Retain as related context; no closure recommendation from this roll-up. |
| [omacom/omarchy#11273](https://github.com/omacom/omarchy/pull/11273) — @niconistal | open | **incorporated**: Existing shared lock blank/wake fingerprint lifecycle and retry behavior. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [omacom/omarchy#11952](https://github.com/omacom/omarchy/pull/11952) — @tonibergholm | open | **incorporated**: Existing status/enrollment UI combined with omacom/omarchy#11273 through their shared lock service. | Recommend closure in favor of this feature roll-up after maintainers accept preserved coverage. |
| [omacom/omarchy#12201](https://github.com/omacom/omarchy/pull/12201) — @slr01 | closed | **context**: Closed shared-reader predecessor superseded by omacom/omarchy#12426. | Already closed; retain attribution and context. No action proposed. |
| [omacom/omarchy#12420](https://github.com/omacom/omarchy/pull/12420) — @slr01 | open | **alternative**: Shared-reader blanking alternative avoids aborting the active scan; differs from selected omacom/omarchy#11273 lifecycle. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#12426](https://github.com/omacom/omarchy/pull/12426) — @slr01 | open | **alternative**: Fresh PAM-context ownership alternative supersedes omacom/omarchy#12201; differing hardware reports do not validate selected code. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#7064](https://github.com/omacom/omarchy/pull/7064) — @shawnyeager | open | **alternative**: Complete legacy EFI/Touch Bar handoff retained; competing HID-module provider not layered onto T1Bridge. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#7950](https://github.com/omacom/omarchy/pull/7950) — @csk-grit42 | open | **alternative**: Virtual-HID rebinding depends on legacy provider; differs from T1Bridge DRM/configuration ownership. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy-pkgs#152](https://github.com/omacom/omarchy-pkgs/pull/152) — @shawnyeager | open | **alternative**: Heratiki legacy driver and ACPI power behavior conflict with selected T1Bridge ownership; full source preserved. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy-pkgs#298](https://github.com/omacom/omarchy-pkgs/pull/298) — @monomyth | open | **alternative**: AJ/freeze-safe legacy provider with different reports and no legacy ALS module; not evidence for T1Bridge behavior. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy-pkgs#315](https://github.com/omacom/omarchy-pkgs/pull/315) — @shawnyeager | open | **alternative**: Legacy ALS service packaging retained; selected T1Bridge optional package installs its own original service. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#12435](https://github.com/omacom/omarchy/pull/12435) — @jonathan-downs | open | **alternative**: Overlapping shared lock/resume lifecycle reviewed with P04. Keep separate from the selected omacom/omarchy#11273/omacom/omarchy#11952 service until the differing triggers and reader behavior are reconciled. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#12502](https://github.com/omacom/omarchy/pull/12502) — @mohan314e | open | **context**: Overlapping shared lock/resume lifecycle reviewed with P04. Keep separate from the selected omacom/omarchy#11273/omacom/omarchy#11952 service until the differing triggers and reader behavior are reconciled. | Retain as related context; no closure recommendation from this roll-up. |

These are recommendations for original authors and maintainers. No original PR is closed, edited or automatically linked for closure. Complete source diffs, pinned heads and authors—including unselected alternatives—are in the [source inventory](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/source-coverage.json).

## Validation and provenance

- Base: `omacom/omarchy-pkgs:master` at `bda2a070f4641fd44e5d02bd9cbf7da3fce4e345`.
- Prepared commit: `30fd083f692e64c91571f3d710aa8b0f45b6daf4`; tree: `b2d0b11b41597343c84dad16a3750ccc48a77bc4`.
- [Exact patch](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/patches/P12-packages.patch), SHA-256 `0e003b22c9cc44e6bb931537306a7ea1ca2851e473a23215260eb0cc90ca6363`. The candidate tree matches the already-reviewed consolidation; publication preparation changes no implementation.
- Available package CI self-tests: **10/10 command groups passed**, including the workflow-approval tests; changed recipe syntax/JSON checks recorded. These ran on this actual tree in a disconnected disposable filesystem.
- Unrun: publish-artifact fixture (`rclone` unavailable), Docker build-isolation job, remote build-pr approval and fresh signed target-kernel delivery. The local subset does not equal passing upstream CI.
- [Check logs and receipts](https://github.com/andrew-boyd/omarchy/tree/intel-mac/review-index/checks) and [focused evidence / hardware checklist](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/evidence/P12/README.md). Observations reproducing defects are not successful hardware behavior. No real module load, firmware write, suspend or host configuration change occurred.

## Known gaps and follow-up work

- [ ] No automatic Omarchy installer, provider transition or fresh-ISO setup is supplied. Automatic keyboard lighting and legacy default-on/menu behavior are absent; optional auto-brightness controls the panel only.
- [ ] The original optional release has a reproduced DPMS-off panel acceptance defect. Original driver packaging lacks the additional provider-conflict/header guards found in a historical local rewrite; those authored repairs are excluded.
- [ ] Core 0.1.9 documents system suspend/resume as unsupported on its tested machine. Display blank/wake does not establish whole-system suspend support or parity across T1 models.
- [ ] Machine-specific EFI/FDR data remains owner-supplied. The matched libfprint/fprintd pair replaces distribution libraries, and enrollment does not configure every PAM consumer. Password fallback, camera coexistence and rollback require hardware validation.
- [ ] Official archive requests returned HTTP 403 in the recorded refresh; cached public archives match pinned hashes. Original-recipe dependency resolution, a new fingerprint-library build and the exact 7.2.5 ABI remain unverified. Prior adapted-recipe builds cannot certify absent guards.

Hardware reports should include the exact commit, model, relevant device/codec IDs, kernel/headers, package/provider versions, existing configuration and reproducible results. Use the feature-specific checklist and recovery preparation in the evidence. Keep author reports distinct from independently reproduced outcomes.

## Attribution

Original authors and the treatment of their work are listed above. Jev supplied advisory classification; agent work compared sources, consolidated compatible existing contributions, reconciled target collisions and recorded checks. Software observations do not establish hardware support.

The existing released T1Bridge sources and recipes are by Standard Agents / Andrew Boyd and their upstream contributors. Original MIT/GPL/LGPL notices and fingerprint patches are preserved. The [released setup/removal documents](https://github.com/andrew-boyd/omarchy/tree/intel-mac/review-index/evidence/P12/released-docs) and pinned public source archives accompany the evidence.
