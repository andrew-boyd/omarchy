#!/bin/bash
# Real boot-image/package operations with explicit model fixtures, inside QEMU.
set -euo pipefail
iso=$(realpath "${1:?Usage: run-migration-scenario.sh ISO spi-pio|kernel-headers}")
scenario=${2:?Choose a migration scenario}
[[ $scenario == spi-pio || $scenario == kernel-headers ]]
build_dir=$(dirname "$iso")
[[ $(cat "$build_dir/build.exit") == 0 ]]
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true
SCENARIO="mac-migration-$scenario"
source "$build_dir/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready || { echo 'Run the ISO integration installer first.' >&2; exit 1; }
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'

status=0
if [[ $scenario == spi-pio ]]; then
  ssh_sudo '
    set -euo pipefail
    test "$(hostname)" = omarchy-test
    test "$(systemd-detect-virt)" = kvm
    export OMARCHY_PATH=/usr/share/omarchy
    printf "MacBook8,1\n" > /tmp/vintage-model
    # Change only the DMI input path. All file writes and boot operations are real.
    sed "s|/sys/class/dmi/id/product_name|/tmp/vintage-model|g" \
      /usr/share/omarchy/install/hardware/apple/fix-spi-keyboard.sh > /tmp/vintage-spi-leaf.sh
    bash -eE -o pipefail /tmp/vintage-spi-leaf.sh
    cat /etc/mkinitcpio.conf.d/macbook_spi_modules.conf
    cat /etc/limine-entry-tool.d/macbook81-spi-pio.conf
    ! pacman -Q macbook12-spi-driver-dkms
    modinfo -k "$(uname -r)" applespi
    export OMARCHY_MACBOOK81_DMI_PRODUCT=/tmp/vintage-model
    bash -euo pipefail /usr/share/omarchy/migrations/1788318101.sh
    test -f /var/lib/omarchy/migrations/1788318101
    find /boot/EFI/Linux -name "*.efi" -type f -exec sha256sum {} + | sort > /tmp/vintage-uki-before
    bash -euo pipefail /usr/share/omarchy/migrations/1788318101.sh
    find /boot/EFI/Linux -name "*.efi" -type f -exec sha256sum {} + | sort > /tmp/vintage-uki-after
    diff -u /tmp/vintage-uki-before /tmp/vintage-uki-after
  ' > "$RUN_DIR/migration.log" 2>&1 || status=$?
else
  ssh_sudo '
    set -euo pipefail
    test "$(hostname)" = omarchy-test
    test "$(systemd-detect-virt)" = kvm
    export OMARCHY_PATH=/usr/share/omarchy
    # Add a real stock fallback and the real Broadcom DKMS package. The
    # candidate migration, rather than this fixture, must supply its headers.
    pacman -Sy --noconfirm
    pacman -S --noconfirm --needed linux broadcom-wl-dkms
    ! pacman -Q linux-headers
    bash -euo pipefail /usr/share/omarchy/migrations/1789546355.sh
    pacman -Q linux linux-headers linux-omarchy linux-omarchy-headers
    for module_dir in /usr/lib/modules/*; do
      test -f "$module_dir/pkgbase" || continue
      test -f "$module_dir/build/Makefile"
      test "$(make -s -C "$module_dir/build" kernelrelease)" = "${module_dir##*/}"
      dkms autoinstall -k "${module_dir##*/}"
    done
    pacman -Q | sort > /tmp/vintage-packages-before
    sha256sum /etc/default/limine > /tmp/vintage-limine-before
    printf "Apple Inc.\n" > /tmp/vintage-vendor
    OMARCHY_KERNEL_DMI_VENDOR=/tmp/vintage-vendor \
      bash -euo pipefail /usr/share/omarchy/migrations/1789325478.sh
    pacman -Q | sort > /tmp/vintage-packages-after
    sha256sum /etc/default/limine > /tmp/vintage-limine-after
    diff -u /tmp/vintage-packages-before /tmp/vintage-packages-after
    diff -u /tmp/vintage-limine-before /tmp/vintage-limine-after
    # Exercise the non-Apple path against the actual guest bootloader too.
    bash -euo pipefail /usr/share/omarchy/migrations/1789325478.sh
    test -f /var/lib/omarchy/migrations/1789325478
    pacman -Q linux linux-headers linux-omarchy linux-omarchy-headers
  ' > "$RUN_DIR/migration.log" 2>&1 || status=$?
fi

if ((status == 0)); then
  ssh_sudo 'systemctl reboot' || true
  sleep 5
  wait_for_ssh "$BOOT_TIMEOUT" || status=$?
  ssh_guest 'cat /proc/cmdline; uname -a; pacman -Q linux-omarchy linux-omarchy-headers' > "$RUN_DIR/reboot.log" 2>&1 || status=$?
  if [[ $scenario == spi-pio ]]; then
    ssh_guest 'grep -q "initcall_blacklist=dw_pci_driver_init" /proc/cmdline && grep -q "mem_sleep_default=s2idle" /proc/cmdline' || status=$?
  else
    ssh_guest 'pacman -Q linux linux-headers && test "$(cat /usr/lib/modules/$(uname -r)/pkgbase)" = linux-omarchy' || status=$?
  fi
fi
ssh_sudo 'cat /boot/limine.conf; cat /var/log/pacman.log; journalctl -b -p warning --no-pager' > "$RUN_DIR/guest-log.txt" 2>&1 || true
ssh_sudo 'dkms status; find /var/lib/dkms -name make.log -exec cat {} +' > "$RUN_DIR/dkms.log" 2>&1 || true
capture_console "migration-$scenario-final"
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
log "Migration scenario exit $status. Artifacts: $RUN_DIR"
exit "$status"
