# P07 review evidence

Carry all of #9735 unchanged for the exact MacBook8,1: PIO and s2idle parameters through a Limine drop-in, retained SPI initramfs modules and the original migration. The author's input/lid report is attributed evidence, not a test of this branch.

## Known gaps and future work

- A custom drop-in without the PIO substring is replaced, discarding other parameters. A comment-only substring can produce a completion marker without the active setting.
- A file with PIO but without s2idle is accepted; an existing marker plus comment-only match suppresses repair. Four boundary observations reproduce these defects.
- No live boot, encrypted-root input, suspend or rollback trial occurred. P06 retirement requires separate ownership review before combined deployment.
- The full suite additionally failed preinstalls-test.sh (cliamp reported missing). Its relevant files are identical to upstream; 5/5 isolated repetitions pass on each tree. The cause remains unestablished, and the original failing receipt is retained for follow-up.

## Hardware acceptance checklist

- [ ] Review all four inherited configuration defects below before a trial. Use a disposable or independently recoverable installation, inspect the exact drop-in and markers, and do not rely on a completion marker as evidence of effective boot parameters.
- [ ] Use a confirmed MacBook8,1 with an external USB keyboard and recovery boot media. Record DMI, kernel, installed SPI provider, boot entry and effective kernel command line; do not extrapolate to later MacBooks or T1.
- [ ] Preserve the exact prior Limine drop-in, SPI initramfs configuration and boot artifacts, including whether each file was absent. Record the machine repair marker and each test user migration marker. Test rollback on recoverable media before relying on internal input.
- [ ] On an agreed test candidate, verify both parameters reach the actual selected boot entry and /proc/cmdline after reboot; writing a drop-in or completing a rebuild alone does not establish that.
- [ ] Check internal keyboard and trackpad at encrypted-disk unlock, login and the desktop. Record failures as well as successful cases and keep the external keyboard available.
- [ ] Repeat lid-close and manual suspend/resume cycles, checking input each time. Record the selected sleep mode, elapsed sleep time, kernel messages and any recovery needed. Source reports do not establish power-use or resume behavior on another kernel.
- [ ] For rollback, restore the captured prior configuration and boot artifacts through the known recovery route; a rebuild must use the restored configuration. Restore prior marker state deliberately so a pending migration cannot silently reapply the trial. Verify the previous boot entry and input behavior. This checklist has not been exercised on hardware.

## Reading the receipts

Source comparisons, recorded focused checks and boundary observations are retained under `receipts/`. A passing observation that reproduces a defect is not a successful behavior test. Earlier source-review status fields refer to that receipt, not to publication readiness. Local usernames/paths were redacted; original and staged hashes are in the evidence inventory. New full-suite results and exact candidate commits are under `../../checks/` and `../../manifest.json`. Hardware, visual acceptance and remote CI remain unverified.
