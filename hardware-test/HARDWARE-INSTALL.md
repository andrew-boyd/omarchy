# First physical trial: MacBookPro13,3

**Ready for an attended hardware trial.** Use `omarchy-intel-mac-20260921-9e6288ef.iso`, SHA-256 `9e6288ef5cc1eadce519cdd7384c8030286eb938a6288eb218f025a61b433252` (6,215,624,704 bytes). Fresh VM installation and required software checks are complete; the [test report](HANDOFF.md) preserves failed runs and qualified reruns. Physical hardware remains untested by this effort. No USB media has been flashed.

This is one physical test within the all-64-bit-Intel-Mac effort. It does not validate pre-T1 or T2 machines, other T1 models, or every alternative in the inventory. Apple Silicon is outside this effort.

## Before writing media or erasing a disk

1. Identify the actual test machine and the disk to be erased by model, capacity and serial number. MacBookPro13,3 is a 2016 15-inch **T1** Mac, not a T2 Mac. The build host is also this model; that does not authorize erasing the build host. USB flashing and physical installation are a later, explicit step.
2. Have a person at the machine, AC power, a wired keyboard/mouse if needed, and a USB Ethernet adapter or another known-working network path. Installation and recovery must not depend on the experimental Wi-Fi path or continued remote access.
3. Verify a restorable external backup of the target's data and its existing EFI System Partition, including `EFI/APPLE/EMBEDDEDOS` if present. Keep it off the disk being installed. Check file hashes from the external copy. For Touch ID, explicitly verify this Mac's `EFI/APPLE/EMBEDDEDOS/FDRData`: packages and re-enrollment cannot recreate it. If it is missing, follow the pinned provider's recovery instructions before claiming Touch ID readiness. Do not use another Mac's firmware/FDR files: they may contain machine-specific material. Do not upload them to GitHub or the public evidence branch.
4. Establish a recovery path before the wipe. On Intel Macs, holding **Option** at startup selects a startup disk; **Command-R** enters local Recovery and **Option-Command-R** requests Internet Recovery. Confirm that the chosen recovery method is available on this actual machine. Apple's [startup-key reference](https://support.apple.com/en-ie/102603) and [bootable macOS installer guide](https://support.apple.com/en-ie/101578) describe the supported steps. A Btrfs snapshot on a disk about to be erased is not a backup.
5. Match the downloaded ISO's SHA-256 to the final handoff. Use a USB drive with capacity greater than the actual ISO file, and verify the written image when the later flashing step is authorized. No destructive device command is supplied here before the device is identified.

