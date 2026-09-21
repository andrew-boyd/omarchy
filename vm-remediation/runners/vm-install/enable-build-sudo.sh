#!/bin/bash
# Explicit, temporary exception requested by Boyd for unattended ISO builds.
# Install once from the user's terminal with sudo; no SSH changes are needed.
set -euo pipefail
umask 077

build_user=boyd
rule=/etc/sudoers.d/zz-vintage-iso-build
marker='# Temporary Vintage ISO build access; managed by enable-build-sudo.sh'
expires=$(/usr/bin/date -u -d '+4 hours' +%Y%m%d%H%M%SZ)

render_rule() {
  printf '%s\n' "$marker"
  printf '# Docker is root-equivalent. New sudo invocations expire after four hours.\n'
  printf '%s ALL=(root) NOTAFTER=%s NOPASSWD: /usr/bin/docker\n' "$build_user" "$expires"
}

if [[ ${1:-} == "--print" && $# == 1 ]]; then
  render_rule
  exit 0
fi
if (( $# )); then
  echo "Usage: sudo bash $0  (or bash $0 --print to preview)" >&2
  exit 1
fi
if (( EUID != 0 )); then
  echo "Run once in your terminal: sudo bash $0" >&2
  exit 1
fi
if [[ ${SUDO_USER:-} != "$build_user" ]]; then
  echo "Run through interactive sudo from the boyd account." >&2
  exit 1
fi

/usr/bin/visudo -c
if [[ -L $rule || ( -e $rule && ! -f $rule ) ]]; then
  echo "Refusing a non-regular sudoers destination: $rule" >&2
  exit 1
fi
if [[ -e $rule ]] && ! /usr/bin/grep -Fxq "$marker" "$rule"; then
  echo "Refusing to replace an unrelated sudoers rule: $rule" >&2
  exit 1
fi

candidate=$(/usr/bin/mktemp /etc/sudoers.d/.vintage-iso-candidate.XXXXXX)
previous=""
installed=false
cleanup() {
  local result=$?
  if (( result != 0 )) && $installed; then
    if [[ -n $previous ]]; then
      /usr/bin/mv -fT -- "$previous" "$rule"
      previous=""
    else
      /usr/bin/rm -f -- "$rule"
    fi
    echo "Validation failed; restored the previous sudo policy." >&2
  fi
  [[ -z $candidate ]] || /usr/bin/rm -f -- "$candidate"
  [[ -z $previous ]] || /usr/bin/rm -f -- "$previous"
}
trap cleanup EXIT

render_rule > "$candidate"
/usr/bin/chmod 0440 "$candidate"
/usr/bin/chown root:root "$candidate"
/usr/bin/visudo -cf "$candidate"
if [[ -e $rule ]]; then
  previous=$(/usr/bin/mktemp /etc/sudoers.d/.vintage-iso-previous.XXXXXX)
  /usr/bin/cp -p -- "$rule" "$previous"
fi
/usr/bin/mv -fT -- "$candidate" "$rule"
candidate=""
installed=true
/usr/bin/visudo -c

# Verify the actual account can reach Docker without a prompt. This does not
# launch a container or change the running build.
/usr/bin/runuser -u "$build_user" -- /usr/bin/sudo -n /usr/bin/docker version \
  --format 'Docker server: {{.Server.Version}}'

printf '\nPasswordless Docker access expires at %s UTC.\n' "$expires"
printf 'Revoke earlier: sudo rm -f %s\n' "$rule"
