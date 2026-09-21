#!/bin/bash
# Source after the ISO integration harness. Login is through QMP, not autologin.
guest_session_ready() {
  ssh_guest '
    export XDG_RUNTIME_DIR=/run/user/$(id -u)
    signature=$(ls -t "$XDG_RUNTIME_DIR/hypr" 2>/dev/null | head -n1)
    test -n "$signature" || exit 1
    export HYPRLAND_INSTANCE_SIGNATURE="$signature"
    hyprctl -j monitors >/dev/null
  ' >/dev/null 2>&1
}

establish_guest_desktop() {
  local attempt
  sleep 5
  for attempt in {1..12}; do
    if guest_session_ready; then
      capture_console success-guest-desktop-login
      return 0
    fi
    capture_console "guest-greeter-$attempt"
    press ctrl-a
    press backspace
    type_text "$GUEST_PASSWORD"
    press ret
    sleep 10
  done
  echo 'Guest SSH is available but the graphical user login did not complete.' >&2
  return 1
}
