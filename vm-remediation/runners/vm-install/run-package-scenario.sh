#!/bin/bash
# Real package transactions and DKMS builds in disposable installed-ISO guests.
set -euo pipefail

review_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
wave="$review_root/.state/vm-install/2026-09-20"
iso=$(realpath "${1:?Usage: run-package-scenario.sh ISO camera|audio12|audio-pro|t1bridge}")
scenario=${2:?Choose a package scenario}
case $scenario in
  camera) packages=(facetimehd-firmware facetimehd-data facetimehd-dkms) ;;
  audio12) packages=(macbook12-audio-driver-dkms) ;;
  audio-pro) packages=(snd-hda-macbookpro-dkms) ;;
  t1bridge) packages=(libfprint-t1bridge fprintd-t1bridge t1bridge-dkms t1bridge t1bridge-omarchy) ;;
  *) echo "Unknown package scenario: $scenario" >&2; exit 2 ;;
esac
build_dir=$(dirname "$iso")
[[ $(cat "$build_dir/build.exit") == 0 && -s $build_dir/package-sha256sums ]]

export OMARCHY_INTEGRATION_ISO="$iso"
export OMARCHY_INTEGRATION_NO_PREVIEW=true
SCENARIO="mac-packages-$scenario"
# Reuse the repository's VM lifecycle and its installed, unencrypted base.
source "$build_dir/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready || { echo 'Run the ISO integration installer first.' >&2; exit 1; }

mirror="$wave/cache/iso/airootfs/var/cache/omarchy/mirror/offline"
stage="$RUN_DIR/packages"
mkdir -p "$stage"
for package in "${packages[@]}"; do
  found=0
  for artifact in "$mirror/$package-"*.pkg.tar.zst; do
    [[ -f $artifact ]] || continue
    read -r name version < <(pacman -Qp "$artifact")
    [[ $name == "$package" ]] || continue
    ((found += 1))
    filename=$(basename "$artifact")
    expected=$(awk -v file="$filename" '$2 == file { print $1 }' "$build_dir/package-sha256sums")
    [[ $expected =~ ^[a-f0-9]{64}$ ]]
    actual=$(sha256sum "$artifact")
    [[ ${actual%% *} == "$expected" ]] || { echo "Archive changed since ISO build: $filename" >&2; exit 1; }
    cp --reflink=auto "$artifact" "$stage/"
    printf '%s  %s\n' "$expected" "$filename" >> "$stage/SHA256SUMS"
    printf '%s %s\n' "$name" "$version" >> "$stage/expected-packages"
  done
  ((found == 1)) || { echo "Expected one archive for $package; found $found" >&2; exit 1; }
done

start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
# Never run a package transaction unless the SSH destination proves it is our VM.
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
if [[ $scenario == audio12 ]]; then
  ssh_guest '! pacman -Q linux-headers && ! pacman -Q linux' > "$RUN_DIR/header-baseline.log" 2>&1
  python3 - "$review_root/reviews/vm-install/installed-runtime-payload.json" <<'PY' | ssh_guest 'sha256sum -c -' > "$RUN_DIR/runtime-payload.log"
import json, sys
for row in json.load(open(sys.argv[1])):
    print(row['sha256'] + '  ' + row['path'])
PY
  ssh_guest 'pacman -Q omarchy-dev omarchy-settings-dev linux-omarchy linux-omarchy-headers; lsblk -f' > "$RUN_DIR/runtime-inventory.log"
fi
ssh_sudo 'find /etc/pam.d -type f -exec sha256sum {} + | sort' > "$RUN_DIR/pam-before.txt"
tar -C "$stage" -cf - . | ssh_guest 'mkdir -p /home/omarchy/vintage-packages && tar -C /home/omarchy/vintage-packages -xf -'
ssh_guest 'cd /home/omarchy/vintage-packages && sha256sum -c SHA256SUMS' > "$RUN_DIR/archive-verification.log"

