#!/bin/bash
# Boot a new overlay of the failed test guest; preserve its disk and logs.
set -euo pipefail
iso=$(realpath "${1:?Pass the candidate ISO}")
failed=$(realpath "${2:?Pass the failed runtime run directory}")
[[ $(cat "$failed/scenario.exit") == 1 && -f $failed/run.qcow2 ]]
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
export OMARCHY_INTEGRATION_SSH_PORT=2422 OMARCHY_INTEGRATION_MEMORY=2048
SCENARIO=hardware-runtime-failure-inspection
source "$(dirname "$iso")/sources/omarchy-iso/test/integration.d/base-test.sh"
BASE_DISK="$failed/run.qcow2"
BASE_OVMF="$failed/OVMF_VARS.4m.fd"
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
ssh_guest 'faillock --user omarchy; journalctl --list-boots --no-pager' > "$RUN_DIR/account-state.log" 2>&1
status=0
ssh_sudo '
  set -euo pipefail
  journalctl --list-boots --no-pager
  journalctl -b -1 --no-pager | grep -Ei "pam_|faillock|authenticat|sudo|lock-password" || true
  echo "Current boot authentication:"
  journalctl -b --no-pager | grep -Ei "pam_|faillock|authenticat|sudo" || true
  echo "PAM file checksums:"
  find /etc/pam.d -type f -exec sha256sum {} + | sort
  echo "Known test-password comparison (no hash output):"
  entry=$(getent shadow omarchy)
  actual=${entry#*:}; actual=${actual%%:*}
  IFS=\$ read -r _ algorithm salt rest <<< "$actual"
  test "$algorithm" = 6
  expected=$(openssl passwd -6 -salt "$salt" omarchy)
  test "$expected" = "$actual"
  echo "PASS: failed guest retains its original test password"
' > "$RUN_DIR/authentication-history.log" 2>&1 || status=$?
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
printf 'Failure inspection exit %s. Artifacts: %s\n' "$status" "$RUN_DIR"
exit "$status"
