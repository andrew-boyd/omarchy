# T1Bridge for Omarchy

Optional desktop integration for [T1Bridge](https://github.com/standardagents/t1bridge): volume, mute, media controls, brightness HUDs and renderer-fallback notifications. Arch/Omarchy only; T1Bridge itself remains distro-neutral.

**Official signed package:** `t1bridge-omarchy 0.2.1-1`. Available from the [Standard Agents repository](https://linux.standardagents.ai/arch/standardagents/x86_64/PRERELEASE.md), with corresponding source and recipe. See [acceptance evidence](docs/integration.md#acceptance-evidence) for the tested scope.

## Install and enable

First install and configure the official T1Bridge packages using their manual setup instructions, including machine-data import and any scoped xART firewall rule. This package does neither. It requires Omarchy's `omarchy-osd`, audio, brightness, notification and shell media commands.

With the Standard Agents repository configured, install with `sudo pacman -Syu t1bridge-omarchy`. The package configures the provider through its own user-service drop-in. It does not replace the renderer.

Enable session startup as your normal desktop user:

```bash
mkdir -p "$HOME/.config/omarchy/hooks/post-boot.d"
ln -s /usr/lib/t1bridge-omarchy/session-start "$HOME/.config/omarchy/hooks/post-boot.d/40-t1bridge-omarchy"
/usr/lib/t1bridge-omarchy/session-start
```

`ln` deliberately refuses to replace an existing file. On repeat setup, keep an existing symlink only if it already points to this package. Omarchy's existing `post-boot` hook imports the current graphical-session environment before restarting an already-active Touch Bar service. No Hyprland configuration is patched.

Check the provider without sending an action:

```bash
/usr/lib/t1bridge-omarchy/desktop-provider v1 status
systemctl --user show t1-touchbar.service -p Environment
```

An existing user drop-in may override `T1BRIDGE_DESKTOP_PROVIDER`; inspect it before removing anything. Audio/media capabilities disappear when their desktop service or player is unavailable. Hardware brightness, Fn and Touch ID remain T1Bridge's responsibility.

## Upgrade or remove

Package upgrades replace only package-owned files. The session symlink follows the updated helper. Run the helper again after an upgrade, or log out and back in. Existing custom renderer selection and fingerprint data are untouched.

Before removal, verify the hook with `readlink "$HOME/.config/omarchy/hooks/post-boot.d/40-t1bridge-omarchy"`. If it points to `/usr/lib/t1bridge-omarchy/session-start`, remove that symlink with `unlink`. Keep any unrelated file.

Then remove only `t1bridge-omarchy` with `sudo pacman -R t1bridge-omarchy`, run `systemctl --user daemon-reload`, and `systemctl --user try-restart t1-touchbar.service`. Do not remove T1Bridge or fingerprint packages just to remove desktop integration. Other provider overrides, if present, still apply.

## Fingerprints

Fingerprint menu integration belongs to the separate manager and upstream Omarchy hooks, not this package. It never edits PAM or stores fingerprints. Existing fprintd/PAM setup continues working independently, including password fallback. The reusable fingerprint-management TUI belongs in a separate package; Omarchy menu wiring and T1 lock-screen blank/wake behavior need the upstream hooks listed in [integration ownership](docs/integration.md).

## Development

`make check` runs synthetic command and staged install tests without calling live desktop services. `make install DESTDIR=<staging-directory>` stages the payload. The provider was extracted from Omarchy's `t1bridge-desktop-provider` branch at `f7280948`; its original MIT notice is retained.

The candidate recipe uses a local source archive until this repository has a reviewed public release. From a clean committed checkout, create the archive and compare its SHA-256 with the recipe before building:

```bash
git archive --format=tar --mtime=1970-01-01T00:00:00Z --prefix=t1bridge-omarchy-0.1.0/ 'HEAD^{tree}' | gzip -n > packaging/arch/t1bridge-omarchy-0.1.0.tar.gz
sha256sum packaging/arch/t1bridge-omarchy-0.1.0.tar.gz
(cd packaging/arch && makepkg --cleanbuild)
bash tests/package.sh packaging/arch/t1bridge-omarchy-0.1.0-2-any.pkg.tar.zst
```

The last command uses fakeroot and a temporary pacman root, skips dependency installation and scriptlets, and never calls the host package manager as root. It proves package file ownership and install/reinstall/removal, not live desktop behavior or password authentication. The recipe deliberately contains no install scriptlets and does not restart services.

## Automatic brightness

The package includes an optional light-only panel brightness service using the
T1 sensor through `iio-sensor-proxy`. Enable it in your graphical session:

```sh
systemctl --user enable --now t1bridge-auto-brightness.service
```

Stop automatic adjustment and keep your current brightness:

```sh
systemctl --user disable --now t1bridge-auto-brightness.service
```

The service starts at your current brightness. Manual brightness changes become
its new reference and pause automatic adjustment for 30 seconds. Each doubling
of light adds approximately ten percentage points relative to that reference;
changes are limited to two percentage points per second with a one-point
hysteresis. It normally keeps at least ten percent brightness, but respects a
lower manually selected reference. Locked and inactive sessions pause adjustment.
On unlock it adopts the current brightness again. Sensor loss leaves brightness
unchanged; the service retries after 30 seconds if the monitor exits.

This controls one unambiguous panel backlight only. It requires one light sensor
with a T1 USB ancestor and refuses additional IIO, hwmon/platform light sensors
or FastRPC sensor sources. Sensor replacement, ambiguity, proxy restart, and
non-lux readings stop adjustment and trigger fresh discovery after 30 seconds;
readings from the previous monitor are discarded. It does not adjust
keyboard lighting, capture screen contents, or replace desktop idle behavior.
Do not run it alongside another automatic-brightness controller.

For a read-only preview, stop the service and run
`/usr/lib/t1bridge-omarchy/auto-brightness --dry-run`; after the initial 30-second
hold, changing the light prints proposed values without changing brightness.
The package installs its own files; enabling this preference remains a user
choice. Local cover/uncover, manual-reference, post-unlock and reboot-startup checks passed on MacBookPro13,3. Broader model coverage and observation during the locked interval remain open.
