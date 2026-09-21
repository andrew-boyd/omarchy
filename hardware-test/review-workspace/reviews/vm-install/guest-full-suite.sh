#!/bin/bash
# Run over SSH only inside the disposable guest, after its desktop has started.
set -euo pipefail
[[ $(hostname) == omarchy-test && $(systemd-detect-virt) == kvm && -b /dev/vda ]]
[[ $EUID -ne 0 ]]
suite=${1:?Pass the complete source snapshot staged inside this guest}
[[ -f $suite/test/all ]]
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"
session_environment=$(systemctl --user show-environment)
for variable in WAYLAND_DISPLAY DISPLAY HYPRLAND_INSTANCE_SIGNATURE LANG; do
  value=$(sed -n "s/^$variable=//p" <<< "$session_environment" | head -n 1)
  if [[ -n $value ]]; then
    export "$variable=$value"
  fi
done
if [[ -z ${HYPRLAND_INSTANCE_SIGNATURE:-} ]]; then
  export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t "$XDG_RUNTIME_DIR/hypr" | head -n 1)
fi
if [[ -z ${WAYLAND_DISPLAY:-} ]]; then
  export WAYLAND_DISPLAY=$(find "$XDG_RUNTIME_DIR" -maxdepth 1 -type s -name 'wayland-*' -printf '%f\n' | head -n 1)
fi
[[ -n ${WAYLAND_DISPLAY:-} && -S $XDG_RUNTIME_DIR/$WAYLAND_DISPLAY ]]
[[ -n ${HYPRLAND_INSTANCE_SIGNATURE:-} ]]
hyprctl -j monitors >/dev/null
export OMARCHY_PATH=/usr/share/omarchy PYTHONDONTWRITEBYTECODE=1
unset NO_COLOR LC_ALL
umask 022
bash "$suite/test/all"
