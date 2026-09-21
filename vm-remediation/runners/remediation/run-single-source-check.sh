#!/bin/bash
# Recheck one observed source-test failure in its own fresh VM overlay.
set -euo pipefail
review_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
wave="$review_root/.state/vm-install/2026-09-20"
iso=$(realpath "${1:?Pass installed ISO}")
name=${2:?Pass branch ID}
test=${3:?Pass observed failing test path}
[[ $name =~ ^(P[0-9]{2}|integration)$ && $test =~ ^test/shell.d/[a-z0-9-]+-test.sh$ ]]
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true OMARCHY_INTEGRATION_MEMORY=4096 OMARCHY_INTEGRATION_SSH_PORT=2522
SCENARIO="recheck-$name-$(basename "$test" .sh)"
source "$(dirname "$iso")/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
source "$review_root/reviews/vm-install/guest-session.sh"
establish_guest_desktop
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
for scope in "$name" omarchy-pkgs omarchy-iso; do
 case "$scope" in
  integration) repo="$wave/repos/omarchy" ;;
  omarchy-pkgs|omarchy-iso) repo="$wave/repos/$scope" ;;
  *) repo="$wave/remediation/branches/$scope" ;;
 esac
 git -C "$repo" rev-parse HEAD > "$RUN_DIR/$scope.commit"
 git -C "$repo" archive HEAD | ssh_guest "mkdir -p /home/omarchy/focused/$scope && tar -C /home/omarchy/focused/$scope -xf -"
done
status=0
ssh_guest "export XDG_RUNTIME_DIR=/run/user/1000; export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus; export WAYLAND_DISPLAY=wayland-1; export HYPRLAND_INSTANCE_SIGNATURE=\$(ls -t /run/user/1000/hypr | head -1); export OMARCHY_PATH=/usr/share/omarchy; unset NO_COLOR LC_ALL; bash /home/omarchy/focused/$name/$test" > "$RUN_DIR/check.log" 2>&1 || status=$?
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
capture_console source-recheck-final
printf '%s %s recheck exit %s. Artifacts: %s\n' "$name" "$test" "$status" "$RUN_DIR"
exit "$status"
