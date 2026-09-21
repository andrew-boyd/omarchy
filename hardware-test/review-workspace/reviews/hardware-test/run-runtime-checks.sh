#!/bin/bash
# Installed checks and source suites run exclusively inside the disposable VM.
set -euo pipefail
review_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
iso=$(realpath "${1:?Pass the rebuilt and installed local ISO}")
build_dir=$(dirname "$iso")
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
export OMARCHY_INTEGRATION_SSH_PORT=2322 OMARCHY_INTEGRATION_MEMORY=4096
SCENARIO=hardware-candidate-runtime
source "$build_dir/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
source "$review_root/reviews/vm-install/guest-session.sh"
establish_guest_desktop
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
python - "$build_dir/installed-runtime-payload.json" <<'PY' |
import json,sys
for row in json.load(open(sys.argv[1])):
    print(row['sha256'] + '  ' + row['path'])
PY
  ssh_guest 'sha256sum -c -' > "$RUN_DIR/installed-payload.log"
ssh_guest 'pacman -Q omarchy-dev omarchy-settings-dev omarchy-nvim linux-omarchy linux-omarchy-headers owe owe-lockfeed omasnap; uname -a' > "$RUN_DIR/inventory.log"
for name in omarchy omarchy-pkgs omarchy-iso; do
  git -C "$build_dir/sources/$name" archive HEAD |
    ssh_guest "mkdir -p /home/omarchy/runtime-sources/$name && tar -C /home/omarchy/runtime-sources/$name -xf -"
done
tar -C "$build_dir/test-sync" -cf - test |
  ssh_guest 'mkdir -p /home/omarchy/.local/share/omarchy && tar -C /home/omarchy/.local/share/omarchy -xf -'
for helper in guest-full-suite.sh guest-mac-desktop.sh; do
  ssh_guest "cat > /home/omarchy/$helper" < "$review_root/reviews/vm-install/$helper"
done
ssh_guest 'cat > /home/omarchy/guest-runtime-recovery.sh' < "$review_root/reviews/remediation/guest-runtime-recovery.sh"
status=0
stage() {
  local name=$1 code=0
  shift
  "$@" > "$RUN_DIR/$name.log" 2>&1 || code=$?
  printf '%s\n' "$code" > "$RUN_DIR/$name.exit"
  ((code == 0)) || status=1
}
stage test-all ssh_guest 'bash /home/omarchy/guest-full-suite.sh /home/omarchy/runtime-sources/omarchy'
stage password-lock python "$review_root/reviews/vm-install/run-guest-lock-check.py" "$BASE_DIR" "$RUN_DIR/password-lock" --port "$SSH_PORT"
stage desktop ssh_guest 'bash /home/omarchy/guest-mac-desktop.sh'
ssh_guest 'tar -C /home/omarchy -cf - mac-desktop-checks' | tar -C "$RUN_DIR" -xf -
stage editor-startup ssh_guest 'timeout 45 nvim --headless "+lua print(\"NVIM_STARTUP_ERRMSG=\" .. vim.v.errmsg); if vim.v.errmsg ~= \"\" then vim.cmd(\"cquit 1\") end" +qa'
stage editor-monokai ssh_guest 'timeout 45 nvim --headless "+lua require(\"monokai-pro\").setup()" "+colorscheme monokai-pro" "+lua print(\"NVIM_THEME_ERRMSG=\" .. vim.v.errmsg); if vim.v.errmsg ~= \"\" then vim.cmd(\"cquit 1\") end" +qa'
stage recovery ssh_sudo 'bash /home/omarchy/guest-runtime-recovery.sh'
stage iso-unit ssh_guest 'cd /home/omarchy/runtime-sources/omarchy-iso && python -m unittest discover -s test/unit -p "test_*.py"'
capture_console success-runtime-final
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
printf 'Runtime checks exit %s. Artifacts: %s\n' "$status" "$RUN_DIR"
exit "$status"
