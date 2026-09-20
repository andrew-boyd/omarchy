# P01 review evidence

Apple headset remotes and SMC power/lid devices can appear as keyboards. Combine the two existing exclusions so these controls do not select the layout label or replace the remembered typing keyboard; retain shared layout synchronization.

## Known gaps and future work

- Live Quickshell rendering, IPC timing and actual device events remain untested. Before/after visual captures are still needed.

## Hardware acceptance checklist

- [ ] Record model, kernel, Hyprland/Quickshell versions, input device names and configured layouts.
- [ ] On a multi-layout session, check the displayed label while switching through every layout using the widget and keyboard shortcut.
- [ ] Check internal and external typing keyboards, reconnection and unknown device names; then check available SMC/headset event devices do not take over label selection.
- [ ] Report expected and observed labels with device/event logs. Shared layout synchronization remains unchanged; exclusion from label selection does not mean exclusion from switch recipients.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
