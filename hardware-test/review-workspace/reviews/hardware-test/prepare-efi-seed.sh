#!/bin/bash
# Create synthetic EFI files on a virtual secondary disk inside a disposable VM.
# No Apple firmware, host disks, or host mounts are used.
set -euo pipefail
iso=$(realpath "${1:?Pass the previously installed ISO}")
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
export OMARCHY_INTEGRATION_SSH_PORT=2522 OMARCHY_INTEGRATION_MEMORY=4096
SCENARIO=synthetic-efi-seed
source "$(dirname "$iso")/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready
seed="$RUN_DIR/apple-efi-seed.qcow2"
qemu-img create -f qcow2 "$seed" 40G >/dev/null
qemu-img create -f qcow2 -b "$BASE_DISK" -F qcow2 "$RUN_DIR/run.qcow2" >/dev/null
cp "$BASE_OVMF" "$RUN_DIR/OVMF_VARS.4m.fd"
ACTIVE_OVMF="$RUN_DIR/OVMF_VARS.4m.fd"
start_vm "$RUN_DIR/run.qcow2" "$RUN_DIR/serial.log" \
  -drive "file=$seed,format=qcow2,if=none,id=seed0" \
  -device virtio-blk-pci,drive=seed0
wait_for_ssh "$BOOT_TIMEOUT"
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda && test -b /dev/vdb'
ssh_guest 'cat > /home/omarchy/seed-efi.sh' <<'GUEST'
#!/bin/bash
set -euo pipefail
[[ $(hostname) == omarchy-test && $(systemd-detect-virt) == kvm ]]
[[ $(blockdev --getsize64 /dev/vdb) == 42949672960 ]]
[[ $(lsblk -nr -o TYPE /dev/vdb) == disk ]]
printf 'label: gpt\nsize=1GiB, type=U\n' | sfdisk /dev/vdb
udevadm settle
mkfs.vfat -F 32 -n SYNTHETIC /dev/vdb1
mkdir -p /mnt/efi-seed
mount /dev/vdb1 /mnt/efi-seed
trap 'cd /; umount /mnt/efi-seed' EXIT
mkdir -p /mnt/efi-seed/EFI/APPLE/{EMBEDDEDOS,EXTENSIONS}
printf 'SYNTHETIC TEST FIXTURE — not Apple firmware\n' > /mnt/efi-seed/EFI/APPLE/EMBEDDEDOS/EmbeddedOSFirmware.im4p
printf 'SYNTHETIC TEST FIXTURE — no certificates\n' > /mnt/efi-seed/EFI/APPLE/EMBEDDEDOS/FDRData
printf 'SYNTHETIC TEST FIXTURE — extension\n' > /mnt/efi-seed/EFI/APPLE/EXTENSIONS/Firmware.scap
printf 'The fresh install must wipe this unrelated file.\n' > /mnt/efi-seed/old-esp-marker
cd /mnt/efi-seed
find EFI/APPLE -type f -print0 | sort -z | xargs -0 sha256sum > /home/omarchy/efi-seed.sha256
sync
GUEST
ssh_sudo 'bash /home/omarchy/seed-efi.sh' > "$RUN_DIR/seed.log" 2>&1
ssh_guest 'cat /home/omarchy/efi-seed.sha256' > "$RUN_DIR/efi-seed.sha256"
stop_vm
qemu-img check "$seed" > "$RUN_DIR/qcow2-check.txt"
printf '%s\n' "$seed" > "$RUN_DIR/seed-path.txt"
printf 'Synthetic EFI seed: %s\n' "$seed"
