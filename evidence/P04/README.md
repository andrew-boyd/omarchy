# P04 review evidence

Use #10713's verified active-external-display lid-lock component as an accepted provisional consolidation draft. Retain existing logind sleep ownership. Connector identity, real USB displays and debounce remain documented future work; all competing sources are preserved.

## Known gaps and future work

- #11516 excludes every USB connector, including real USB displays. Touch Bar identity needs device evidence.
- The separate #12210 changes global sleep policy, includes a 20-second model delay, can terminate an unrelated reused PID and has a missing installed wake hook.
- #10462, #12435, #12616 and #12634 have different wake triggers or filtering scope. No connecting implementation was invented. Physical lid/display/lock behavior and visual captures remain unverified.

## Hardware acceptance checklist

- [ ] Record model, kernel, Hyprland version, physical DRM connectors and compositor monitor JSON; identify the Touch Bar separately from usable external screens.
- [ ] Undocked: close the lid and verify the session locks even when a Touch Bar connector is connected. Reopen and record the existing wake behavior.
- [ ] Docked: verify an active external monitor keeps the session usable. Repeat with that output disabled, disconnected and reconnected.
- [ ] Check any available USB-C/DisplayLink outputs, mirrors, and rapid close/reopen events. Record actual connector names rather than assuming USB means Touch Bar.
- [ ] Record existing logind and suspend-toggle behavior. This component changes the lock decision only; it does not introduce debounce or replace the sleep owner.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
