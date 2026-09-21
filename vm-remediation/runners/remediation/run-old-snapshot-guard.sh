#!/bin/bash
set -euo pipefail
review_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
wave="$review_root/.state/vm-install/2026-09-20"
iso=$(realpath "${1:?Pass old installed ISO}")
new_build=$(realpath "${2:?Pass the new build directory}")
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
SCENARIO=old-snapshot-refusal
source "$(dirname "$iso")/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready
# Reuse only the existing test's terminal driver functions, without its reset.
helpers=$(mktemp)
cleanup_old_guard() {
  local status=$?
  rm -f "$helpers"
  cleanup
  return "$status"
}
trap cleanup_old_guard EXIT
python - "$new_build/sources/omarchy-iso/test/integration.d/factory-reset-test.sh" > "$helpers" <<'PY'
import sys,re
s=open(sys.argv[1]).read()
for name in ['start_reset','reset_output','wait_for_reset_output']:
 print(re.search(r'^'+name+r'\(\) \{\n.*?^\}',s,re.M|re.S).group(0))
PY
source "$helpers"
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
ssh_guest 'cat > /home/omarchy/new-reset-command' < "$new_build/sources/omarchy/bin/omarchy-system-factory-reset"
ssh_sudo 'install -m755 /home/omarchy/new-reset-command /usr/bin/omarchy-system-factory-reset'
ssh_sudo 'sha256sum /boot/limine.conf /etc/passwd /etc/shadow /etc/machine-id; find /boot -type f -exec sha256sum {} + | sort' > "$RUN_DIR/before.sha256"
start_reset
wait_for_reset_output "Type .reset. to continue" 60
ssh_guest "printf 'reset\r' >/tmp/reset.in"
# The expected refusal itself includes Error:, so poll directly.
for attempt in {1..60}; do
 reset_output > "$RUN_DIR/reset.out"
 grep -q 'COMMAND_EXIT_CODE=' "$RUN_DIR/reset.out" && break
 sleep 2
done
grep -q 'the factory snapshot lacks shared-ESP-safe provisioning' "$RUN_DIR/reset.out"
grep -q 'COMMAND_EXIT_CODE="1"' "$RUN_DIR/reset.out"
ssh_sudo 'sha256sum /boot/limine.conf /etc/passwd /etc/shadow /etc/machine-id; find /boot -type f -exec sha256sum {} + | sort' > "$RUN_DIR/after.sha256"
diff -u "$RUN_DIR/before.sha256" "$RUN_DIR/after.sha256"
ssh_sudo '! mountpoint -q /run/omarchy-system-factory-reset/top'
echo 'PASS: new reset refuses the old factory snapshot before account, identity or ESP changes; temporary mount cleaned.'
printf '0\n' > "$RUN_DIR/scenario.exit"
printf 'Artifacts: %s\n' "$RUN_DIR"
