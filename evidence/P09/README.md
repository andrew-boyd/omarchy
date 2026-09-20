# P09 review evidence

Use complete #11624's narrower Apple-controller implementation as an accepted provisional NVMe consolidation draft, with its custom-unit overwrite/deletion risks documented. Preserve #10877's first-controller discovery approach separately. Selection does not establish that a discovered controller needs a quirk.

## Known gaps and future work

- #11624 overwrites custom units and removes them when vendor data is missing, unreadable or non-Apple. Ownership, unknown-state handling and rollback remain unresolved.
- The fixed PCI address/vendor test does not prove an affected storage controller. Multi-controller, Samsung/replaced-drive and model applicability need hardware evidence.
- #10877 also overwrites units and can reset a legacy GPU power setting based on a path substring. Neither source is recommended for unattended live installation.

## Hardware acceptance checklist

- [ ] Resolve the source ownership/cleanup findings before selecting a live candidate. Neither complete source proposal is currently recommended for installation; no host workaround should be replaced from this review.
- [ ] On an agreed recoverable test system, record DMI model, exact controller vendor/device/subsystem and PCI class, controller firmware, kernel, sleep mode, NVMe device-to-PCI mapping and whether storage is internal, replaced or externally attached. An Apple drive model string is not an Apple PCI vendor ID.
- [ ] Record the original failure and its recovery path on the exact hardware. Compare a proposed controller setting with the captured baseline while keeping other power/workaround settings fixed. Do not infer necessity from discovery or from a failure log ending at suspend entry.
- [ ] Capture the existing unit and drop-ins, ownership, enabled state, target address, and deliberate customizations before any approved trial. Missing or unreadable sysfs data must remain an unknown observation, not permission to remove a custom unit.
- [ ] Check that only the intended affected storage controller changes and that unrelated GPU/bridge settings remain as captured. Cover multiple-controller and absent-controller situations without applying a first-device assumption to real storage.
- [ ] Record repeated short/long suspend and cold-boot behavior, storage availability, errors and required recovery. Distinguish deep from s2idle and successful NVMe recovery from successful whole-system resume.
- [ ] For rollback, restore captured units, drop-ins, enablement and prior parameter values through the known recovery route; do not assume restoring every value to one recreates the baseline. Restore migration-marker state deliberately. No physical trial or rollback was performed here.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
