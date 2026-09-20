# P08 review evidence

Combine #12067's packaged FaceTime PCIe delivery with #11381's exact Apple DMI gate. Keep the original detector, wiring, migration and manual; the companion proposes the existing facetimehd-dkms, facetimehd-firmware and facetimehd-data recipes.

## Known gaps and future work

- PCIe 14e4:1570 cameras are the scope; USB/iBridge cameras are separate. #11381's AUR delivery, nonfatal failure policy, live module load and duplicate migration are excluded.
- Prior private build/DKMS checks used available 7.2.3 headers. Matching Omarchy 7.2.5 headers, signed distribution delivery, real package hooks and ISO availability were not verified.
- Camera frames, calibration/image quality, reboot, suspend and rollback require hardware. Firmware/calibration source redistribution and delivery require review.

## Hardware acceptance checklist

- [ ] Record Apple model, PCI 14e4:1570, kernel/header versions and current camera driver/firmware providers. USB/iBridge cameras are outside this candidate.
- [ ] Keep a recovery boot entry and record how to restore previous driver, firmware and calibration packages. Review conflicts with existing AUR/Git providers before changing a hardware test system.
- [ ] On an agreed candidate and tested kernel, capture the actual package transaction and DKMS logs, module binding and video-device enumeration.
- [ ] Capture real frames, reporting resolution, frame rate, orientation, color and low-light behavior. Package checksums and fixture results do not establish image quality or correct calibration.
- [ ] Check reboot, repeated setup and suspend/resume with frame capture afterward. Keep existing-install and fresh-install/offline-cache results distinct.
- [ ] Restore the prior packages and boot entry through the recorded recovery procedure and confirm prior behavior. No physical trial or rollback was performed here.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
