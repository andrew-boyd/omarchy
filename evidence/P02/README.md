# P02 review evidence

Carry the existing #12074 migration that installs missing stock-kernel headers when broadcom-wl-dkms is present, including retained fallback kernels. The production migration is unchanged; local additions are fixtures.

## Known gaps and future work

- No real package transaction, wl connection, fallback boot or reboot was tested. Installing headers does not establish a successful DKMS build.

## Hardware acceptance checklist

- [ ] Record installed kernels, matching header packages, broadcom-wl-dkms version and dkms status before testing.
- [ ] On an affected test system with a recovery path, verify the migration installs missing stock headers while retaining Omarchy/T2 kernel coverage.
- [ ] Capture actual package and DKMS build output; a successful package transaction alone is insufficient.
- [ ] Verify wl loads and Wi-Fi works after reboot into each retained kernel, including the fallback; record rerun behavior and rollback procedure.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
