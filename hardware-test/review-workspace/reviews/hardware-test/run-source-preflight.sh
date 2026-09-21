#!/bin/bash
# Check revised source in a disposable prior-ISO guest; this is not a new-ISO pass.
set -euo pipefail
review_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
iso=$(realpath "${1:?Pass the previously installed ISO}")
prepared=$(realpath "${2:?Pass the immutable revised build directory}")
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
export OMARCHY_INTEGRATION_SSH_PORT=2522 OMARCHY_INTEGRATION_MEMORY=4096
SCENARIO=hardware-source-preflight
source "$(dirname "$iso")/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
for repo in omarchy omarchy-pkgs omarchy-iso; do
  git -C "$prepared/sources/$repo" rev-parse HEAD > "$RUN_DIR/$repo.commit"
  git -C "$prepared/sources/$repo" archive HEAD |
    ssh_guest "mkdir -p /home/omarchy/hardware-sources/$repo && tar -C /home/omarchy/hardware-sources/$repo -xf -"
done
status=0
code=0
ssh_guest 'cd /home/omarchy/hardware-sources/omarchy && bash test/shell.d/brcmfmac-suspend-test.sh' > "$RUN_DIR/broadcom.log" 2>&1 || code=$?
printf '%s\n' "$code" > "$RUN_DIR/broadcom.exit"
((code == 0)) || status=1
code=0
ssh_guest 'cd /home/omarchy/hardware-sources/omarchy-iso && python -m unittest test.unit.test_apple_efi' > "$RUN_DIR/apple-efi.log" 2>&1 || code=$?
printf '%s\n' "$code" > "$RUN_DIR/apple-efi.exit"
((code == 0)) || status=1
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
printf 'Source-only preflight exit %s; artifacts: %s\n' "$status" "$RUN_DIR"
exit "$status"
