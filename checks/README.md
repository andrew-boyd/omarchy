# Check interpretation

Every feature runs the repository-prescribed `./test/all` on a disposable copy of its actual committed tree. An unchanged upstream base is the control. All source checkouts remain unchanged; no hardware or host configuration was touched. Package inputs are the matching companion where one exists; other features use the pinned package base. The pinned ISO checkout is present.

Full-run failures must be read from both the final failing-file summary and explicit assertion lines. Every run fails the four upstream-control files: locate, network QR, kernel migration and Plymouth. Two do not emit an explicit `not ok` assertion. P14 additionally fails bin-style-test.sh because its unchanged original diagnostics command uses `command -v rtcwake` instead of the required Omarchy helper. That source-specific failure is disclosed as follow-up; it is not an upstream-control failure. The logs retain their output and exceptions; no assertion was suppressed or source repaired for this packet.

A fresh-copy baseline diagnostic passes locate, while the full run raises a Unicode decoding exception during its scan. This suggests interaction with earlier tests in the writable full-suite checkout; it is not a diagnosed candidate regression. Fresh-copy network QR exits 2 after its first two cases. The kernel migration and Plymouth failures also reproduce on a fresh copy. Their root causes beyond the documented kernel assertion remain unresolved. These diagnostic runs do not replace the failed full suite.

Graphical/device/tool/namespace skips are listed in each receipt. `assertions_passed` counts literal `ok` lines, including skip messages; it is not a count of hardware cases or an overall passing suite. Tests within a failing file can stop at its first failure, though the runner continues to subsequent files.

The package candidates each pass ten available CI self-test command groups plus recorded syntax/metadata checks. The prescribed publish-artifact fixture needs unavailable rclone; Docker build-isolation and maintainer-controlled remote builds were not run. These local results do not satisfy the full upstream CI suite. Earlier package/DKMS receipts are qualified by their actual kernel, recipe and isolation limitations.

Paths/usernames in public logs are redacted. Current receipts contain the staged log hash and preserve the original log hash separately. Historical receipt hashes are in `../evidence/receipt-index.json`.

The authorship correction changes metadata only. Receipts retain their actual tested commit IDs; `reused_for_commit` identifies the corrected candidate with the same tree and base. See `../commit-authorship.json`. No new full-suite run is claimed for the corrected commit IDs.
