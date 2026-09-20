# Intel Mac consolidation targets

14 feature roll-ups and 3 package companions organize 67 reviewed source/context PRs (52 original references plus later related discoveries). Existing PRs remain credited; closure recommendations are conditional. Scope: 64-bit Intel Macs. No hardware certification or complete release-wide integration is claimed.

## Feature and package targets

| ID | Proposal | Follow-up base in the coordinating fork | Source rows |
| --- | --- | --- | --- |
| P01 | [[Intel Mac P01] Keep keyboard layout tracking on typing devices](bodies/P01.md) | [andrew-boyd/omarchy:intel-mac/p01-keyboard-layout](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p01-keyboard-layout) | 2 |
| P02 | [[Intel Mac P02] Repair headers for retained stock kernels](bodies/P02.md) | [andrew-boyd/omarchy:intel-mac/p02-kernel-headers](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p02-kernel-headers) | 9 |
| P03 | [[Intel Mac P03] Consolidate Apple hardware detection](bodies/P03.md) | [andrew-boyd/omarchy:intel-mac/p03-hardware-detection](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p03-hardware-detection) | 5 |
| P04 | [[Intel Mac P04] Consolidate lid handling and display classification](bodies/P04.md) | [andrew-boyd/omarchy:intel-mac/p04-lid-handling](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p04-lid-handling) | 8 |
| P05 | [[Intel Mac P05] Handle ghost internal displays](bodies/P05.md) | [andrew-boyd/omarchy:intel-mac/p05-ghost-displays](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p05-ghost-displays) | 2 |
| P06 | [[Intel Mac P06] Retire the legacy SPI package alongside T1Bridge](bodies/P06.md) | [andrew-boyd/omarchy:intel-mac/p06-spi-retirement](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p06-spi-retirement) | 3 |
| P07 | [[Intel Mac P07] Preserve the MacBook8,1 SPI PIO workaround](bodies/P07.md) | [andrew-boyd/omarchy:intel-mac/p07-spi-pio](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p07-spi-pio) | 1 |
| P08 | [[Intel Mac P08] Consolidate FaceTime PCIe camera support](bodies/P08.md) | [andrew-boyd/omarchy:intel-mac/p08-facetime-camera](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p08-facetime-camera) | 2 |
| P08-packages | [[Intel Mac P08/packages] Consolidate FaceTime PCIe camera packages](bodies/P08-packages.md) | [andrew-boyd/omarchy-pkgs:intel-mac/p08-facetime-camera](https://github.com/andrew-boyd/omarchy-pkgs/tree/intel-mac/p08-facetime-camera) | 2 |
| P09 | [[Intel Mac P09] Consolidate NVMe suspend applicability](bodies/P09.md) | [andrew-boyd/omarchy:intel-mac/p09-nvme-suspend](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p09-nvme-suspend) | 2 |
| P10 | [[Intel Mac P10] Consolidate Broadcom calibration and sleep recovery](bodies/P10.md) | [andrew-boyd/omarchy:intel-mac/p10-broadcom-wifi](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p10-broadcom-wifi) | 6 |
| P11 | [[Intel Mac P11] Consolidate model-specific Cirrus audio support](bodies/P11.md) | [andrew-boyd/omarchy:intel-mac/p11-cirrus-audio](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p11-cirrus-audio) | 12 |
| P11-packages | [[Intel Mac P11/packages] Consolidate model-specific Cirrus audio packages](bodies/P11-packages.md) | [andrew-boyd/omarchy-pkgs:intel-mac/p11-cirrus-audio](https://github.com/andrew-boyd/omarchy-pkgs/tree/intel-mac/p11-cirrus-audio) | 12 |
| P12 | [[Intel Mac P12] Consolidate T1Bridge support and fingerprint UI](bodies/P12.md) | [andrew-boyd/omarchy:intel-mac/p12-t1bridge](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p12-t1bridge) | 14 |
| P12-packages | [[Intel Mac P12/packages] Package the existing T1Bridge stack](bodies/P12-packages.md) | [andrew-boyd/omarchy-pkgs:intel-mac/p12-t1bridge](https://github.com/andrew-boyd/omarchy-pkgs/tree/intel-mac/p12-t1bridge) | 14 |
| P13 | [[Intel Mac P13] Consolidate the Intel Mac kernel migration policy](bodies/P13.md) | [andrew-boyd/omarchy:intel-mac/p13-kernel-policy](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p13-kernel-policy) | 2 |
| P14 | [[Intel Mac P14] Consolidate suspend diagnostics](bodies/P14.md) | [andrew-boyd/omarchy:intel-mac/p14-suspend-diagnostics](https://github.com/andrew-boyd/omarchy/tree/intel-mac/p14-suspend-diagnostics) | 1 |

## Contribution and merge order

Open feature work against `andrew-boyd/omarchy` and the exact feature base above; package work goes to `andrew-boyd/omarchy-pkgs` with the matching base. Use `[Intel Mac PNN]` or `[Intel Mac PNN/packages]` in titles and `intel-mac/pnn/short-change` contributor branches. Merging follow-ups updates their roll-up. PR numbers are assigned only when drafts are created; these deterministic branch links identify the targets without invented numbers.

Review/open the three package companions first, then their linked feature drafts. Package availability must precede dependent installer/migration acceptance. P12 UI is independently reviewable; its hardware path requires manual setup. P06 retirement requires that prepared provider transition and resolution of P07 ownership before any automatic rollout. P02 header repair and P13 kernel policy are separate decisions. Other features can be reviewed independently. Shared installer/manual/lock files require reconciliation in a later optional release branch; there is no claim that all fourteen stack cleanly today.

## Validation status

Full Omarchy pre-push runs and an unchanged-base control are recorded under [checks](checks). They currently fail and skip cases as disclosed in each body. The three package candidates pass their available self-test subset; Docker isolation, publish-artifact and maintainer-controlled build CI remain unrun. Hardware and visual evidence are absent. This packet makes the known gaps reviewable; it does not approve deployment.

## Labels and repository requirements

Available Omarchy labels include `mac`, `compatibility`, `sleep`, `bug`, `documentation`, `dragon`, `duplicate`, `enhancement`, `nvidia` and `verified`. Suggested labels are recorded per proposal; none is applied. `verified` is a maintainer/triage readiness signal and is not self-awarded. The meaning of `dragon` was not established. No dedicated roll-up labels exist upstream. Package `build-approved` and workflow approvals remain maintainer-controlled. Optional labels on our own fork can be considered after publication.

Follow repository AGENTS/contribution rules, atomic commits and prescribed tests; visual changes need actual before/after evidence before readiness is claimed. No mandatory PR title/body template was found. [Publication metadata](manifest.json), [source coverage](source-coverage.json) and [publication procedure](PUBLICATION.md) pin the scope and exact local candidates.
