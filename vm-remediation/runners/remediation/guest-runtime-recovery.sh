#!/bin/bash
# Actual privileged command/state behavior, only inside the disposable guest.
set -euo pipefail
[[ $(hostname) == omarchy-test && $(systemd-detect-virt) == kvm && -b /dev/vda && $EUID == 0 ]]
export OMARCHY_PATH=/usr/share/omarchy
command=/usr/share/omarchy/bin/omarchy-diagnose-suspend-wake
state=/run/omarchy-diagnose-suspend-wake
[[ ! -e $state ]]
"$command" restore
[[ $(stat -c %u:%a "$state") == 0:700 && $(stat -c %u:%a "$state/lock") == 0:600 ]]
echo 'PASS: actual privileged state directory and lock are root-owned/private'
# A concurrent command must fail before it starts sleep or writes devices.
(
  exec 9>"$state/lock"
  flock -n 9
  if "$command" test 10; then exit 1; fi
)
echo 'PASS: actual lock rejects a concurrent test'
chmod 755 "$state"
if "$command" restore; then exit 1; fi
chmod 700 "$state"
echo 'PASS: unsafe directory permissions are rejected'
fixture=$(mktemp -d /tmp/vintage-recovery.XXXXXX)
mkdir -p "$fixture/good/power" "$fixture/retry/power"
printf 'disabled\n' > "$fixture/good/power/wakeup"
printf 'GOOD\tusb\t%s/good/\nRETRY\tusb\t%s/retry/\n' "$fixture" "$fixture" > "$state/pending"
if "$command" restore; then exit 1; fi
[[ $(cat "$fixture/good/power/wakeup") == enabled ]]
[[ $(cat "$state/pending") == $(printf 'RETRY\tusb\t%s/retry/' "$fixture") ]]
if "$command" diagnose 10 <<< n; then exit 1; fi
printf 'disabled\n' > "$fixture/retry/power/wakeup"
"$command" restore
[[ ! -e $state/pending && $(cat "$fixture/retry/power/wakeup") == enabled ]]
echo 'PASS: actual installed restore retains only failed device records and retries them'
# Exercise command failure propagation through the actual installed entry point.
mkdir "$fixture/bin"
printf '#!/bin/bash\nexit 7\n' > "$fixture/bin/rtcwake"
chmod 755 "$fixture/bin/rtcwake"
if PATH="$fixture/bin:$PATH" "$command" test 10; then exit 1; fi
echo 'PASS: failed RTC command returns failure without a false success report'
# No device wake settings are changed by test; this is actual virtual S3/RTC.
before=$(date +%s)
"$command" test 10
after=$(date +%s)
((after-before>=7))
journalctl -b --since "@$before" --no-pager | grep -E 'PM: suspend entry|PM: suspend exit|PM: Low-level resume'
[[ ! -e $state/pending ]]
echo 'PASS: actual guest RTC sleep/resume and recovery-state cleanup'

# The virtual guest has no Broadcom device. Exercise the installed hook's
# real root-state/locking/error paths without substituting its file operations.
[[ ! -e /sys/bus/pci/drivers/brcmfmac ]]
hook=/usr/share/omarchy/default/systemd/system-sleep/rebind-brcmfmac
export OMARCHY_BRCMFMAC_SLEEP_STATE=/run/vintage-brcmfmac-check
bash "$hook" pre suspend
[[ $(stat -c %u:%a "$OMARCHY_BRCMFMAC_SLEEP_STATE") == 0:600 ]]
bash "$hook" post suspend
[[ ! -e $OMARCHY_BRCMFMAC_SLEEP_STATE ]]
printf '0000:ff:00.0\n' > "$OMARCHY_BRCMFMAC_SLEEP_STATE"
bash "$hook" pre suspend
[[ $(cat "$OMARCHY_BRCMFMAC_SLEEP_STATE") == 0000:ff:00.0 ]]
if bash "$hook" post suspend; then exit 1; fi
[[ $(cat "$OMARCHY_BRCMFMAC_SLEEP_STATE") == 0000:ff:00.0 ]]
rm "$OMARCHY_BRCMFMAC_SLEEP_STATE" "$OMARCHY_BRCMFMAC_SLEEP_STATE.lock"
echo 'PASS: installed Broadcom hook preserves pending state across pre and a real failed bind'
