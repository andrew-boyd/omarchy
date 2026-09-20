# Intel Mac consolidation targets

14 feature roll-ups and 3 package companions organize 73 reviewed source/context PRs (52 original references plus later related discoveries). Existing PRs remain credited; closure recommendations are conditional. Scope: 64-bit Intel Macs. No hardware certification or complete release-wide integration is claimed.

**17 draft PRs are open: 14 feature groups + 3 package companions.** No groups are held. See [current scope decisions](scope-decisions.json). P04 retains connector/debounce future work; P09 retains custom-unit preservation/applicability gaps and its alternative. P06 requires the existing manual T1Bridge replacement before removal; P10 is a provisional pre/post recovery target with its documented gaps.

## Feature and package targets

| ID | Proposal | Follow-up base in the coordinating fork | Source rows | Status |
| --- | --- | --- | --- | --- |
| P01 | [[Intel Mac P01] Keep keyboard layout tracking on typing devices](https://github.com/omacom/omarchy/pull/12679) | [andrew-boyd/omarchy:intel-mac/p01-keyboard-layout](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p01-keyboard-layout) | 2 | Draft PR |
| P02 | [[Intel Mac P02] Repair headers for retained stock kernels](https://github.com/omacom/omarchy/pull/12680) | [andrew-boyd/omarchy:intel-mac/p02-kernel-headers](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p02-kernel-headers) | 9 | Draft PR |
| P03 | [[Intel Mac P03] Consolidate Apple hardware detection](https://github.com/omacom/omarchy/pull/12681) | [andrew-boyd/omarchy:intel-mac/p03-hardware-detection](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p03-hardware-detection) | 5 | Draft PR |
| P04 | [[Intel Mac P04] Consolidate lid handling and display classification](https://github.com/omacom/omarchy/pull/12682) | [andrew-boyd/omarchy:intel-mac/p04-lid-handling](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p04-lid-handling) | 12 | Draft PR |
| P05 | [[Intel Mac P05] Handle ghost internal displays](https://github.com/omacom/omarchy/pull/12683) | [andrew-boyd/omarchy:intel-mac/p05-ghost-displays](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p05-ghost-displays) | 3 | Draft PR |
| P06 | [[Intel Mac P06] Retire the legacy SPI package alongside T1Bridge](https://github.com/omacom/omarchy/pull/12684) | [andrew-boyd/omarchy:intel-mac/p06-spi-retirement](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p06-spi-retirement) | 4 | Draft PR |
| P07 | [[Intel Mac P07] Preserve the MacBook8,1 SPI PIO workaround](https://github.com/omacom/omarchy/pull/12685) | [andrew-boyd/omarchy:intel-mac/p07-spi-pio](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p07-spi-pio) | 2 | Draft PR |
| P08 | [[Intel Mac P08] Consolidate FaceTime PCIe camera support](https://github.com/omacom/omarchy/pull/12686) | [andrew-boyd/omarchy:intel-mac/p08-facetime-camera](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p08-facetime-camera) | 2 | Draft PR |
| P08-packages | [[Intel Mac P08/packages] Consolidate FaceTime PCIe camera packages](https://github.com/omacom/omarchy-pkgs/pull/556) | [andrew-boyd/omarchy-pkgs:intel-mac/p08-facetime-camera](https://github.com/andrew-boyd/omarchy-pkgs/tree/intel-mac/p08-facetime-camera) | 2 | Draft PR |
| P09 | [[Intel Mac P09] Consolidate NVMe suspend applicability](https://github.com/omacom/omarchy/pull/12687) | [andrew-boyd/omarchy:intel-mac/p09-nvme-suspend](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p09-nvme-suspend) | 3 | Draft PR |
| P10 | [[Intel Mac P10] Consolidate Broadcom calibration and sleep recovery](https://github.com/omacom/omarchy/pull/12688) | [andrew-boyd/omarchy:intel-mac/p10-broadcom-wifi](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p10-broadcom-wifi) | 7 | Draft PR |
| P11 | [[Intel Mac P11] Consolidate model-specific Cirrus audio support](https://github.com/omacom/omarchy/pull/12689) | [andrew-boyd/omarchy:intel-mac/p11-cirrus-audio](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p11-cirrus-audio) | 12 | Draft PR |
| P11-packages | [[Intel Mac P11/packages] Consolidate model-specific Cirrus audio packages](https://github.com/omacom/omarchy-pkgs/pull/557) | [andrew-boyd/omarchy-pkgs:intel-mac/p11-cirrus-audio](https://github.com/andrew-boyd/omarchy-pkgs/tree/intel-mac/p11-cirrus-audio) | 12 | Draft PR |
| P12 | [[Intel Mac P12] Consolidate T1Bridge support and fingerprint UI](https://github.com/omacom/omarchy/pull/12690) | [andrew-boyd/omarchy:intel-mac/p12-t1bridge](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p12-t1bridge) | 19 | Draft PR |
| P12-packages | [[Intel Mac P12/packages] Package the existing T1Bridge stack](https://github.com/omacom/omarchy-pkgs/pull/558) | [andrew-boyd/omarchy-pkgs:intel-mac/p12-t1bridge](https://github.com/andrew-boyd/omarchy-pkgs/tree/intel-mac/p12-t1bridge) | 19 | Draft PR |
| P13 | [[Intel Mac P13] Consolidate the Intel Mac kernel migration policy](https://github.com/omacom/omarchy/pull/12691) | [andrew-boyd/omarchy:intel-mac/p13-kernel-policy](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p13-kernel-policy) | 2 | Draft PR |
| P14 | [[Intel Mac P14] Consolidate suspend diagnostics](https://github.com/omacom/omarchy/pull/12692) | [andrew-boyd/omarchy:intel-mac/p14-suspend-diagnostics](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p14-suspend-diagnostics) | 1 | Draft PR |

## Contribution and merge order

Open feature work against `andrew-boyd/omarchy` and the exact feature base above; package work goes to `andrew-boyd/omarchy-pkgs` with the matching base. Use `[Intel Mac PNN]` or `[Intel Mac PNN/packages]` in titles and `intel-mac/pnn/short-change` contributor branches. Merging follow-ups updates their roll-up. The table links each live draft and its canonical contribution branch.

Review the three package companions alongside their linked feature drafts. Package availability must precede dependent installer/migration acceptance. P12 UI is independently reviewable; its hardware path requires manual setup. P06 retirement requires that prepared provider transition and resolution of P07 ownership before any automatic rollout. P02 header repair and P13 kernel policy are separate decisions. Other features can be reviewed independently. Shared installer/manual/lock files require reconciliation in a later optional release branch; there is no claim that all fourteen stack cleanly today.

## Validation status

Full Omarchy pre-push runs and an unchanged-base control are recorded under [checks](checks). They currently fail and skip cases as disclosed in each body. The three package candidates pass their available self-test subset; Docker isolation and publish-artifact checks were not run locally; live maintainer-controlled CI status is on each draft. Hardware and visual evidence are absent. This packet makes the known gaps reviewable; it does not approve deployment.

## Labels and repository requirements

Available Omarchy labels include `mac`, `compatibility`, `sleep`, `bug`, `documentation`, `dragon`, `duplicate`, `enhancement`, `nvidia` and `verified`. Suggested labels are recorded per proposal; none is applied. `verified` is a maintainer/triage readiness signal and is not self-awarded. The meaning of `dragon` was not established. No dedicated roll-up labels exist upstream. Package `build-approved` and workflow approvals remain maintainer-controlled. Optional labels on our own fork can be considered after publication.

Follow repository AGENTS/contribution rules, atomic commits and prescribed tests; visual changes need actual before/after evidence before readiness is claimed. No mandatory PR title/body template was found. [Publication metadata](manifest.json), [source coverage](source-coverage.json) and [publication procedure](PUBLICATION.md) pin the scope and exact local candidates.

Original Git authors and co-author trailers are preserved in the prepared commits; [attribution details](AUTHORSHIP.md) distinguish actual contributing identities from PR openers. Preserve this metadata during later squash/rebase.

[Latest upstream refresh](UPSTREAM-REFRESH.md): rebased candidates, source dispositions and refreshed check receipts. The accepted P04/P09 scope remains unchanged.
