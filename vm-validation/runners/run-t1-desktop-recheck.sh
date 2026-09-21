#!/bin/bash
# Continue from a shut-down, installed T1 scenario in a new disposable overlay.
set -euo pipefail
review_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
iso=$(realpath "${1:?Pass the local ISO}")
previous=$(realpath "${2:?Pass the completed T1 scenario directory}")
build_dir=$(dirname "$iso")
[[ -s $previous/run.qcow2 && -s $previous/reboot.log && -s $previous/pam-before.txt ]]
grep -Fq 't1bridge-dkms/0.1.9, 7.2.5-4-omarchy, x86_64: installed' "$previous/reboot.log"
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
SCENARIO=mac-t1-desktop-recheck
source "$build_dir/sources/omarchy-iso/test/integration.d/base-test.sh"
source "$review_root/reviews/vm-install/guest-session.sh"
qemu-img create -f qcow2 -b "$previous/run.qcow2" -F qcow2 "$RUN_DIR/run.qcow2" >/dev/null
cp "$previous/OVMF_VARS.4m.fd" "$RUN_DIR/OVMF_VARS.4m.fd"
ACTIVE_OVMF="$RUN_DIR/OVMF_VARS.4m.fd"
start_vm "$RUN_DIR/run.qcow2" "$RUN_DIR/serial.log"
wait_for_ssh "$BOOT_TIMEOUT"
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
establish_guest_desktop
ssh_guest 'cat > /home/omarchy/guest-t1-desktop.sh' < "$review_root/reviews/vm-install/guest-t1-desktop.sh"
status=0
ssh_guest 'bash /home/omarchy/guest-t1-desktop.sh' > "$RUN_DIR/t1-desktop.log" 2>&1 || status=$?
ssh_guest 'tar -C /home/omarchy -cf - t1-desktop-evidence' | tar -C "$RUN_DIR" -xf - || true
python3 "$review_root/reviews/vm-install/run-guest-lock-check.py" "$BASE_DIR" "$RUN_DIR/lock-check" --port "$SSH_PORT" > "$RUN_DIR/lock-check.log" 2>&1 || status=$?
ssh_sudo 'find /etc/pam.d -type f -exec sha256sum {} + | sort' > "$RUN_DIR/pam-after.txt"
diff -u "$previous/pam-before.txt" "$RUN_DIR/pam-after.txt" > "$RUN_DIR/pam-diff.txt" || status=$?
ssh_sudo 'pacman -Q t1bridge-dkms t1bridge t1bridge-omarchy libfprint-t1bridge fprintd-t1bridge; dkms status; systemctl --failed --no-pager' > "$RUN_DIR/installed-state.log"
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
log "T1 desktop recheck exit $status. Artifacts: $RUN_DIR"
exit "$status"
