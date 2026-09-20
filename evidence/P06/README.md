# P06 review evidence

Carry the complete #9880 installer/cache cleanup and retirement migration. The intended T1 replacement is P12's existing manual T1Bridge path; the source migration itself neither detects nor installs that replacement. Accepted as a dependent local test target only for systems that have completed that manual replacement before removal; automatic migration remains a documented gap.

## Known gaps and future work

- Global removal can affect installations that have not completed a provider transition. A failed old DKMS build does not establish that installed modules are unused.
- Review a transition before automatic rollout. Encrypted-root input, package hooks, initramfs, Touch Bar/camera/ALS and rollback remain untested.
- P12 lacks automatic keyboard lighting and established system suspend support. P07 retains the baseline SPI package; package ownership must be resolved before combining P06 and P07 for release.

## Hardware acceptance checklist

- [ ] Record exact model, kernel, initramfs, installed old package and all current T1/SPI module and service owners. Keep an independent recovery boot path and prior package/initramfs.
- [ ] On a T1 machine, first complete the accepted P12 manual setup on a prepared system, reboot and validate that the intended provider owns Touch Bar/ALS and that password/input access works. Do not use this migration as a way to perform the provider handoff.
- [ ] Review the actual package-drop transaction and initramfs hook behavior before an attended removal trial. Preserve locally modified configuration and record dependency removals. No such transaction was run here.
- [ ] Check input at encrypted-root unlock and in the desktop, then Touch Bar, camera and ALS. Any sleep trial remains separately constrained by T1Bridge's documented suspend limitation.
- [ ] Test restoration using the recorded prior boot/package/configuration state. Neither these instructions nor passing source fixtures certify live removal or rollback.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
