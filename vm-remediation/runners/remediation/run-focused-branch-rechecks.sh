#!/bin/bash
set -euo pipefail
review_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
wave="$review_root/.state/vm-install/2026-09-20"
iso=$(realpath "${1:?Pass installed base ISO}")
export OMARCHY_INTEGRATION_ISO="$iso" OMARCHY_INTEGRATION_NO_PREVIEW=true OMARCHY_INTEGRATION_MEMORY=4096 OMARCHY_INTEGRATION_SSH_PORT=2522
SCENARIO=preinstalls-assertion-rechecks
source "$(dirname "$iso")/sources/omarchy-iso/test/integration.d/base-test.sh"
base_image_ready
start_vm_from_base
wait_for_ssh "$BOOT_TIMEOUT"
ssh_guest 'test "$(hostname)" = omarchy-test && test "$(systemd-detect-virt)" = kvm && test -b /dev/vda'
status=0
for name in P03 P05 P06 P07 P09 P10 P11 P13 P14; do
 repo="$wave/remediation/branches/$name"
 git -C "$repo" rev-parse HEAD > "$RUN_DIR/$name.commit"
 git -C "$repo" archive HEAD | ssh_guest "mkdir -p /home/omarchy/focused/$name && tar -C /home/omarchy/focused/$name -xf -"
 code=0
 ssh_guest "bash /home/omarchy/focused/$name/test/shell.d/preinstalls-test.sh" > "$RUN_DIR/$name.log" 2>&1 || code=$?
 printf '%s\n' "$code" > "$RUN_DIR/$name.exit"
 printf '%s focused recheck: %s\n' "$name" "$code"
 ((code==0)) || status=1
done
# Recheck only files that actually failed in the preceding complete runs.
# Keep the original aggregate exits; these are separately identified reruns.
stop_vm
full_run="$(dirname "$iso")/sources/omarchy-iso/test-runs/$(basename "$iso" .iso)-integration/runs/20260921-005008-remediation-branch-suites"
python - "$full_run" > "$RUN_DIR/failed-file-rechecks.tsv" <<'PY'
import pathlib,re,sys
p=pathlib.Path(sys.argv[1])
for name in ['integration','P03','P05','P06','P07','P09','P10','P11','P13','P14']:
 for path in re.findall(r'^  (test/shell.d/[a-z0-9-]+-test.sh)$',(p/(name+'.log')).read_text(),re.M):
  if name!='integration' and path.endswith('/preinstalls-test.sh'):continue
  print(name+'\t'+path)
PY
while IFS=$'\t' read -r name test; do
 code=0
 bash "$review_root/reviews/remediation/run-single-source-check.sh" "$iso" "$name" "$test" < /dev/null > "$RUN_DIR/$name-$(basename "$test").log" 2>&1 || code=$?
 printf '%s\n' "$code" > "$RUN_DIR/$name-$(basename "$test").exit"
 printf '%s %s focused recheck: %s\n' "$name" "$test" "$code"
 ((code==0)) || status=1
done < "$RUN_DIR/failed-file-rechecks.tsv"
printf '%s\n' "$status" > "$RUN_DIR/scenario.exit"
printf 'Artifacts: %s\n' "$RUN_DIR"
exit "$status"
