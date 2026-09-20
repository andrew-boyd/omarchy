# P03 review evidence

Carry #12076's focused sysfs implementation for Broadcom wl/T2 detection and Vulkan/NVIDIA package selection. Six production files match the source; the NVIDIA script retains the target's equivalent heredoc delimiter. Added fixtures do not change hardware policy.

## Known gaps and future work

- No power-use or GPU-wakeup measurement, real installer run or mid-read hot-unplug validation was performed. Broader architecture changes in #11259 remain separate.

## Hardware acceptance checklist

- [ ] Record model, kernel, PCI vendor/device/class identifiers and existing driver packages on the affected Intel Mac.
- [ ] Compare sysfs detection and package selection with expected BCM4331/4360 and Intel/AMD/NVIDIA display hardware; check BCM43602 remains with brcmfmac.
- [ ] Check installation in a disposable system or image with a recovery path, including helper availability at each installer stage.
- [ ] If claiming fewer GPU wakes or lower power use, measure those outcomes on real hardware with a repeatable before/after procedure. Fixture tests only establish tested selection behavior.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
