#!/bin/bash
# Fresh unattended installation over a synthetic pre-existing EFI partition.
set -euo pipefail
iso=$(realpath "${1:?Pass the rebuilt local ISO}")
seed=$(realpath "${2:?Pass the synthetic 40-GiB QCOW2 seed}")
manifest=$(realpath "${3:?Pass the seed SHA-256 manifest}")
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
export OMARCHY_INTEGRATION_SSH_PORT=2322 OMARCHY_INTEGRATION_MEMORY=4096
export OMARCHY_INTEGRATION_INITIAL_DISK="$seed"
SCENARIO=apple-efi-fresh-install
source "$(dirname "$iso")/sources/omarchy-iso/test/integration.d/base-test.sh"
[[ $(basename "$seed") == apple-efi-seed.qcow2 && -f $seed ]]
cp "$manifest" "$RUN_DIR/efi-seed.sha256"
sha256sum "$seed" > "$RUN_DIR/seed-before.sha256"
install_phase
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
ssh_guest 'cat > /home/omarchy/efi-seed.sha256' < "$manifest"
ssh_sudo 'cd /boot && sha256sum -c /home/omarchy/efi-seed.sha256 && test ! -e /boot/old-esp-marker' > "$RUN_DIR/efi-restored.log" 2>&1
python - "$(dirname "$iso")/installed-runtime-payload.json" <<'PY' |
import json,sys
for row in json.load(open(sys.argv[1])):
    print(row['sha256'] + '  ' + row['path'])
PY
  ssh_guest 'sha256sum -c -' > "$RUN_DIR/installed-payload.log"
ssh_guest 'pacman -Q omarchy-dev omarchy-settings-dev omarchy-nvim linux-omarchy; lsblk -f' > "$RUN_DIR/installed-inventory.log"
stop_vm
sha256sum -c "$RUN_DIR/seed-before.sha256" > "$RUN_DIR/seed-unchanged.log"
printf '0\n' > "$RUN_DIR/scenario.exit"
printf 'Fresh install preserved synthetic EFI files and wiped the unrelated marker: %s\n' "$RUN_DIR"
