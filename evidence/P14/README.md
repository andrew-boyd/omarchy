# P14 review evidence

Carry #11904's complete standalone suspend diagnostics command unchanged. It has a read-only status path and active test/diagnose/restore paths; it adds no automatic boot, installer or sleep hook.

## Known gaps and future work

- Behavioral verification is absent: bash -n checks syntax only, and no production subcommand ran. The author did not report a complete end-to-end automated diagnose loop.
- State records candidates before checking successful writes; restore ignores failures and clears state. INT/TERM restoration does not explicitly terminate, and EXIT/HUP/RTC cleanup and shared-state ownership are incomplete.
- Failed rtcwake can be classified as non-culprit/inconclusive. A generated rule replaces a same-name file and matches USB vendor/product broadly. Wall-clock duration does not establish S3 or the cause of early wake.
- Active commands suspend or write wake settings and require an attended recoverable trial with independently captured state. No unrestricted live-use recommendation is made.
- The full candidate suite also fails bin-style-test.sh: the unchanged source uses command -v rtcwake at line 44 instead of the required Omarchy command helper. This source-specific style failure is separate from the four upstream-control failures; it remains unfixed for the draft.

## Hardware acceptance checklist

- [ ] Read the full unchanged script and findings before considering an active diagnostic trial. `test`/`diagnose` suspend hardware; `restore` writes wake settings.
- [ ] Record exact model/kernel/sleep mode, ACPI/USB wake state, RTC alarm, existing tool state and udev rules on a recoverable attended machine.
- [ ] Validate interruption and restoration failures in a disposable fixture before live diagnose. The source records candidates rather than confirmed successful writes, lacks a terminating signal trap and can clear state after failed writes.
- [ ] Assess multiple identical USB devices and shared-controller effects before accepting a generated vendor/product rule.
- [ ] Keep independent console/recovery access and a captured restoration plan; no active source command was run here.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
