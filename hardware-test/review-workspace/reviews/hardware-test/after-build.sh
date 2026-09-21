#!/bin/bash
# Keep the exact build/validation process running across terminal disconnects.
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
build=$(realpath "${1:?Pass the exact build directory}")
container=${2:?Pass the confirmed Docker container ID}
[[ $container =~ ^[0-9a-f]{64}$ && -d $build/sources/omarchy-iso ]]
while [[ ! -f $build/build.exit ]]; do
  # A file or a timeout alone is not proof that the build is alive. Keep
  # waiting only while Docker confirms this same container is running.
  state=$(sudo /usr/bin/docker inspect --format '{{.State.Status}}' "$container")
  if [[ $state != "running" ]]; then
    sleep 2
    [[ -f $build/build.exit ]] || { echo "Container is $state without a build receipt; inspect before resuming." >&2; exit 1; }
    break
  fi
  sleep 15
done
[[ $(cat "$build/build.exit") == 0 ]] || { echo 'Build failed; fresh-image tests not started.' >&2; exit 1; }
exec /usr/bin/python "$root/reviews/hardware-test/run-validation.py" "$build"