status=0
ssh_sudo '
  set -euo pipefail
  test "$(hostname)" = omarchy-test
  test "$(systemd-detect-virt)" = kvm
  # The alpm download user cannot traverse the private desktop home.
  install -d -m755 /var/cache/vintage-packages
  cp -a /home/omarchy/vintage-packages/. /var/cache/vintage-packages/
  chmod -R a+rX /var/cache/vintage-packages
  cd /var/cache/vintage-packages
  repo-add vintage-test.db.tar.gz ./*.pkg.tar.zst
  awk "
    !added && /^\\[core\\]/ {
      print \"[vintage-test]\\nSigLevel = Never\\nServer = file:///var/cache/vintage-packages\\n\"
      added = 1
    }
    { print }
  " /etc/pacman.conf > /tmp/vintage-pacman.conf
  mapfile -t targets < <(awk "{print \$1 \"=\" \$2}" expected-packages)
  pacman --config /tmp/vintage-pacman.conf -Sy --noconfirm
  pacman --config /tmp/vintage-pacman.conf -Sp --print-format "%n %v" "${targets[@]}"
  if [[ ${targets[0]} == snd-hda-macbookpro-dkms=* ]]; then
    # Exercise the installed positive setup path, including its actual helper
    # and dependency resolution. Only the DMI input is a fixture.
    ! pacman -Q linux-headers
    ! pacman -Q linux
    cp /etc/pacman.conf /tmp/vintage-original-pacman.conf
    trap "cp /tmp/vintage-original-pacman.conf /etc/pacman.conf" EXIT
    cp /tmp/vintage-pacman.conf /etc/pacman.conf
    printf "MacBookPro14,3\n" > /tmp/vintage-audio-model
    export OMARCHY_DMI_PRODUCT_NAME=/tmp/vintage-audio-model
    export OMARCHY_PATH=/usr/share/omarchy OMARCHY_INSTALL=/usr/share/omarchy/install
    source "$OMARCHY_INSTALL/hardware/apple/fix-cs8409-audio.sh"
    bash -euo pipefail "$OMARCHY_PATH/migrations/1786889011.sh"
    ! pacman -Q linux-headers
    ! pacman -Q linux
    cp /tmp/vintage-original-pacman.conf /etc/pacman.conf
    trap - EXIT
  else
    pacman --config /tmp/vintage-pacman.conf -S --noconfirm --needed "${targets[@]}"
  fi
  while read -r name version; do
    test "$(pacman -Q "$name")" = "$name $version"
  done < expected-packages
  kernel=$(uname -r)
  test -f "/usr/lib/modules/$kernel/build/Makefile"
  test "$(make -s -C "/usr/lib/modules/$kernel/build" kernelrelease)" = "$kernel"
  dkms autoinstall -k "$kernel"
  dkms status
' > "$RUN_DIR/package-install.log" 2>&1 || status=$?

if [[ $scenario == audio12 ]] && ((status == 0)); then
  ssh_guest '
    set -euo pipefail
    test "$(pacman -Q macbook12-audio-driver-dkms)" = "macbook12-audio-driver-dkms 0.1-2"
    ! pacman -Q linux-headers
    ! pacman -Q linux
    dkms status | grep -F "macbook12-audio-driver/0.1, $(uname -r), x86_64: installed"
  ' > "$RUN_DIR/audio-header-regression.log" 2>&1 || status=$?
  if grep -Ei 'ERROR:|error: command failed|Missing .*kernel modules tree' "$RUN_DIR/package-install.log" > "$RUN_DIR/audio-hook-errors.log"; then
    status=1
  fi
fi

if ((status == 0)); then
  ssh_sudo 'systemctl reboot' || true
  sleep 5
  wait_for_ssh "$BOOT_TIMEOUT" || status=$?
  ssh_guest 'uname -a; pacman -Q linux-omarchy linux-omarchy-headers; dkms status' > "$RUN_DIR/reboot.log" 2>&1 || status=$?
  ssh_sudo 'find /etc/pam.d -type f -exec sha256sum {} + | sort' > "$RUN_DIR/pam-after.txt"
  diff -u "$RUN_DIR/pam-before.txt" "$RUN_DIR/pam-after.txt" > "$RUN_DIR/pam-diff.txt" || status=$?
fi

if [[ $scenario == t1bridge ]] && ((status == 0)); then
  source "$review_root/reviews/vm-install/guest-session.sh"
  establish_guest_desktop || status=$?
  ssh_guest 'cat > /home/omarchy/guest-t1-desktop.sh' < "$review_root/reviews/vm-install/guest-t1-desktop.sh"
  ssh_guest 'bash /home/omarchy/guest-t1-desktop.sh' > "$RUN_DIR/t1-desktop.log" 2>&1 || status=$?
  ssh_guest 'tar -C /home/omarchy -cf - t1-desktop-evidence' | tar -C "$RUN_DIR" -xf - || true
  python3 "$review_root/reviews/vm-install/run-guest-lock-check.py" "$BASE_DIR" "$RUN_DIR/lock-check" --port "$SSH_PORT" > "$RUN_DIR/lock-check.log" 2>&1 || status=$?
  # Real removal transaction with replacement packages already installed. The
  # DMI fixture exercises initramfs setup, not physical T1 provisioning/handoff.
  legacy="$wave/legacy-packages/macbook12-spi-driver-dkms-0+git.315-1-x86_64.pkg.tar.zst"
  [[ $(sha256sum "$legacy") == 96f20ea661cd3ba13a1b107fa989ff302b3ed6450d3c3975bd2a146634927334* ]]
  ssh_guest 'cat > /home/omarchy/legacy-spi.pkg.tar.zst' < "$legacy"
  ssh_sudo '
    set -euo pipefail
    test "$(hostname)" = omarchy-test
    test "$(systemd-detect-virt)" = kvm
    export OMARCHY_PATH=/usr/share/omarchy
    printf "MacBookPro13,3\n" > /tmp/vintage-spi-model
    sed "s|/sys/class/dmi/id/product_name|/tmp/vintage-spi-model|g" \
      /usr/share/omarchy/install/hardware/apple/fix-spi-keyboard.sh > /tmp/vintage-spi-setup.sh
    bash -euo pipefail /tmp/vintage-spi-setup.sh
    limine-mkinitcpio
    native=$(modinfo -n applespi)
    test "${native#*/kernel/}" != "$native"
    sha256sum "$native" > /tmp/vintage-native-spi.sha256
    pacman -Q t1bridge-dkms t1bridge t1bridge-omarchy libfprint-t1bridge fprintd-t1bridge > /tmp/vintage-t1-before
    pacman -U --noconfirm /home/omarchy/legacy-spi.pkg.tar.zst
    pacman -Q macbook12-spi-driver-dkms
    export OMARCHY_SPI_DMI_PRODUCT=/tmp/vintage-spi-model
    bash /usr/share/omarchy/migrations/1788476400.sh
    ! pacman -Q macbook12-spi-driver-dkms
    bash /usr/share/omarchy/migrations/1788476400.sh
    pacman -Q t1bridge-dkms t1bridge t1bridge-omarchy libfprint-t1bridge fprintd-t1bridge > /tmp/vintage-t1-after
    diff -u /tmp/vintage-t1-before /tmp/vintage-t1-after
    sha256sum -c /tmp/vintage-native-spi.sha256
    dkms autoinstall -k "$(uname -r)"
    dkms status
    echo "PASS: repeated real legacy SPI removal preserves native applespi and the five replacement packages. Physical T1 provisioning/handoff is not emulated."
  ' > "$RUN_DIR/spi-retirement.log" 2>&1 || status=$?
fi

# Preserve diagnostics even when pacman hooks or a driver compile fail.
ssh_sudo '
  uname -a
  pacman -Q
  dkms status
  systemctl --failed --no-pager
  find "/usr/lib/modules/$(uname -r)/updates/dkms" -type f -print 2>/dev/null
' > "$RUN_DIR/installed-state.log" 2>&1 || true
ssh_sudo '
  find /var/lib/dkms -name make.log -print0 | tar --null -T - -cf -
' | tar -C "$RUN_DIR" -xf - || true
ssh_sudo 'cat /var/log/pacman.log; journalctl -b -p warning --no-pager' > "$RUN_DIR/guest-log.txt" 2>&1 || true
capture_console "package-$scenario-final"
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
log "Package scenario exit $status. Artifacts: $RUN_DIR"
exit "$status"
