#!/bin/bash
set -euo pipefail
review_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
wave="$review_root/.state/vm-install/2026-09-20"
iso=$(realpath "${1:?Pass final installed ISO}")
build_dir=$(dirname "$iso")
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
SCENARIO=remediation-runtime
source "$build_dir/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
source "$review_root/reviews/vm-install/guest-session.sh"
establish_guest_desktop
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
python - "$build_dir/installed-runtime-payload.json" <<'PY' | ssh_guest 'sha256sum -c -' > "$RUN_DIR/installed-payload.log"
import json,sys
for r in json.load(open(sys.argv[1])): print(r['sha256']+'  '+r['path'])
PY
ssh_guest 'pacman -Q omarchy-dev omarchy-settings-dev linux-omarchy linux-omarchy-headers; uname -a' > "$RUN_DIR/inventory.log"
for name in omarchy omarchy-pkgs omarchy-iso; do
 git -C "$build_dir/sources/$name" archive HEAD | ssh_guest "mkdir -p /home/omarchy/runtime-sources/$name && tar -C /home/omarchy/runtime-sources/$name -xf -"
done
sha256sum "$review_root/reviews/remediation/preinstalls-sigpipe.patch" > "$RUN_DIR/test-only-patch.sha256"
ssh_guest 'cd /home/omarchy/runtime-sources/omarchy && git apply -' < "$review_root/reviews/remediation/preinstalls-sigpipe.patch"
ssh_guest 'mkdir -p /home/omarchy/.local/share/omarchy && tar -C /home/omarchy/.local/share/omarchy -xf -' < <(tar -C "$build_dir/test-sync" -cf - test)
for helper in guest-full-suite.sh guest-mac-desktop.sh; do
 ssh_guest "cat > /home/omarchy/$helper" < "$review_root/reviews/vm-install/$helper"
done
ssh_guest 'cat > /home/omarchy/guest-runtime-recovery.sh' < "$review_root/reviews/remediation/guest-runtime-recovery.sh"
status=0
code=0
ssh_guest 'bash /home/omarchy/guest-full-suite.sh /home/omarchy/runtime-sources/omarchy' > "$RUN_DIR/test-all.log" 2>&1 || code=$?
printf '%s\n' "$code" > "$RUN_DIR/test-all.exit"
((code==0)) || status=1
code=0
ssh_guest 'bash /home/omarchy/guest-mac-desktop.sh' > "$RUN_DIR/desktop.log" 2>&1 || code=$?
printf '%s\n' "$code" > "$RUN_DIR/desktop.exit"
((code==0)) || status=1
ssh_guest 'tar -C /home/omarchy -cf - mac-desktop-checks' | tar -C "$RUN_DIR" -xf -
code=0
ssh_guest 'timeout 45 nvim --headless "+lua print(\"NVIM_STARTUP_ERRMSG=\" .. vim.v.errmsg); if vim.v.errmsg ~= \"\" then vim.cmd(\"cquit 1\") end" +qa' > "$RUN_DIR/editor-startup.log" 2>&1 || code=$?
printf '%s\n' "$code" > "$RUN_DIR/editor-startup.exit"
((code==0)) || status=1
code=0
ssh_sudo 'bash /home/omarchy/guest-runtime-recovery.sh' > "$RUN_DIR/recovery.log" 2>&1 || code=$?
printf '%s\n' "$code" > "$RUN_DIR/recovery.exit"
((code==0)) || status=1
capture_console success-runtime-final
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
printf 'Runtime checks exit %s. Artifacts: %s\n' "$status" "$RUN_DIR"
exit "$status"
