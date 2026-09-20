# P10 review evidence

Combine #11017's MacBookPro13,3 / 106b:015a calibration, #7671's MacBookPro14,2/14,3 path and #12314's pre-sleep unbind/post-wake rebind. Retain the three original installer calls; no calibration bytes, model gates or recovery logic were invented.

## Known gaps and future work

- The selected installer overwrites a customized same-path sleep hook. Failed post-sleep bind loses retry state, and repeated pre-sleep calls clear outstanding state.
- Compare #12314 with the complete #11434 post-resume alternative on the reported BCM4350 and BCM43602 setups. #11434's original failing assertion remains documented alongside its corrected fixture.
- Calibration redistribution, pinned download availability, authentication, traffic, repeated sleep and rollback remain unverified. The 13,3 source adds no update migration. Contradictory calibration reports and broader uncovered boards remain open.
- P12's whole-system T1 suspend limitation is separate. The old combined preview contains calibration only; this individual branch contains the selected recovery source too.

## Hardware acceptance checklist

- [ ] Record exact DMI model, PCI vendor/device/subsystem IDs, kernel, firmware and package versions, regdomain, existing supplicant settings, and AP band/channel/width/security. Record the actual installed NVRAM hash, accounting for its machine-specific MAC; do not share a private MAC unnecessarily.
- [ ] Keep local recovery access or a separate wired connection. Preserve all existing generic, DMI-specific, compressed and override firmware files, including symlinks and absence, before a deliberate trial. Do not reload the radio carrying a remote session.
- [ ] Exercise only the source-supported path: fresh setup for MacBookPro13,3 with 106b:015a; fresh setup and migration 1787312531 for MacBookPro14,2/14,3. The 13,3 source adds no migration. Verify access to the pinned download where required; an offline 13,3 ISO path is not provided.
- [ ] After a cold boot, test actual authentication and data transfer separately on 2.4 GHz and 5 GHz. Record supplicant completion and AP-side station evidence where available; scan visibility alone is insufficient. Preserve failed attempts and kernel firmware errors.
- [ ] Compare throughput and stream capabilities using the same AP, channel width, distance and repeated A/B/A trials. Report link rates separately from measured throughput. RSSI readings can move because calibration offsets change; they are not proof of improved reception.
- [ ] Check MAC stability after reboot and rerun, existing-file preservation, fresh-install behavior and the 14,x migration reboot prompt. Record which file the driver requests/loads, especially if a pre-existing override causes the leaf to skip or shadow another file.
- [ ] After reviewing the documented hook-ownership and retry-state defects, compare the selected #12314 lifecycle with the separate #11434 alternative on an attended recoverable system. Record exact branch commit, board IDs, existing hooks, pre/post state, repeated short/long sleep, association and traffic. Use one lifecycle at a time; neither is a proven cross-model fix.
- [ ] For rollback, restore the captured prior files and absence state, removing only files introduced by this trial. Restore prior migration-marker state deliberately for 14,x and reboot through the known recovery route. Verify original band/authentication behavior returns. No rollback was physically exercised here.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
