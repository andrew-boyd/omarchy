#!/bin/bash
# Real QEMU NVMe at the candidate's fixed address; only DMI is a fixture.
set -euo pipefail
iso=$(realpath "${1:?Pass the tested local ISO}")
build_dir=$(dirname "$iso")
[[ $(cat "$build_dir/build.exit") == 0 ]]
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
SCENARIO=mac-nvme-nonmatching
source "$build_dir/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready || { echo 'Run the ISO integration installer first.' >&2; exit 1; }
qemu-img create -f qcow2 -b "$BASE_DISK" -F qcow2 "$RUN_DIR/run.qcow2" >/dev/null
qemu-img create -f qcow2 "$RUN_DIR/nvme.qcow2" 1G >/dev/null
cp "$BASE_OVMF" "$RUN_DIR/OVMF_VARS.4m.fd"
ACTIVE_OVMF="$RUN_DIR/OVMF_VARS.4m.fd"
start_vm "$RUN_DIR/run.qcow2" "$RUN_DIR/serial.log" \
  -device pcie-root-port,id=vintage-nvme-port,bus=pcie.0,addr=0x1c,chassis=1 \
  -drive file="$RUN_DIR/nvme.qcow2",format=qcow2,if=none,id=vintage-nvme \
  -device nvme,drive=vintage-nvme,serial=VINTAGE-VM-ONLY,bus=vintage-nvme-port
wait_for_ssh "$BOOT_TIMEOUT"
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
status=0
ssh_sudo '
  set -euo pipefail
  test "$(hostname)" = omarchy-test
  test "$(systemd-detect-virt)" = kvm
  lspci -nnk
  lsblk -o NAME,TYPE,MODEL,FSTYPE,MOUNTPOINTS
  pci=/sys/bus/pci/devices/0000:01:00.0
  test "$(cat "$pci/class")" = 0x010802
  test "$(cat "$pci/vendor")" != 0x106b
  test -e /dev/nvme0n1
  cat "$pci/vendor" "$pci/device" "$pci/d3cold_allowed"
  cat "$pci/d3cold_allowed" > /tmp/vintage-nvme-before
  printf "MacBook8,1\n" > /tmp/vintage-model
  sed "s|/sys/class/dmi/id/product_name|/tmp/vintage-model|g" \
    /usr/share/omarchy/install/hardware/apple/fix-suspend-nvme.sh > /tmp/vintage-nvme-leaf.sh
  test ! -e /etc/systemd/system/omarchy-nvme-suspend-fix.service
  bash -euo pipefail /tmp/vintage-nvme-leaf.sh
  test ! -e /etc/systemd/system/omarchy-nvme-suspend-fix.service
  # Also check a pre-existing user unit on this real nonmatching controller.
  printf "# VINTAGE-VM user customization\n" > /etc/systemd/system/omarchy-nvme-suspend-fix.service
  sha256sum /etc/systemd/system/omarchy-nvme-suspend-fix.service > /tmp/vintage-unit-before
  bash -euo pipefail /tmp/vintage-nvme-leaf.sh
  sha256sum -c /tmp/vintage-unit-before
  diff -u /tmp/vintage-nvme-before "$pci/d3cold_allowed"
  echo "PASS: real non-Apple NVMe at 0000:01:00.0 is excluded; its state and existing unit are preserved."
' > "$RUN_DIR/nvme.log" 2>&1 || status=$?
capture_console nvme-final
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
log "NVMe scenario exit $status. Artifacts: $RUN_DIR"
exit "$status"