The integrated Apple EFI contribution copies the folder to RAM before a whole-disk wipe and restores it before the bootloader is installed. It is **best-effort**: warnings do not stop installation, and its own comparison checks file counts and sizes rather than content hashes. Preserve the independent backup even after VM tests pass. See [source PR #174](https://github.com/omacom/omarchy-iso/pull/174).

## What this model can exercise

| Area | Candidate expectation | Physical check / limitation |
| --- | --- | --- |
| Internal keyboard/trackpad | Native `applespi`, with the selected initramfs modules | Type into the installer, encryption unlock and desktop; test trackpad after cold boot. A VM keyboard does not test SPI. |
| Graphics/display | Existing Apple gmux routing; no new GPU-switching policy | Confirm internal panel and external display separately. This host's internal panel is routed through Radeon; do not power it off as a generic hybrid-GPU optimization. |
| Wi-Fi | MacBookPro13,3 board NVRAM only for its matched PCI/subsystem IDs; BCM4350/BCM43602 recovery hook | Inspect actual IDs and configuration, test association and traffic before attempting sleep. Board-data fetching can require network access during setup; record any download failure. |
| Audio | Selected CS8409 DKMS package | Confirm matching kernel/headers and successful DKMS build before reboot; test speakers initially at low volume, microphone and headphones separately. This ISO does not inherit the build host's custom speaker tuning. |
| NVMe | Selected P09 installer excludes MacBookPro13,3 | Confirm the actual storage and GPU addresses. Do not enable another model's fixed-address unit or copy the build host's historical unit, which targets Radeon despite its NVMe name. |
| Touch Bar/camera/ALS/fingerprint | Accepted T1Bridge package/manual setup path | Preserved EFI files and packages alone do not establish working T1 hardware. Follow the pinned P12 provider instructions before retiring an old provider; record each component independently. No automatic T1 installer is claimed. |
| PCIe FaceTime camera | P08 is a different camera path | This T1 model's iBridge USB camera is not validation of the Broadcom PCIe camera package. |
| Sleep/wake | Existing selected contributions only | Run attended trials after basic input/display/network work. Keep AC power and recovery access available; a successful VM suspend fixture is not a physical sleep result. |

The build host's custom `touchbar-rs`, UVC override, speaker tuning and existing workaround files are local machine state, not evidence that the fresh ISO includes or reproduces them. Leave that host unchanged while preparing the image. If it later becomes the selected install target, its data, firmware and custom runtime need their own backup and recovery plan.

For the selected provider, use the pinned [T1Bridge 0.1.9 manual setup](provider-docs/t1bridge-0.1.9/docs/setup.md) and [released support table](provider-docs/t1bridge-0.1.9/README.md). The release explicitly reports system suspend/resume as **not working on its tested machine**; this effort has not resolved that limitation. Treat a T1 sleep trial as a recovery-prepared experiment, not an expected supported capability. Display blanking is a separate check. The [optional desktop README](provider-docs/t1bridge-omarchy-0.2.1/README.md) describes panel brightness and media integration; automatic keyboard lighting is absent.

Those are source-release instructions. This ISO carries locally built, hash-recorded trial archives and a development-runtime dependency adapter; it is not the provider's signed release repository. Do not switch repositories or upgrade to an unrecorded version during the initial trial. Manual setup also requires a local graphical session for authorization; remote SSH alone cannot substitute for enrollment.

The handoff includes `intel-mac-companions-9e6288ef.tar.gz` alongside the ISO and their `SHA256SUMS`. Its [package manifest](companion-download.json) records the exact ten companion archives extracted and verified from this ISO. Keep this bundle available on separate media for the manual T1 stage. Install only the relevant track; the two audio packages conflict and must not be installed together.

For the later T1 stage, on the **freshly installed test Mac**, after verifying the outer archive checksum and completing the backup/recovery prerequisites:

```bash
tar -xzf intel-mac-companions-9e6288ef.tar.gz
(cd packages && sha256sum -c SHA256SUMS)
sudo pacman -U --needed \
  packages/t1bridge-0.1.9-1-x86_64.pkg.tar.zst \
  packages/t1bridge-dkms-0.1.9-1-x86_64.pkg.tar.zst \
  packages/t1bridge-omarchy-0.2.1-2.1-any.pkg.tar.zst \
  packages/libfprint-t1bridge-1.94.100-17-x86_64.pkg.tar.zst \
  packages/fprintd-t1bridge-1.94.5-14-x86_64.pkg.tar.zst
```

Read the transaction and DKMS results before accepting a reboot. Preserve the matched library/daemon pair and password fallback. Then follow the pinned manual's service/group activation, supported reboot handoff and same-machine data import steps. Do not hot-swap providers, copy another Mac's FDR data, or change signature policy to bypass a failed transaction. These commands are preparation instructions, not actions performed on the build host.

## Installation and first boot

1. Boot the verified USB through the Intel Mac startup picker. Confirm the installer displays correctly and the internal keyboard/trackpad work. Record the displayed ISO/build version and any boot errors.
2. Select the independently identified destination disk. Verify its identity again at the destructive confirmation. Stop if the installer cannot see the expected disk, the firmware backup is missing, or the target is ambiguous.
3. Use the same installation mode validated in the final VM report. For an encrypted installation, verify that the **internal** keyboard can unlock the disk on the first reboot. Keep the wired keyboard available for recovery and record if it was required.
4. Before optional provider changes or sleep tests, capture the baseline below. Verify the restored `EFI/APPLE` files against the independent pre-install manifest. If preservation warned or hashes differ, preserve logs and resolve recovery before testing T1 peripherals.
5. Check package/header versions and DKMS status. Keep the initial software versions fixed during the first trial; an update creates a different test candidate and must be recorded.

Read-only baseline commands on the **installed test machine**:

```bash
cat /sys/class/dmi/id/product_name
uname -a
cat /proc/cmdline
lsblk -e7 -o NAME,MODEL,SIZE,TYPE,FSTYPE,MOUNTPOINTS,TRAN
lspci -nnk
cat /proc/bus/input/devices
pacman -Q omarchy-dev omarchy-settings-dev linux-omarchy linux-omarchy-headers
dkms status
systemctl --failed --no-pager
hyprctl monitors all
wpctl status
cat /sys/power/mem_sleep
journalctl -b -p warning..alert --no-pager
```

Save diagnostic output privately first. Before sharing, remove serial numbers, MAC addresses, SSIDs, user information and any firmware certificates. Preserve the unredacted originals locally so redaction does not destroy evidence.

## Ordered physical checks

- **Boot and input:** two cold boots; internal keyboard and trackpad in the installer, encrypted unlock if selected, greeter and desktop. Record whether an external keyboard was needed.
- **Desktop and applications:** panel brightness, keyboard layout switching, terminal, strict Neovim startup, lock with an incorrect password followed by the correct password, external-display attach/detach. Keep password fallback working before fingerprint experiments.
- **Network:** association and sustained traffic on available 2.4/5 GHz networks; then Bluetooth pairing/audio separately. Report unavailable bands as untested, not failed or passed.
- **Audio:** speakers at low initial volume, channel routing, microphone and headphones. Do not import another codec/model's mixer preset.
- **T1:** follow the pinned P12 manual setup in a separate recorded stage. Verify Touch Bar, camera, ALS and fingerprint individually after reboot. Preserve the ability to return to the prior provider; do not run competing providers simultaneously.
- **Sleep:** only after the preceding baseline, try one attended suspend/resume using the current default sleep mode. Then check internal input, panel, Wi-Fi, audio and T1 components. If stable, repeat several short cycles, followed by a longer attended cycle. Record the mode and duration. Stop at the first hard hang or regression and collect the previous/current boot logs rather than stacking another workaround.

No P09 NVMe adjustment, custom #422 kernel, T2 Wi-Fi recovery, hibernation policy or new power tuning is added to this trial merely because sleep fails. Those are separate candidates with different evidence and scope.

## Recovery and result handoff

If the installed system fails, use the prepared recovery media/Intel startup picker and the verified backup. Do not erase again, reset NVRAM, substitute another Mac's firmware, or layer unrelated fixes as an automatic response. Record the last successful stage, visible error and whether a normal reboot restores function; decide the recovery action from that evidence.

Report: ISO SHA-256, exact model and PCI IDs, kernel/package versions, installation/encryption mode, test step, expected/observed result, logs/screenshots and whether reproducible. Mark **pass / fail / untested / not applicable** for each hardware area. Link findings to the relevant P01–P14 target. A pass on this machine is labeled **MacBookPro13,3 only**; [the full inventory](INVENTORY.md) retains the other model and T2 work.
