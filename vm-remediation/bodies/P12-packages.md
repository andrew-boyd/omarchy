# [Intel Mac P12/packages] Package the existing T1Bridge stack

Package the accepted released T1Bridge sources and matched fingerprint stack. The optional t1bridge-omarchy recipe advances to 0.2.1-2 with a focused patch that suppresses brightness policy when the internal panel is off or its state is unknown. Original source hashes, licenses and the published stable runtime dependency remain.

**Draft consolidation for source review and hardware-owner follow-up.** Known defects remain; no hardware or merge-readiness certification is claimed. Part of the [14-feature Intel Mac series](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/INTEL-MAC-ROLLUPS.md) with three package companions.

**Contribute:** open follow-up PRs in `andrew-boyd/omarchy-pkgs` with base **`intel-mac/p12-t1bridge`**. Use `[Intel Mac P12/packages]` in the title and a contributor branch such as `intel-mac/p12/describe-change`. Link this feature in the series index. Merging a follow-up into this branch updates its roll-up.

## Published series

This draft: [omacom/omarchy-pkgs#558](https://github.com/omacom/omarchy-pkgs/pull/558). [All feature and package drafts](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/INTEL-MAC-ROLLUPS.md).

Feature draft: [omacom/omarchy#12690](https://github.com/omacom/omarchy/pull/12690). Keep the merge/setup dependencies below.

## Rebuilt ISO and software follow-up — 2026-09-21 UTC

Current draft head: `bdf07c6e157a226c0ea57c69107505a5ad7b567d`. Original contribution commits and attribution are preserved.

The repaired combined ISO built and completed fresh unencrypted and encrypted installation/reboot checks. All 13 embedded local package archives and 52 changed runtime payloads were verified against the pinned source. Clean desktop acceptance reruns passed all eight files. The original interrupted/failed harness runs remain in the report; focused reruns are not relabeled as green original aggregates.

**The ISO is not entirely green:** the stricter editor-startup check still fails because the unchanged baseline Neovim package requests an unavailable theme repository. A guest-only replacement-source experiment passed, but that repair is not in this ISO or these feature branches. The earlier acceptance suite did not catch that error.

- **This branch:** the optional brightness-controller repair is in the package companion; 12 repository self-test groups passed. Its production checks ran during the ISO package build. The existing stable dependency and the local ISO adapter remain explicitly separate.
- **Follow-up diff:** [software/test changes](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-remediation/followups/P12-packages.patch); the source-author contribution commits remain ancestors of this head.
- **Combined baseline:** shared-ESP factory reset now passes staging, unattended first boot and provisioning while preserving foreign entries/files. An older unsafe factory snapshot is refused. These baseline repairs are supplied in the integration evidence, not inserted into unrelated feature branches.
- **Boundary:** physical Intel Mac behavior and signed distribution delivery remain unverified. DMI/device input fixtures and virtual RTC/NVMe checks do not emulate Apple hardware.

[Current handoff](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-remediation/HANDOFF.md) · [Exact test/artifact receipts](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-remediation/receipts/results.json) · [Reproduction](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-remediation/REPRODUCE.md) · [Pinned source bundles](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-remediation/integration/sources.json).

<details>
<summary>Earlier ISO/VM validation, before these software repairs</summary>

## ISO / VM validation — 2026-09-21 UTC

Tested as part of the combined 14-feature custom ISO. Fresh encrypted and unencrypted installs booted; the final rebuilt ISO passed all eight desktop acceptance files with the documented test-only OCR correction. The combined live-guest CLI suite and 267 shell files passed, including focused rechecks.

- **This feature:** All five exact T1 packages installed; T1 DKMS built against the installed kernel; reboot passed; PAM hashes unchanged. With an actual logged-in guest desktop, provider reported cap13, volume changed 100 to37, mute toggled and state restored; OSD and fallback notification inspected. Password lock rejected wrong and accepted correct password; zero failed system units. Physical fingerprint/Touch Bar/ALS absent; optional auto-brightness inactive.
- **Hardware boundary:** Device provisioning, Touch ID, Touch Bar, ALS and camera ownership require actual T1 hardware. Accepted source gaps below remain.
- **Overall limits:** the unchanged-baseline shared-ESP factory-reset test failed; the report retains it and the harness interventions. This remains a draft, not release/hardware certification.

[Results and limits](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/HANDOFF.md) · [Feature coverage](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/COVERAGE.md) · [Exact sources and reproduction](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/REPRODUCE.md) · [Final artifact receipt](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/vm-validation/receipts/final-validation.json).


</details>

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
| [omacom/omarchy-pkgs#298](https://github.com/omacom/omarchy-pkgs/pull/298) — @monomyth | open | **alternative**: AJ/freeze-safe legacy provider with different reports and no legacy ALS module; not evidence for T1Bridge behavior. Refreshed head b6495c4 adds only local-package planner metadata; runtime stack and version remain unchanged. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy-pkgs#315](https://github.com/omacom/omarchy-pkgs/pull/315) — @shawnyeager | open | **alternative**: Legacy ALS service packaging retained; selected T1Bridge optional package installs its own original service. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#12435](https://github.com/omacom/omarchy/pull/12435) — @jonathan-downs | open | **alternative**: Overlapping shared lock/resume lifecycle reviewed with P04. Keep separate from the selected omacom/omarchy#11273/omacom/omarchy#11952 service until the differing triggers and reader behavior are reconciled. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#12502](https://github.com/omacom/omarchy/pull/12502) — @mohan314e | open | **context**: Overlapping shared lock/resume lifecycle reviewed with P04. Keep separate from the selected omacom/omarchy#11273/omacom/omarchy#11952 service until the differing triggers and reader behavior are reconciled. | Retain as related context; no closure recommendation from this roll-up. |
| [omacom/omarchy#12652](https://github.com/omacom/omarchy/pull/12652) — @dexteresc | open | **alternative**: Window-event focus recovery for an already active lock surface; separate from omacom/omarchy#12435's logind monitor and omacom/omarchy#9181's resume/PAM retry ownership. Preserve as a follow-up; not stacked into accepted fingerprint work. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#12614](https://github.com/omacom/omarchy/pull/12614) — @dexteresc | closed | **predecessor**: Closed in favor of omacom/omarchy#12652 to correct commit attribution; preserve the original source and exact production comparison. | Already closed; retain attribution and context. No action proposed. |
| [omacom/omarchy#12667](https://github.com/omacom/omarchy/pull/12667) — @prabhchintan | open | **context**: Shared lock numeric-keypad handling with an attributed Apple Magic Keyboard report. Separate from T1 provider and fingerprint lifecycle; retained as follow-up context, not a new prerequisite. | Retain as related context; no closure recommendation from this roll-up. |
| [omacom/omarchy#9181](https://github.com/omacom/omarchy/pull/9181) — @ClGratton | open | **alternative**: Broader FocusScope/focus-generation recovery changes the sleep monitor, explicit resume IPC and post-PAM retry policy. Preserve separately from omacom/omarchy#12652 and omacom/omarchy#12435; no mixed focus ownership is invented. | Retain for comparison; supersede only after distinct behavior and hardware coverage are accepted here. |
| [omacom/omarchy#10141](https://github.com/omacom/omarchy/pull/10141) — @monomyth | open | **broader**: Existing MacBookPro13,3 bundle combines separate calibration, legacy T1/SPI, NVMe and experimental Radeon work. Retain relevant device reports and model boundaries; this roll-up does not cover or endorse the full bundle. | Keep uncovered scope open. This narrower roll-up does not fully supersede it. |

These are recommendations for original authors and maintainers. No original PR is closed, edited or automatically linked for closure. Complete source diffs, pinned heads and authors—including unselected alternatives—are in the [source inventory](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/source-coverage.json).

<details>
<summary>Original pre-VM publication checks and provenance</summary>

## Original publication checks (historical)

- Base: `omacom/omarchy-pkgs:master` at `4b60e4cd95972c16fbf3da634522a955cf7bf36c`.
- Prepared commit: `014acc8e0b892105448a497eedad4780ed72b83e`; tree: `38d9351e72b9c7fea544167d5b70fa7df3fe83cf`.
- [Exact patch](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/patches/P12-packages.patch), SHA-256 `0e003b22c9cc44e6bb931537306a7ea1ca2851e473a23215260eb0cc90ca6363`. The contribution diff matches the accepted consolidation; the [upstream refresh](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/UPSTREAM-REFRESH.md) advances its base without changing that contribution.
- Available package CI self-tests: **12/12 command groups passed**, including the workflow-approval tests; changed recipe syntax/JSON checks recorded. These ran on this actual tree in a disconnected disposable filesystem.
- Unrun: publish-artifact fixture (`rclone` unavailable), Docker build-isolation job, remote build-pr approval and fresh signed target-kernel delivery. The local subset does not equal passing upstream CI.
- [Check logs and receipts](https://github.com/andrew-boyd/omarchy/tree/intel-mac/review-index/checks) and [focused evidence / hardware checklist](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/evidence/P12/README.md). Observations reproducing defects are not successful hardware behavior. No real module load, firmware write, suspend or host configuration change occurred.
- Tests ran at this rebased commit, `014acc8e0b892105448a497eedad4780ed72b83e`. The prior commits remain audit evidence; these results belong to that original publication tree, before the VM follow-up.


</details>

## Known gaps and follow-up work

- [ ] No automatic Omarchy installer or provider transition is supplied. Owner-supplied EFI/FDR data and matching kernel-header preparation remain prerequisites. Automatic keyboard lighting is absent; optional auto-brightness controls the panel only.
- [ ] The optional controller now checks DPMS, enabled state and geometry before changing panel brightness. Physical sensor response, camera coexistence, fingerprint enrollment and provider transition remain unverified.
- [ ] Core 0.1.9 documents system suspend/resume as unsupported on its tested machine. Display blank/wake does not establish whole-system suspend support.
- [ ] The matched libfprint/fprintd pair replaces distribution libraries. Enrollment does not configure every PAM consumer; hardware password fallback and rollback still require validation.
- [ ] The combined ISO uses a documented adapter to depend on its exact local omarchy-dev version. The published recipe retains omarchy>=4.0.1; the adapter does not certify that separate stable-runtime combination or signed release delivery.

Hardware reports should include the exact commit, model, relevant device/codec IDs, kernel/headers, package/provider versions, existing configuration and reproducible results. Use the feature-specific checklist and recovery preparation in the evidence. Keep author reports distinct from independently reproduced outcomes.

## Attribution

The source table names PR authors. The prepared commit uses **Andrew Boyd** as Git Author. Source-declared co-author trailers are retained too. Andrew Boyd is the consolidating committer; this does not imply source-author approval or sign-off. See [verified commit attribution](https://github.com/andrew-boyd/omarchy/blob/intel-mac/review-index/AUTHORSHIP.md).

Jev supplied advisory classification; agent work compared sources, consolidated compatible existing contributions, reconciled target collisions and recorded checks. Software observations do not establish hardware support.

The existing released T1Bridge sources and recipes are by Standard Agents / Andrew Boyd and their upstream contributors. Original MIT/GPL/LGPL notices and fingerprint patches are preserved. The [released setup/removal documents](https://github.com/andrew-boyd/omarchy/tree/intel-mac/review-index/evidence/P12/released-docs) and pinned public source archives accompany the evidence.

Software repairs and test-harness corrections are subsequent agent-assisted commits by the consolidating contributor; original author credit does not imply approval of those follow-ups.
