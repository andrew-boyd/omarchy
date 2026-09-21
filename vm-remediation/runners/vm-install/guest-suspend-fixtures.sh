#!/bin/bash
# Counterexamples for documented P14 limitations. No real suspend or sysfs writes.
set -euo pipefail
[[ $(hostname) == omarchy-test && $(systemd-detect-virt) == kvm && -b /dev/vda ]]
work=${1:?Pass a guest artifact directory}
mkdir -p "$work"
work=$(realpath "$work")
sed '/^# --- entry point/,$d' /usr/share/omarchy/bin/omarchy-diagnose-suspend-wake > "$work/functions.sh"
mkdir -p "$work/device/power" "$work/unrelated/power"
printf '106b\n' > "$work/device/idVendor"
printf 'fixture\n' > "$work/device/idProduct"
printf 'Fixture\n' > "$work/device/manufacturer"
printf 'Disposable USB fixture\n' > "$work/device/product"
printf 'disabled\n' > "$work/device/power/wakeup"
printf 'disabled\n' > "$work/unrelated/power/wakeup"

(
  source "$work/functions.sh"
  STATE_FILE="$work/restore.state"
  save_state "$(printf 'fixture\tusb\t%s/' "$work/device")"
  cmd_restore
  [[ $(cat "$work/device/power/wakeup") == enabled ]]
  [[ $(cat "$work/unrelated/power/wakeup") == disabled ]]
  [[ ! -e $STATE_FILE ]]
  cmd_restore
) > "$work/restore-success.log" 2>&1
echo 'PASS: restore re-enables its recorded USB fixture, preserves unrelated disabled state, and repeats as a no-op.'

(
  source "$work/functions.sh"
  set +e # Preserve the command's original non-errexit behavior.
  STATE_FILE="$work/missing-device.state"
  save_state "$(printf 'missing\tusb\t%s/' "$work/device-removed")"
  cmd_restore
  [[ ! -e $STATE_FILE ]] || exit 1
) > "$work/restore-missing-device.log" 2>&1
echo 'KNOWN LIMIT REPRODUCED: a failed restore write still clears the recorded state.'

(
  source "$work/functions.sh"
  set +e # A failed run_test assignment must follow the actual command path.
  rtcwake() { return 1; }
  cmd_test 10
  printf 'cmd_test exit: %s\n' "$?"
) > "$work/inconclusive-exit.log" 2>&1
grep -Fq 'Could not complete the test.' "$work/inconclusive-exit.log"
grep -Fq 'cmd_test exit: 0' "$work/inconclusive-exit.log"
echo 'KNOWN LIMIT REPRODUCED: rtcwake failure is reported as inconclusive but cmd_test exits zero.'

# A child uses the unchanged command loop and signal trap with fake wake I/O.
# Interrupt during the control result; verify whether any candidate test follows.
cat > "$work/interrupt.sh" <<'SCRIPT'
#!/bin/bash
set -uo pipefail
work=$1
source "$work/functions.sh"
STATE_FILE="$work/interrupt.state"
RULE_FILE="$work/fixture.rules"
all_candidates() { printf 'fixture\tusb\t%s/\n' "$work/device"; }
settle() { :; }
run_test() {
  local count
  count=$(cat "$work/test-count")
  count=$((count + 1))
  printf '%s\n' "$count" > "$work/test-count"
  printf 'test call %s\n' "$count" >&2
  if ((count == 2)); then
    kill -TERM "$$"
    echo held
  else
    echo woke-early
  fi
}
cmd_diagnose 10
SCRIPT
printf '0\n' > "$work/test-count"
printf 'enabled\n' > "$work/device/power/wakeup"
printf 'y\nn\n' | bash "$work/interrupt.sh" "$work" > "$work/interrupt.log" 2>&1
grep -Fq 'Interrupted - restoring wake sources before exiting.' "$work/interrupt.log"
[[ $(cat "$work/test-count") == 3 ]]
[[ $(cat "$work/device/power/wakeup") == disabled ]]
[[ -s $work/interrupt.state ]]
echo 'KNOWN LIMIT REPRODUCED: TERM restores, then diagnosis continues and disables the fixture again.'
