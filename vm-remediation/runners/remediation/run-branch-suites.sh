#!/bin/bash
# Complete source suites in a disposable installed-ISO guest only.
set -euo pipefail
review_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
wave="$review_root/.state/vm-install/2026-09-20"
iso=$(realpath "${1:?Pass installed base ISO}")
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true OMARCHY_INTEGRATION_MEMORY=4096
SCENARIO=remediation-branch-suites
source "$(dirname "$iso")/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
source "$review_root/reviews/vm-install/guest-session.sh"
establish_guest_desktop
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
ssh_guest 'mkdir -p /home/omarchy/branch-tests'
for name in omarchy-pkgs omarchy-iso integration P03 P05 P06 P07 P09 P10 P11 P13 P14; do
  case "$name" in
    omarchy-pkgs|omarchy-iso) repo="$wave/repos/$name" ;;
    integration) repo="$wave/repos/omarchy" ;;
    *) repo="$wave/remediation/branches/$name" ;;
  esac
  [[ -z $(git -C "$repo" status --porcelain) ]]
  git -C "$repo" rev-parse HEAD > "$RUN_DIR/$name.commit"
  git -C "$repo" archive HEAD | ssh_guest "mkdir -p /home/omarchy/branch-tests/$name && tar -C /home/omarchy/branch-tests/$name -xf -"
done
ssh_guest 'cat > /home/omarchy/guest-full-suite.sh' < "$review_root/reviews/vm-install/guest-full-suite.sh"
status=0
for name in integration P03 P05 P06 P07 P09 P10 P11 P13 P14; do
  code=0
  ssh_guest "bash /home/omarchy/guest-full-suite.sh /home/omarchy/branch-tests/$name" > "$RUN_DIR/$name.log" 2>&1 || code=$?
  printf '%s\n' "$code" > "$RUN_DIR/$name.exit"
  printf '%s full suite: %s\n' "$name" "$code"
  ((code == 0)) || status=1
done
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
printf 'Artifacts: %s\n' "$RUN_DIR"
exit "$status"
