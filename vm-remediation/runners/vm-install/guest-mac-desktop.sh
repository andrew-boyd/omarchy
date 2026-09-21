#!/bin/bash
# Installed-product checks, executed only in the disposable desktop guest.
set -euo pipefail
[[ $(hostname) == omarchy-test && $(systemd-detect-virt) == kvm && -b /dev/vda ]]
[[ $EUID -ne 0 ]]
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"
export WAYLAND_DISPLAY=$(find "$XDG_RUNTIME_DIR" -maxdepth 1 -type s -name 'wayland-*' -printf '%f\n' | head -n1)
export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t "$XDG_RUNTIME_DIR/hypr" | head -n1)
export OMARCHY_PATH=/usr/share/omarchy
export OMARCHY_ACCEPTANCE_DIR="$HOME/mac-desktop-checks"
source "$HOME/.local/share/omarchy/test/acceptance.d/base-test.sh"
lock_status=0
omarchy-hyprland-session-locked || lock_status=$?
[[ $lock_status == 1 ]] || fail "desktop checks start with an unlocked session"

lspci -nnk > "$ARTIFACTS/pci-inventory.txt"
for detector in bcm43xx t2 nvidia facetimehd; do
  status=0
  "omarchy-hw-$detector" || status=$?
  [[ $status == 1 ]] || fail "$detector excludes the real QEMU PCI inventory" "exit $status"
  pass "$detector excludes the real QEMU PCI inventory"
done
pacman -Q | sort > "$ARTIFACTS/packages-before-noop.txt"
for setup in fix-facetimehd fix-bcm43602-nvram fix-spi-keyboard fix-suspend-nvme; do
  # These are sourced installer leaves. Use the actual non-Apple identity.
  source "$OMARCHY_PATH/install/hardware/apple/$setup.sh"
done
pacman -Q | sort > "$ARTIFACTS/packages-after-noop.txt"
diff -u "$ARTIFACTS/packages-before-noop.txt" "$ARTIFACTS/packages-after-noop.txt"
[[ ! -e /etc/systemd/system/omarchy-nvme-suspend-fix.service ]]
[[ ! -e /etc/mkinitcpio.conf.d/macbook_spi_modules.conf ]]
pass "non-Apple hardware setup leaves package and hardware configuration unchanged"

watcher=$(pgrep -f '^/bin/bash /usr/share/omarchy/bin/omarchy-hyprland-monitor-watch$' | head -n1)
[[ -n $watcher ]]
omarchy-monitor-state > "$ARTIFACTS/monitor-state-before.txt"
hyprctl -j monitors > "$ARTIFACTS/monitors-before.json"
omarchy-hyprland-monitor-disable-ghosts
hyprctl reload >/dev/null
sleep 3
kill -0 "$watcher"
hyprctl -j monitors > "$ARTIFACTS/monitors-after.json"
jq -e 'length == 1 and .[0].name == "Virtual-1" and .[0].width > 0 and .[0].height > 0 and .[0].disabled == false' "$ARTIFACTS/monitors-after.json" >/dev/null
status=0
omarchy-hyprland-monitor-modeless || status=$?
[[ $status == 1 ]]
omarchy-monitor-state > "$ARTIFACTS/monitor-state-after.txt"
pass "installed monitor watcher survives reload and preserves the working virtual output"
omarchy-shell shell summon omarchy.monitor >/dev/null
sleep 2
screenshot success-monitor-panel
omarchy-shell shell hide omarchy.monitor >/dev/null

input_config="$HOME/.config/hypr/input.lua"
cp "$input_config" "$ARTIFACTS/input.lua.before"
restore_layout() {
  cp "$ARTIFACTS/input.lua.before" "$input_config"
  hyprctl reload >/dev/null || true
}
trap restore_layout EXIT
printf '\nhl.config({ input = { kb_layout = "us,de" } })\n' >> "$input_config"
hyprctl reload >/dev/null
sleep 3
hyprctl -j devices > "$ARTIFACTS/keyboards-before.json"
keyboard=$(jq -r '.keyboards[] | select(.name == "at-translated-set-2-keyboard") | .name' "$ARTIFACTS/keyboards-before.json")
[[ -n $keyboard ]]
hyprctl switchxkblayout "$keyboard" 0 >/dev/null
sleep 2
screenshot success-layout-en
hyprctl switchxkblayout "$keyboard" 1 >/dev/null
sleep 2
hyprctl -j devices > "$ARTIFACTS/keyboards-german.json"
jq -e --arg kb "$keyboard" '.keyboards[] | select(.name == $kb) | .active_keymap == "German" and .active_layout_index == 1' "$ARTIFACTS/keyboards-german.json" >/dev/null
screenshot success-layout-de
hyprctl switchxkblayout "$keyboard" 0 >/dev/null
sleep 2
screenshot success-layout-en-restored
pass "the installed desktop switches a real virtual keyboard US to German and back"
restore_layout
trap - EXIT
omarchy-diagnose-suspend-wake status > "$ARTIFACTS/suspend-status.txt"
pass "installed suspend diagnostics enumerate the guest wake sources"
