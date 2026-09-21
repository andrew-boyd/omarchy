#!/bin/bash
set -euo pipefail
[[ $(hostname) == omarchy-test && $(systemd-detect-virt) == kvm && -b /dev/vda && $EUID != 0 ]]
cd /home/omarchy/package-source
commands=(
 'node --test tests/pr-workflow-approval.cjs'
 'node --test tests/builder-image.cjs'
 'python tests/oma-service-removal.py'
 'python tests/upstream-watch.py'
 './bin/sync-upstream self-test'
 './bin/sync-rebuilds --self-test'
 './bin/omarchy-pkgs self-test'
 './bin/omarchy-release self-test'
 './tests/partial-release.sh'
 './tests/published-build-plan.sh'
 './tests/controller.sh'
 './tests/artifact-helpers.sh'
)
failed=0
for command in "${commands[@]}"; do
 printf '==> %s\n' "$command"
 bash -c "$command" || failed=1
done
bash -n pkgbuilds/t1bridge-omarchy/PKGBUILD
printf 'Self-test aggregate exit: %s\n' "$failed"
exit "$failed"
