#!/bin/bash
# Repeat only failed installed-product checks in a fresh disposable overlay.
set -euo pipefail
review_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
wave="$review_root/.state/vm-install/2026-09-20"
iso=$(realpath "${1:?Pass the installed Build 7 ISO}")
build_dir=$(dirname "$iso")
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
export OMARCHY_INTEGRATION_SSH_PORT=2422 OMARCHY_INTEGRATION_MEMORY=4096
SCENARIO=remediation-runtime-followups
source "$build_dir/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
source "$review_root/reviews/vm-install/guest-session.sh"
establish_guest_desktop
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
ssh_guest 'mkdir -p /home/omarchy/.local/share/omarchy && tar -C /home/omarchy/.local/share/omarchy -xf -' < <(tar -C "$build_dir/test-sync" -cf - test)
ssh_guest 'cat > /home/omarchy/guest-mac-desktop.sh' < "$review_root/reviews/vm-install/guest-mac-desktop.sh"
ssh_guest 'cat > /home/omarchy/guest-runtime-recovery.sh' < "$review_root/reviews/remediation/guest-runtime-recovery.sh"
status=0
code=0
ssh_guest 'bash /home/omarchy/guest-mac-desktop.sh' > "$RUN_DIR/desktop.log" 2>&1 || code=$?
printf '%s\n' "$code" > "$RUN_DIR/desktop.exit"
((code==0)) || status=1
ssh_guest 'tar -C /home/omarchy -cf - mac-desktop-checks' | tar -C "$RUN_DIR" -xf -
code=0
ssh_sudo 'bash /home/omarchy/guest-runtime-recovery.sh' > "$RUN_DIR/recovery.log" 2>&1 || code=$?
printf '%s\n' "$code" > "$RUN_DIR/recovery.exit"
((code==0)) || status=1

# Keep the real editor failure separate from a baseline-only repair experiment.
# This must never relabel the unchanged ISO's startup check as a pass.
code=0
ssh_guest 'timeout 45 nvim --headless "+lua print(\"NVIM_STARTUP_ERRMSG=\" .. vim.v.errmsg); if vim.v.errmsg ~= \"\" then vim.cmd(\"cquit 1\") end" +qa' > "$RUN_DIR/editor-original.log" 2>&1 || code=$?
printf '%s\n' "$code" > "$RUN_DIR/editor-original.exit"
ssh_guest 'cat > /home/omarchy/editor-repair-check.py' < "$review_root/reviews/remediation/guest-editor-repair-check.py"
code=0
ssh_guest 'python /home/omarchy/editor-repair-check.py' > "$RUN_DIR/editor-candidate.log" 2>&1 || code=$?
printf '%s\n' "$code" > "$RUN_DIR/editor-candidate.exit"
((code==0)) || status=1
capture_console runtime-followups-final
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
printf 'Follow-ups exit %s; original editor result remains separate. Artifacts: %s\n' "$status" "$RUN_DIR"
exit "$status"
