# P13 review evidence

Carry #12328's existing policy proposal to skip the pending kernel migration when DMI vendor begins with Apple. T2/architecture exclusions remain. This leaves pending upgrades on their existing kernels; it does not reverse completed upgrades or change the ISO default.

## Known gaps and future work

- Apple* is a broad case-sensitive vendor prefix, not a validated model list; it also matches the Appleish fixture. Missing/unreadable DMI still migrates.
- The original suite fails on both baseline and candidate at the superseded PTL migration assertion. Later cases in that suite do not run; the 13 supplemental scope assertions do not make the original suite pass.
- Kernel policy approval and actual boot/graphics/audio/network/resume validation remain external. No rollback to an older kernel is supplied for already-migrated machines.

## Hardware acceptance checklist

- [ ] Record model, DMI vendor, kernels/header packages, boot entries, DKMS modules and migration completion markers before testing.
- [ ] On an affected late-upgrade test system, check the source Apple exemption preserves existing kernel packages and BOOT_ORDER; retain a recovery boot path.
- [ ] Treat already-completed upgrades separately: this patch does not reinstall an older kernel, restore boot order or rerun completed user migrations.
- [ ] Record boot, graphics, audio, networking and resume outcomes for the exact kernel/driver versions. Compare kernels only on hardware with a recovery path; provide reproducible logs for any regression.
- [ ] Fresh installs retain current ISO defaults. A proposal to change those defaults or reverse completed upgrades is a separate policy decision, absent from this patch.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
