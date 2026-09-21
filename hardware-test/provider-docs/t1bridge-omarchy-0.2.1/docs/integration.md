# Integration ownership and acceptance

| Existing work | Owner / extraction |
| --- | --- |
| `bin/omarchy-t1bridge-desktop-provider` | This package: `/usr/lib/t1bridge-omarchy/desktop-provider`; v1 contract, no new daemon. |
| Provider environment drop-in | This package: uniquely named `40-t1bridge-omarchy.conf`; no overwrite of Omarchy's `20-omarchy-desktop-provider.conf`. |
| Session environment import / renderer restart | This package helper invoked by the existing user `post-boot.d` hook. No replacement of `default/hypr/autostart.lua`; no whole-environment import. |
| Audio sink routing, brightness queries, OSD, shell media IPC | Omarchy-owned commands; reused, never vendored or replaced. |
| Enrollment/removal TUI, hand/finger selection, themed progress | Separate generic fingerprint-management package, usable with other readers/desktops. Do not copy the large root-wrapped Omarchy implementation into this package. |
| Setup/Security menu entries | Minimal upstream integration needed: command-presence-gated launch of the separate manager. The current menu loads one default plus one user extension, not package fragments. Do not overwrite either. |
| Fingerprint setup / PAM | Distribution policy, explicitly configured. This package must not silently replace sudo, Polkit or lock PAM stacks. |
| Per-attempt PAM context and stale callback handling | Generic Omarchy lock-screen correction; upstream PR, not package-owned QML. |
| T1 blank/wake prompt lifecycle | Omarchy lock hook needed: release T1 authentication when blanked, rearm on wake; leave other readers armed. Existing branch has this in `Service.qml`; cannot be shipped by replacing that file. |
| EFI preservation, T1 detection, install, import notification/retry, firewall provisioning | Installer/post-install PR work, outside this runtime package. |

## Remaining hooks

The current Omarchy branch's hard-coded T1 package test in the lock screen should become a small capability/configuration seam owned by Omarchy. The optional package can then supply its T1 behavior without forking the lock screen. Preserve the already-tested generic-reader retry behavior. Decide the exact hook with the upstream PR, not by injecting QML at installation time.

Menu entries must launch the generic fingerprint manager only when installed. Initial setup, add, remove and disable-authentication are distinct operations; removing this integration must not delete enrolled fingers or disable password authentication.

## Acceptance evidence

- [x] Provider contract, unavailable capabilities, argument validation, failed action/HUD handling: `tests/provider.sh` with stub desktop commands.
- [x] Staged install/reinstall owns exactly eight files and preserves synthetic PAM, machine-data, renderer and Omarchy files: `tests/install.sh`. Actual package removal is a separate check below.
- [x] Session helper imports only the allowlisted environment, no-op outside Omarchy, and uses `try-restart` without touching renderer selection: `tests/session.sh` with a stub systemctl, not a live service test.
- [x] Built candidate install/reinstall/removal and versioned upgrade passed in isolated pacman roots (`tests/package.sh`, `packaging/arch/test-upgrade.sh`). These skip dependency installation and scriptlets; the package has no scriptlets.
- [x] Installed extracted package: volume, display and keyboard controls, HUDs and hold-repeat accepted locally; HUDs remain available after reboot (September 7).
- [x] Media controls: owner confirmed Touch Bar media buttons work with a music app (September 9). Installed provider and session helper are byte-identical to this source. This is a live user report, separate from synthetic dispatch tests.
- [x] Fresh sudo fingerprint and password fallback passed after extracted-package installation (September 7). PAM files were unchanged. This does not claim a new broker-down test or fresh live install/remove cycle.

The September 9 candidate changes documentation and package revision only;
provider, session helper and service drop-in are unchanged from the installed
0.1.0-1 candidate. Synthetic checks cover mute dispatch and unavailable services;
no separate live mute result is recorded.

## Outside this package

Generic fingerprint-manager menu integration and T1 lock blank/wake behavior
are tracked separately in Omarchy and the manager project; they are not
bundled into this provider package. Existing password policy and renderer selection stay owned
by their current components. No new live authentication test or hardware
recovery is claimed by this acceptance record.

Version 0.2.0-2 is distributed through the official signed repository with corresponding source and recipe.

## Automatic brightness

Version 0.2.0 adds the standard `iio-sensor-proxy`, `brightnessctl` and
`coreutils` dependencies and a separately enabled user service. Installation
now owns eight files. The service consumes standard light reports and controls
only a single discovered panel backlight; it never changes PAM, the T1 USB
configuration or renderer selection. See the README for policy and controls.
Synthetic tests cover policy bounds, manual references, T1 ancestry, ambiguous
sensor rejection and locked/inactive sessions. On September 11, attended tests
on MacBookPro13,3 confirmed 25–26 lux and 58–59% brightness covered, then
75–78 lux and 73–74% uncovered. Manual 100% held beyond the 30-second pause.
Brightness and sensor reports remained healthy after a reported lock/unlock;
the locked interval itself was not observed. After reboot the enabled user
service started automatically at graphical login with zero restarts. It adopts
the current startup brightness instead of persisting the previous boot's
reference. The release also rejects alternate IIO light-sensor attribute forms
when checking for ambiguous devices; synthetic rejection tests cover them.
Other-model and concurrent camera/authentication acceptance remain open. Parent work is
[core #17](https://github.com/standardagents/t1bridge/issues/17).
