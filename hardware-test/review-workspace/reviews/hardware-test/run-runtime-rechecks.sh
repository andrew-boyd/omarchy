#!/bin/bash
# Recheck only the failed installed checks in a fresh overlay of the same ISO.
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
iso=$(realpath "${1:?Pass the installed candidate ISO}")
build=$(dirname "$iso")
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
export OMARCHY_INTEGRATION_SSH_PORT=2422 OMARCHY_INTEGRATION_MEMORY=3072
SCENARIO=hardware-runtime-clean-rechecks
source "$build/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
source "$root/reviews/vm-install/guest-session.sh"
establish_guest_desktop
ssh_guest 'faillock --user omarchy; journalctl --user -b --no-pager -n 100' > "$RUN_DIR/before.log" 2>&1
ssh_sudo 'true; journalctl -b --no-pager | grep -E "pam_|faillock|sudo" || true' > "$RUN_DIR/sudo-baseline.log" 2>&1
python - "$build/installed-runtime-payload.json" <<'PY' |
import json,sys
for row in json.load(open(sys.argv[1])):
    print(row['sha256'] + '  ' + row['path'])
PY
  ssh_guest 'sha256sum -c -' > "$RUN_DIR/installed-payload.log"
tar -C "$build/test-sync" -cf - test |
  ssh_guest 'mkdir -p /home/omarchy/.local/share/omarchy && tar -C /home/omarchy/.local/share/omarchy -xf -'
ssh_guest 'cat > /home/omarchy/guest-mac-desktop.sh' < "$root/reviews/vm-install/guest-mac-desktop.sh"
ssh_guest 'cat > /home/omarchy/guest-runtime-recovery.sh' < "$root/reviews/remediation/guest-runtime-recovery.sh"
status=0
stage() {
  local name=$1 code=0
  shift
  "$@" > "$RUN_DIR/$name.log" 2>&1 || code=$?
  printf '%s\n' "$code" > "$RUN_DIR/$name.exit"
  ((code == 0)) || status=1
}
stage password-lock python "$root/reviews/vm-install/run-guest-lock-check.py" "$BASE_DIR" "$RUN_DIR/password-lock" --port "$SSH_PORT"
stage desktop ssh_guest 'bash /home/omarchy/guest-mac-desktop.sh'
ssh_guest 'tar -C /home/omarchy -cf - mac-desktop-checks' | tar -C "$RUN_DIR" -xf -
stage recovery ssh_sudo 'bash /home/omarchy/guest-runtime-recovery.sh'
ssh_guest 'faillock --user omarchy; journalctl --user -b --no-pager -n 100' > "$RUN_DIR/after.log" 2>&1
ssh_sudo 'journalctl -b --no-pager | grep -E "pam_|faillock|sudo" || true' > "$RUN_DIR/authentication.log" 2>&1 || true
capture_console runtime-clean-recheck-final
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
printf 'Clean runtime rechecks exit %s. Artifacts: %s\n' "$status" "$RUN_DIR"
exit "$status"
