# Reproduce the Intel Mac VM validation

The public `vm-validation/integration/sources.json` lists the exact upstream bases, integration commits, tree hashes, bundles and aggregate patches. The bundles preserve the merged contribution commits and authors. Each bundle was verified by fetching its pinned base into an otherwise empty repository, fetching the bundle and checking out the exact tested tree. Each aggregate patch was independently applied to its base index and produced the same tree hash.

## Restore sources

Clone the `intel-mac/review-index` branch of `andrew-boyd/omarchy` as a separate evidence checkout. For each repository in `sources.json`, make a normal full clone of its listed upstream repository, fetch its bundle and check out the tested commit:

```bash
git clone https://github.com/omacom/omarchy.git omarchy
git -C omarchy fetch /absolute/path/to/evidence/vm-validation/integration/omarchy.bundle vm/intel-mac-integration
git -C omarchy checkout --detach 8ffe7ac51a35d8bce32e3e272b3a5ce0704c92c9
```

Repeat for `omarchy-pkgs` and `omarchy-iso` using their recorded commits. In the ISO checkout, run `git submodule update --init --recursive`; the archiso commit is `424e78130db2af6c1ceb55b442d7914b1109ff2b`. Verify `git rev-parse HEAD^{tree}` against `sources.json`. Full upstream history is recommended because package version generation uses Git history; a shallow reconstruction proves tree identity but may produce a different package revision count.

The `.patch` files are a fallback for tree reconstruction (`git apply --index` at the pinned base); they do not preserve commit authorship by themselves. Do not replace the feature branches' author commits with an anonymous aggregate commit.

## Build and install

Use the checked-out ISO repository's documented QEMU/KVM, Docker and archiso dependencies. Work in a disposable build directory with enough storage. Normal interactive sudo for Docker is sufficient; the original machine's temporary Docker-only grant is not a prerequisite or a file to copy.

```bash
cd omarchy-iso
umask 022
./bin/omarchy-iso-make --no-boot-offer --local-source ../omarchy ../omarchy-pkgs
```

Retain the output ISO, `build.log`, `build.exit`, source commits, local package list and package SHA256 receipt. The local builder produces the three runtime and ten Mac companion archives and verifies pinned source hashes. It builds the optional T1 desktop adapter against the exact local dev-runtime version. It does not automatically provision T1 hardware.

No reuse receipt is required: a fresh build rebuilds all packages. If reusing tested archives, the helper requires the explicit verified-source/hash receipt; do not relabel old artifacts as newly built. The original build's package mirrors and moving upstream dependencies can change. Exact source reconstruction does not promise a byte-for-byte identical future ISO.

Before acceptance, copy only the source `test/` directory into a separate test-sync directory and apply `runners/acceptance-ocr-whitespace.patch` there. This preserves the product tree while retaining the observed OCR correction. Then run the real installer and acceptance suite:

```bash
./bin/omarchy-iso-test /absolute/path/to/generated.iso --sync-omarchy /absolute/path/to/test-sync --no-preview
```

Use `--encrypt` for the encrypted path. Do not use `--reuse-base` for the first run of a newly built artifact. All eight acceptance files must finish; preserve failures as well as reruns. The product under test must remain `/usr/share/omarchy` inside the VM.

The original integration harness chooses stable/dev packages partly from the ISO filename. Its local-source input must contain `local` in the name. Use a hardlink with `local` in its name; a symlink is resolved by the scenario scripts and loses that distinction. Verify both paths have identical bytes.

```bash
./test/integration /absolute/path/to/intel-mac-local.iso --no-preview
```

Consult that runner's help if options change. Its shared-ESP factory-reset scenario failed on the pinned baseline; that failure is part of this report. Do not erase foreign data in a real installation to reproduce it.

## Focused guest scenarios

The supplied `runners/` scripts record the actual tests used. Their original layout expects a review root with `reviews/vm-install/` and `.state/vm-install/2026-09-20/builds/<build>/sources/{omarchy,omarchy-pkgs,omarchy-iso}`. `start-build.sh` creates immutable build snapshots from `.state/vm-install/2026-09-20/repos/`. Adapt paths deliberately if using another layout; never point guest operations at the host.

`run-package-scenario.sh` installs camera, either audio stack or T1 packages in separate overlays, verifies package hashes/versions and target headers, compiles DKMS and reboots. The audio12 regression additionally requires `0.1-2`, verifies that stock kernel/headers were not pulled into an Omarchy-only system, and rejects the previously hidden DKMS hook errors. `run-migration-scenario.sh` exercises PIO and kernel/header upgrade paths. `run-nvme-scenario.sh` adds an actual virtual non-Apple NVMe controller. The full source suite and desktop/lock checks use the remaining guest helpers.

Each helper guards the test destination (`omarchy-test`, KVM, `/dev/vda`). DMI/vendor overrides are explicitly fixture inputs, never claims that QEMU emulates Apple hardware. The test username/password are disposable synthetic guest credentials; do not use a real account password. Do not publish guest SSH private keys, VM disks or host credentials with results.

After completion, shut down guests and stop their background workers. Record exact artifact/source hashes, return codes, log hashes, screenshots and physical limitations in the relevant draft PR. Retain original failures and clarify when an assertion or harness was corrected.
