# P12 review evidence

Pair #11273/#11952's shared fingerprint UI with the existing T1Bridge manual setup path. T1Bridge is the preferred owner of T1 hardware support; its existing five-package split is retained, with an optional panel auto-brightness consumer. Competing legacy providers remain alternatives.

## Known gaps and future work

- No automatic Omarchy installer, provider transition or fresh-ISO setup is supplied. Automatic keyboard lighting and legacy default-on/menu behavior are absent; optional auto-brightness controls the panel only.
- The original optional release has a reproduced DPMS-off panel acceptance defect. Original driver packaging lacks the additional provider-conflict/header guards found in a historical local rewrite; those authored repairs are excluded.
- Core 0.1.9 documents system suspend/resume as unsupported on its tested machine. Display blank/wake does not establish whole-system suspend support or parity across T1 models.
- Machine-specific EFI/FDR data remains owner-supplied. The matched libfprint/fprintd pair replaces distribution libraries, and enrollment does not configure every PAM consumer. Password fallback, camera coexistence and rollback require hardware validation.
- Official archive requests returned HTTP 403 in the recorded refresh; cached public archives match pinned hashes. Original-recipe dependency resolution, a new fingerprint-library build and the exact 7.2.5 ABI remain unverified. Prior adapted-recipe builds cannot certify absent guards.

## Hardware acceptance checklist

- [ ] Record exact T1 model, kernel/headers, package versions and module/service/renderer ownership. Preserve the same-machine EFI/FDR backup, password access and a recovery boot route.
- [ ] Review the released core README and setup/removal documents. Use their existing manual setup on a prepared system, preserving the matched fingerprint library pair. Record hooks, DKMS/initramfs and reboot separately.
- [ ] Review the optional desktop README for its session hook and independently enabled panel-brightness service. Check Touch Bar/Fn/HUDs, camera coexistence, ALS and manual brightness; explicitly record the DPMS-off defect.
- [ ] With the actual reader, test blank/wake, rapid failures, retry, enrollment absent, password in flight, late callbacks and unlock/relock. Capture before/after UI behavior; no live UI result was obtained here.
- [ ] Record cold boot and reboot. System suspend remains a released limitation; an attended investigation needs its own recovery plan.
- [ ] Follow released removal/recovery instructions and verify restored input, camera, login and password fallback. No hardware or rollback trial occurred in this effort.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
