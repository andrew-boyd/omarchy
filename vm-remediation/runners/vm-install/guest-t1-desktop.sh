#!/bin/bash
# Installed T1 desktop adapter on virtual audio; no T1 device is emulated.
set -euo pipefail
[[ $(hostname) == omarchy-test && $(systemd-detect-virt) == kvm && -b /dev/vda ]]
[[ $EUID -ne 0 ]]
export OMARCHY_PATH=/usr/share/omarchy
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"
for attempt in {1..60}; do
  signature=$(ls -t "$XDG_RUNTIME_DIR/hypr" 2>/dev/null | head -n1 || true)
  if [[ -n $signature ]]; then
    export HYPRLAND_INSTANCE_SIGNATURE="$signature"
    export WAYLAND_DISPLAY=$(find "$XDG_RUNTIME_DIR" -maxdepth 1 -type s -name 'wayland-*' -printf '%f\n' | head -n1)
    hyprctl -j monitors >/dev/null 2>&1 && break
  fi
  sleep 2
done
hyprctl -j monitors >/dev/null
mkdir -p "$HOME/t1-desktop-evidence"
evidence="$HOME/t1-desktop-evidence"
provider=/usr/lib/t1bridge-omarchy/desktop-provider
systemctl --user daemon-reload
systemctl --user show t1-touchbar.service -p Environment > "$evidence/service-environment.txt"
grep -Fq 'T1BRIDGE_DESKTOP_PROVIDER=/usr/lib/t1bridge-omarchy/desktop-provider' "$evidence/service-environment.txt"
"$provider" v1 status | tee "$evidence/status-before.txt"
sink=$(omarchy-audio-output-sink)
[[ -n $sink ]]
original_volume=$(pactl get-sink-volume "$sink" | awk 'NR==1 {for(i=1;i<=NF;i++) if($i ~ /%$/) {print $i;exit}}')
original_mute=$(pactl get-sink-mute "$sink" | awk '{print $2}')
restore_audio() {
  pactl set-sink-volume "$sink" "$original_volume"
  pactl set-sink-mute "$sink" "$original_mute"
}
trap restore_audio EXIT
"$provider" v1 set-volume 37
sleep 1
grim "$evidence/volume-osd.png"
"$provider" v1 status | tee "$evidence/status-volume37.txt"
grep -Eq '^T1BRIDGE-DESKTOP 1 [0-9]+ 37 0$' "$evidence/status-volume37.txt"
"$provider" v1 toggle-mute
"$provider" v1 status | tee "$evidence/status-muted.txt"
grep -Eq '^T1BRIDGE-DESKTOP 1 [0-9]+ 37 1$' "$evidence/status-muted.txt"
"$provider" v1 notify-renderer-fallback selection-unavailable
sleep 1
grim "$evidence/renderer-fallback-notification.png"
restore_audio
trap - EXIT
"$provider" v1 status > "$evidence/status-restored.txt"
pacman -Qo /usr/bin/t1bridge /usr/bin/t1-touchid > "$evidence/cli-ownership.txt"
systemctl --user is-enabled t1bridge-auto-brightness.service > "$evidence/auto-brightness-enabled.txt" || true
systemctl --user is-active t1bridge-auto-brightness.service > "$evidence/auto-brightness-active.txt" || true
[[ $(cat "$evidence/auto-brightness-active.txt") != active ]]
echo 'PASS: exact installed desktop provider exposes virtual audio, changes volume, toggles mute, restores audio, and renders OSD/notification. Optional auto-brightness remains inactive.'
