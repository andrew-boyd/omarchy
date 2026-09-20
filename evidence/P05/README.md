# P05 review evidence

Combine #10198's ghost-disabling recovery commands and watcher with #12072's backend display filter. All three production files match their sources; retain the target's current panel parser and enabled-count policy.

## Known gaps and future work

- Exclude #12072's duplicate frontend geometry filter and its assertion: the recorded end-to-end counterexample shows it removes real displays temporarily at 0x0.
- The selected backend still omits an identityless, modeless 0x0 external output. The existing guard counts enabled real displays awaiting recovery and does not guarantee a second visible image.
- Live rendering, hotplug, dock/undock and before/after visual captures remain unverified.

## Hardware acceptance checklist

- [ ] Record model, GPUs, kernel, Hyprland/Quickshell versions and complete monitor JSON before testing; record which internal panel is physically usable.
- [ ] Verify only the empty duplicate internal connector is disabled while the healthy panel remains active. Repeat after connector numbering changes, hotplug and configuration reload.
- [ ] Check the only internal connector and real external displays awaiting mode recovery remain enabled by the recovery helper; verify recovery completes on the real device.
- [ ] Check settings omit enabled and disabled identityless ghosts while retaining intentionally disabled real panels and external displays with identity or advertised modes.
- [ ] Test dock/undock, mirroring and re-enabling a deliberately disabled real display. Record the rendered rows and enabled count alongside the backend JSON.
- [ ] Assess the existing enabled-count guard when a real display is temporarily 0x0. This target preserves that baseline policy and does not guarantee that every counted display is currently showing a picture.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
