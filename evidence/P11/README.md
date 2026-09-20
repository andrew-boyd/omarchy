# P11 review evidence

Combine three existing audio tracks: #9516/#249 CS8409; #6921 plus @doctor's linked mixer/service/current-kernel upgrade contribution with #153 for MacBook CS4208; and complete #10458 in-tree iMac CS4208 configuration. The package companion contains two unchanged recipes for separate model tracks.

## Known gaps and future work

- The two DKMS audio packages conflict on one machine. The iMac CS4208 track needs no new DKMS package. Existing model gates are retained; the CS8409 regex is unanchored and can match unsupported suffixes.
- The MacBook follow-up's s2idle policy and #12286's freeze/EFI policy are both excluded. Contradictory sleep reports remain separate; no EFI changes are included.
- iMac setup replaces same-name rules and saved routes, tolerates mixer errors, and can fail after configuration changes. Preserve custom configuration before any trial.
- Original #6921 migration contents are retained under 1789869577.sh because its original name collides with an unrelated target migration; only matching test references were adjusted.
- Prior original-recipe DKMS builds passed on 7.2.3, with qualified download/fakeroot harness adjustments. Target 7.2.5, signed release/ISO delivery, audible sound, capture and rollback remain unverified.

## Hardware acceptance checklist

- [ ] Record exact model, codec/subsystem IDs, kernel/header/package versions and chosen track before a trial.
- [ ] Use a recoverable test installation; retain the prior kernel, modules, packages and user audio configuration for rollback.
- [ ] Test speakers, headphones, microphone, mute and volume independently; distinguish source reports from your observations.
- [ ] Record cold boot and repeated suspend/resume, mixer defaults, existing-install migration and fresh-install behavior separately.
- [ ] Capture DKMS and package transaction logs on the actual target kernel; 7.2.3 build evidence does not establish Omarchy 7.2.5 or offline ISO delivery.
- [ ] For MacBook comparisons use one complete alternative at a time. #12286 changes EFI/sleep state; it is held for review and excluded from the combined candidate.
- [ ] For iMac review preserve custom WirePlumber rules and routes first. The original source replaces/reset these; do not infer preservation from its passing suite.
- [ ] Restore captured packages/configuration and boot the prior kernel to verify rollback; no physical trial or rollback occurred here.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
