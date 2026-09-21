#!/bin/bash
# Run only inside the disposable Arch container, with task cache mounted.
set -euo pipefail
[[ -f /.dockerenv && -d /evidence && -d /var/cache/intel-mac-build/libfprint-t1bridge/src/build ]]
exec > >(tee /evidence/recheck.log) 2>&1
trap 'result=$?; echo "$result" > /evidence/recheck.exit' EXIT
pacman -Syu --noconfirm --needed base-devel sudo meson glib2-devel gobject-introspection gtk-doc python-cairo python-gobject systemd libgcc glib2 glibc libgudev libgusb openssl pixman cairo umockdev
useradd -m -s /bin/bash builder
printf 'builder ALL=(ALL) NOPASSWD: ALL\n' > /etc/sudoers.d/builder
pacman -Q > /evidence/container-packages.txt
cd /var/cache/intel-mac-build/libfprint-t1bridge
su builder -c 'cd /var/cache/intel-mac-build/libfprint-t1bridge/src && meson test -C build --no-rebuild --num-processes 1 --repeat 3 --print-errorlogs --logbase isolated-recheck egis_etu905'
cp src/build/meson-logs/isolated-recheck.* /evidence/
su builder -c 'cd /var/cache/intel-mac-build/libfprint-t1bridge/src && meson test -C build --no-rebuild --num-processes 1 --repeat 2 --print-errorlogs --logbase full-serial-recheck'
cp src/build/meson-logs/full-serial-recheck.* /evidence/
# Package the same verified source; run its complete check() again, without
# skipping tests or changing drivers, timeouts, or the selected source patch.
su builder -c 'cd /var/cache/intel-mac-build/libfprint-t1bridge && MAKEFLAGS=-j4 MESON_NUM_PROCESSES=1 makepkg --noextract --force --noconfirm'
cp src/build/meson-logs/testlog.* /evidence/
sha256sum ./*.pkg.tar.zst > /evidence/package.sha256
