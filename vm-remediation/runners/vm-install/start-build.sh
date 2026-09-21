#!/bin/bash
# Run in the user's remote terminal so the Docker launch has visible sudo auth.
set -euo pipefail
# Git records executable bits, not group/other readability. Use normal source
# permissions so cp -a in the package recipes cannot ship root-only payloads.
umask 022

prepare_only=false
case ${1:-} in
  --prepare-only) prepare_only=true ;;
  "") ;;
  *) echo "Usage: $0 [--prepare-only]" >&2; exit 1 ;;
esac

review_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
wave="$review_root/.state/vm-install/2026-09-20"
iso_root="$wave/repos/omarchy-iso"
mkdir -p "$wave/builds" "$wave/cache/pacman" "$wave/cache/companions"
exec 9>"$wave/build-launch.lock"
flock -n 9 || { echo "A build launch is already in progress." >&2; exit 1; }

if [[ -L $wave/latest-build && ! -f $wave/latest-build/build.exit ]]; then
  echo "The previous build has not finished. Log: $wave/latest-build/build.log" >&2
  exit 1
fi

build_dir=$(mktemp -d "$wave/builds/build-$(date -u +%Y%m%dT%H%M%SZ)-XXXXXX")
mkdir -p "$build_dir/sources"
for repo in omarchy omarchy-pkgs omarchy-iso; do
  git -C "$wave/repos/$repo" rev-parse HEAD > "$build_dir/$repo.commit"
  if [[ -n $(git -C "$wave/repos/$repo" status --porcelain) ]]; then
    echo "Uncommitted source in $repo; checkpoint it before building." >&2
    exit 1
  fi
  # Snapshot tracked content so ignored test caches are excluded, permissions
  # are reproducible, and subsequent agent edits cannot alter a running build.
  git clone --quiet --no-hardlinks --no-checkout "$wave/repos/$repo" "$build_dir/sources/$repo"
  git -C "$build_dir/sources/$repo" checkout --quiet --detach "$(cat "$build_dir/$repo.commit")"
  git -C "$build_dir/sources/$repo" remote remove origin
done
git -C "$build_dir/sources/omarchy-iso" \
  -c protocol.file.allow=always -c "submodule.archiso.url=$iso_root/archiso" \
  submodule update --init --recursive

if $prepare_only; then
  echo "Prepared immutable build sources: $build_dir"
  exit 0
fi

export OMARCHY_BUILD_RELEASE_PATH="$build_dir"
export OMARCHY_ISO_CACHE_ROOT="$wave/cache/iso"
export OMARCHY_PACMAN_CACHE_DIR="$wave/cache/pacman"
export OMARCHY_COMPANION_BUILD_DIR="$wave/cache/companions"

cd "$build_dir/sources/omarchy-iso"
./bin/omarchy-iso-make --detach --keep-pkg-cache --no-boot-offer --debug \
  --local-source "$build_dir/sources/omarchy" "$build_dir/sources/omarchy-pkgs" \
  | tee "$build_dir/launch.log"
ln -sfn "$build_dir" "$wave/latest-build"
echo "The build continues independently of this terminal. I can follow its log locally."
