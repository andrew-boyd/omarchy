# Full Intel Mac inventory

All 64-bit Intel Macs; pre-T1, T1 and T2. MacBookPro13,3 is only the first physical test target.

Inventory/disposition coverage is not implementation completion. Separate work tracks remain unimplemented by P01–P14; alternative/deferred/context rows are not ISO content.

This is the current audited inventory. The dated test report and publication receipts identify the tested ISO and the state of the 17 existing draft updates.

| Source | Current state | Roll-up disposition | Separate work track |
| --- | --- | --- | --- |
| [leifliddy/macbook12-audio-driver#60](https://github.com/leifliddy/macbook12-audio-driver/pull/60) — Fix DKMS install and removal lifecycle | merged | P11: context | None |
| [omacom/omarchy-iso#174](https://github.com/omacom/omarchy-iso/pull/174) — Preserve Apple EFI firmware folder across the install | open | P12: partial | efi-preservation |
| [omacom/omarchy-iso#182](https://github.com/omacom/omarchy-iso/pull/182) — Install linux-omarchy by default except on T2 Macs | merged | P13: context | None |
| [omacom/omarchy-iso#183](https://github.com/omacom/omarchy-iso/pull/183) — Install matching kernel headers before hardware setup | open | P02: superseded | None |
| [omacom/omarchy-iso#184](https://github.com/omacom/omarchy-iso/pull/184) — Install and validate matching kernel headers in the ISO | merged | P02: context | None |
| [omacom/omarchy-pkgs#152](https://github.com/omacom/omarchy-pkgs/pull/152) — Build apple-ib-tb on kernel 6.12+ from Heratiki's fork | open | P12: alternative | None |
| [omacom/omarchy-pkgs#153](https://github.com/omacom/omarchy-pkgs/pull/153) — Add MacBook12 CS4208 DKMS package | open | P11: included | None |
| [omacom/omarchy-pkgs#155](https://github.com/omacom/omarchy-pkgs/pull/155) — Add snd-hda-macbookpro-dkms for 2016-2017 MacBook speakers | open | P11: superseded | None |
| [omacom/omarchy-pkgs#182](https://github.com/omacom/omarchy-pkgs/pull/182) — Add MacBookPro13,1 camera and audio packages | open | P08: alternative; P11: alternative | mbp131-bundle |
| [omacom/omarchy-pkgs#249](https://github.com/omacom/omarchy-pkgs/pull/249) — Add snd-hda-macbookpro-dkms for pre-T2 MacBook and iMac speakers | open | P11: included | None |
| [omacom/omarchy-pkgs#298](https://github.com/omacom/omarchy-pkgs/pull/298) — Package freeze-safe Apple T1 Touch Bar driver | open | P12: alternative | None |
| [omacom/omarchy-pkgs#315](https://github.com/omacom/omarchy-pkgs/pull/315) — Install the T1 ALS auto-brightness user unit | open | P12: alternative | None |
| [omacom/omarchy-pkgs#349](https://github.com/omacom/omarchy-pkgs/pull/349) — Add tb-ar-shim-dkms: Alpine Ridge suspend fix for the MacBookPro14,1 | open | None | alpine-ridge |
| [omacom/omarchy-pkgs#422](https://github.com/omacom/omarchy-pkgs/pull/422) — fix: add Apple BCM43602 resume kernel | open | P10: alternative; P13: alternative | None |
| [omacom/omarchy-pkgs#445](https://github.com/omacom/omarchy-pkgs/pull/445) — Replace AUR sync with direct upstream release watches | merged | P06: context | None |
| [omacom/omarchy-pkgs#454](https://github.com/omacom/omarchy-pkgs/pull/454) — Remove kernel header dependencies from DKMS packages | merged | P02: context | None |
| [omacom/omarchy-pkgs#476](https://github.com/omacom/omarchy-pkgs/pull/476) — Add afanctl: applesmc fan supervisor for pre-T2 Intel Macs (A1708) | open | None | applesmc-fans |
| [omacom/omarchy-pkgs#509](https://github.com/omacom/omarchy-pkgs/pull/509) — linux-omarchy: fix poweroff/reboot hang with Thunderbolt/USB4 displays on 7.2 | open | None | thunderbolt-kernel |
| [omacom/omarchy-pkgs#516](https://github.com/omacom/omarchy-pkgs/pull/516) — linux-omarchy: carry Apple SMC charge-threshold patches | open | None | battery-limits |
| [omacom/omarchy-pkgs#544](https://github.com/omacom/omarchy-pkgs/pull/544) — linux-omarchy: carry ACPICA PCI bus fix for resume delays | open | P13: alternative | alpine-ridge |
| [omacom/omarchy#10065](https://github.com/omacom/omarchy/pull/10065) — Hibernation: keep native GPU drivers out of the initramfs so resume runs before any GPU driver touches the hardware | open | None | pre-t2-hibernation |
| [omacom/omarchy#10111](https://github.com/omacom/omarchy/pull/10111) — bluetooth: register pairing agent and discover before pair/connect; fix usbcore autosuspend cmdline | open | None | bluetooth-discovery |
| [omacom/omarchy#10125](https://github.com/omacom/omarchy/pull/10125) — Avoid Baffin GPU hangs during screen recording | open | None | baffin-capture |
| [omacom/omarchy#10139](https://github.com/omacom/omarchy/pull/10139) — Keep the Apple USB SD card reader alive after suspend | open | None | sd-reader |
| [omacom/omarchy#10140](https://github.com/omacom/omarchy/pull/10140) — Apply USB autosuspend policy through the kernel command line | open | None | alpine-ridge |
| [omacom/omarchy#10141](https://github.com/omacom/omarchy/pull/10141) — Stabilize MacBookPro13,3 hardware support | open | P06: context; P07: context; P09: context; P10: context; P12: context | mbp133-bundle |
| [omacom/omarchy#10169](https://github.com/omacom/omarchy/pull/10169) — Fix iMac20,2 AMDGPU startup race | open | None | imac-gpu-boot |
| [omacom/omarchy#10196](https://github.com/omacom/omarchy/pull/10196) — Require a real charge threshold before reporting a held charge | open | None | battery-limits |
| [omacom/omarchy#10198](https://github.com/omacom/omarchy/pull/10198) — Disable ghost internal display connectors | open | P05: included | None |
| [omacom/omarchy#10224](https://github.com/omacom/omarchy/pull/10224) — Exclude the internal Apple T2 Ethernet link from automatic wired profiles | closed | None | t2-ethernet |
| [omacom/omarchy#10234](https://github.com/omacom/omarchy/pull/10234) — fix(brightness): fall back to ACPI when DDC fails | closed | None | brightness-routing |
| [omacom/omarchy#10306](https://github.com/omacom/omarchy/pull/10306) — Install Apple Broadcom Wi-Fi firmware on every Mac brcmfmac drives, not just T2 | open | P10: deferred | wifi-firmware |
| [omacom/omarchy#10313](https://github.com/omacom/omarchy/pull/10313) — Cap MacBook10,1 RAPL at 4.5W/7W and CPU turbo at 3GHz | open | None | cpu-power |
| [omacom/omarchy#10314](https://github.com/omacom/omarchy/pull/10314) — Disable MacBook10,1 BCM4350 wakeup through S3 | open | P10: deferred | None |
| [omacom/omarchy#10331](https://github.com/omacom/omarchy/pull/10331) — Follow the T1 ambient light sensor for panel and keyboard backlight | open | P12: context | None |
| [omacom/omarchy#10332](https://github.com/omacom/omarchy/pull/10332) — Fix Wi-Fi dying after suspend on BCM43602 MacBooks | open | P10: alternative | None |
| [omacom/omarchy#10366](https://github.com/omacom/omarchy/pull/10366) — Fix keyboard backlight restore after screensaver dismiss | open | None | keyboard-backlight-state |
| [omacom/omarchy#10458](https://github.com/omacom/omarchy/pull/10458) — Enable speakers on Late 2015 21.5-inch iMacs | open | P11: included | None |
| [omacom/omarchy#10462](https://github.com/omacom/omarchy/pull/10462) — Wake the panel when a laptop-only lid opens | closed | P04: alternative | None |
| [omacom/omarchy#10468](https://github.com/omacom/omarchy/pull/10468) — Name keycode bindings after the layout the keyboard is using | open | P01: context | None |
| [omacom/omarchy#10485](https://github.com/omacom/omarchy/pull/10485) — Send Broadcom's ACL-priority command to fix Bluetooth A2DP stutter on T2 Macs | open | None | bluetooth-audio |
| [omacom/omarchy#10502](https://github.com/omacom/omarchy/pull/10502) — Decide the charge limit from the threshold, not the charge level | closed | None | battery-limits |
| [omacom/omarchy#10582](https://github.com/omacom/omarchy/pull/10582) — Enable first-run user units one at a time | open | P12: context | None |
| [omacom/omarchy#10713](https://github.com/omacom/omarchy/pull/10713) — Use active external displays for the lid-close lock decision | open | P04: included | None |
| [omacom/omarchy#10758](https://github.com/omacom/omarchy/pull/10758) — Fix Thunderbolt suspend on the MacBookPro14,1 | open | None | alpine-ridge |
| [omacom/omarchy#10783](https://github.com/omacom/omarchy/pull/10783) — docs: add 2020 iMac models to the T2 Mac list | open | None | model-docs |
| [omacom/omarchy#10797](https://github.com/omacom/omarchy/pull/10797) — Install DKMS headers for the kernel that actually boots | closed | P02: superseded | None |
| [omacom/omarchy#10807](https://github.com/omacom/omarchy/pull/10807) — Pick Vulkan ICDs from sysfs instead of three lspci greps | closed | P03: context | None |
| [omacom/omarchy#10808](https://github.com/omacom/omarchy/pull/10808) — Share one sysfs T2 helper for packages and arch-mact2 | closed | P03: context | None |
| [omacom/omarchy#10810](https://github.com/omacom/omarchy/pull/10810) — Detect BCM4360/BCM4331 from sysfs instead of lspci | closed | P03: context | None |
| [omacom/omarchy#10877](https://github.com/omacom/omarchy/pull/10877) — Target the actual NVMe controller in Apple suspend fix | open | P09: alternative | None |
| [omacom/omarchy#10886](https://github.com/omacom/omarchy/pull/10886) — Repair T1 Mac PCIe hotplug defaults | open | None | t1-pcie |
| [omacom/omarchy#10890](https://github.com/omacom/omarchy/pull/10890) — Classify T2 built-in trackpads as internal | closed | None | t2-trackpad |
| [omacom/omarchy#10910](https://github.com/omacom/omarchy/pull/10910) — fix(bcm43xx): add BCM43224 detection and blacklist conflicting drivers | open | P10: deferred | wifi-legacy |
| [omacom/omarchy#10936](https://github.com/omacom/omarchy/pull/10936) — Support pre-GCN AMD GPUs and BCM4321 wireless | open | None | older-macs |
| [omacom/omarchy#10942](https://github.com/omacom/omarchy/pull/10942) — Document pre-2012 Intel Mac support | open | None | older-macs |
| [omacom/omarchy#11017](https://github.com/omacom/omarchy/pull/11017) — Install missing BCM43602 board NVRAM on MacBookPro13,3 | open | P10: included | None |
| [omacom/omarchy#11064](https://github.com/omacom/omarchy/pull/11064) — Add pre-T2 MacBook Cirrus CS8409 speaker fix | open | P11: alternative | None |
| [omacom/omarchy#11259](https://github.com/omacom/omarchy/pull/11259) — Avoid lspci in favor of sysfs | open | P03: context | None |
| [omacom/omarchy#11273](https://github.com/omacom/omarchy/pull/11273) — Lock screen: keep fingerprint idle while the display is blanked | open | P12: included | None |
| [omacom/omarchy#11296](https://github.com/omacom/omarchy/pull/11296) — Document custom MacBook trackpad gestures | open | None | trackpad-defaults |
| [omacom/omarchy#11311](https://github.com/omacom/omarchy/pull/11311) — Install b43-firmware for BCM4322 Wi-Fi (older MacBooks) | open | P10: deferred | wifi-legacy |
| [omacom/omarchy#11312](https://github.com/omacom/omarchy/pull/11312) — Software brightness fallback when DRM backlight is missing | open | None | brightness-routing |
| [omacom/omarchy#11381](https://github.com/omacom/omarchy/pull/11381) — Install the pre-T2 FaceTime HD camera driver and firmware | open | P08: partial | None |
| [omacom/omarchy#11404](https://github.com/omacom/omarchy/pull/11404) — fix(brightness): guard keyboard backlight state across lock and idle blanking | open | None | keyboard-backlight-state |
| [omacom/omarchy#11432](https://github.com/omacom/omarchy/pull/11432) — Make power profiles change the CPU on Intel machines without HWP | open | None | cpu-power |
| [omacom/omarchy#11434](https://github.com/omacom/omarchy/pull/11434) — apple: reload brcmfmac after resume, some Broadcom Wi-Fi parts don't survive S3 | closed | P10: alternative | None |
| [omacom/omarchy#11464](https://github.com/omacom/omarchy/pull/11464) — Add the 2017 iMac 5K to Mac support | open | None | imac-5k |
| [omacom/omarchy#11481](https://github.com/omacom/omarchy/pull/11481) — Keep Voxtype on CPU for Intel Haswell GPUs | open | None | haswell-voxtype |
| [omacom/omarchy#11514](https://github.com/omacom/omarchy/pull/11514) — Mise: no forced release-age 0; SSE4.2 agent skip; keep OpenClaw CLI | open | None | cpu-instructions |
| [omacom/omarchy#11516](https://github.com/omacom/omarchy/pull/11516) — Ignore USB Touch Bar DRM when detecting external displays | open | P04: alternative | None |
| [omacom/omarchy#11536](https://github.com/omacom/omarchy/pull/11536) — Fix BCM4377 Bluetooth hang and D3 suspend abort on T2 Macs | open | P10: alternative | wifi-t2-combo |
| [omacom/omarchy#11548](https://github.com/omacom/omarchy/pull/11548) — Arbitrate MacBookPro11,5 dGPU to radeon | open | None | legacy-gpu |
| [omacom/omarchy#11570](https://github.com/omacom/omarchy/pull/11570) — Suspend on MacBookPro14,2: keep Wi-Fi and USB-C working across S3 (two systemd-sleep hooks) | open | P10: alternative; P04: alternative | alpine-ridge |
| [omacom/omarchy#11592](https://github.com/omacom/omarchy/pull/11592) — Fix legacy Intel VA-API driver detection | open | None | intel-video |
| [omacom/omarchy#11616](https://github.com/omacom/omarchy/pull/11616) — Fix weak WiFi signal on BCM43602 (MacBook Pro 2015-2017) | open | P10: alternative | None |
| [omacom/omarchy#11623](https://github.com/omacom/omarchy/pull/11623) — Fix MacBook Pro 2015-2017: WiFi signal (-90 dBm) and audio (CS8409) | closed | P10: alternative; P11: alternative | None |
| [omacom/omarchy#11624](https://github.com/omacom/omarchy/pull/11624) — Scope the MacBook NVMe suspend fix to Apple's NVMe controller | open | P09: included | None |
| [omacom/omarchy#11625](https://github.com/omacom/omarchy/pull/11625) — Fix audio on MacBook Pro 2015-2017 (Cirrus Logic CS8409) | closed | P11: alternative | None |
| [omacom/omarchy#11748](https://github.com/omacom/omarchy/pull/11748) — Set the boot Wi-Fi country on BCM4350/BCM43602 Macs | open | P10: deferred | wifi-country |
| [omacom/omarchy#11897](https://github.com/omacom/omarchy/pull/11897) — Use Omarchy kernel headers for hardware DKMS drivers | merged | P02: context | None |
| [omacom/omarchy#11898](https://github.com/omacom/omarchy/pull/11898) — [4.0.4] Use Omarchy kernel headers for hardware DKMS drivers | merged | P02: context | None |
| [omacom/omarchy#11900](https://github.com/omacom/omarchy/pull/11900) — Treat kernel headers as part of the base system | merged | P02: context | None |
| [omacom/omarchy#11901](https://github.com/omacom/omarchy/pull/11901) — Treat kernel headers as part of the 4.0.4 base system | merged | P02: context | None |
| [omacom/omarchy#11904](https://github.com/omacom/omarchy/pull/11904) — Add omarchy-diagnose-suspend-wake | open | P14: included | None |
| [omacom/omarchy#11937](https://github.com/omacom/omarchy/pull/11937) — Restart Bluetooth agent when BlueZ is replaced | open | None | bluetooth-discovery |
| [omacom/omarchy#11952](https://github.com/omacom/omarchy/pull/11952) — Show fingerprint reader status in authentication dialogs | open | P12: included | None |
| [omacom/omarchy#12007](https://github.com/omacom/omarchy/pull/12007) — Drop macbook12-spi-driver-dkms, which no longer builds on 7.x kernels | open | P06: alternative | None |
| [omacom/omarchy#12067](https://github.com/omacom/omarchy/pull/12067) — Install the FaceTime HD camera driver on Intel Macs that have one | open | P08: included | None |
| [omacom/omarchy#12072](https://github.com/omacom/omarchy/pull/12072) — Omit empty duplicate displays from the Display panel | open | P05: partial | None |
| [omacom/omarchy#12074](https://github.com/omacom/omarchy/pull/12074) — Install stock kernel headers for broadcom-wl-dkms on upgraded Macs | open | P02: included | None |
| [omacom/omarchy#12076](https://github.com/omacom/omarchy/pull/12076) — Detect BCM43xx, T2, Vulkan, and NVIDIA via sysfs helpers | open | P03: included | None |
| [omacom/omarchy#12090](https://github.com/omacom/omarchy/pull/12090) — Install matching kernel headers before broadcom-wl-dkms | open | P02: alternative | None |
| [omacom/omarchy#12200](https://github.com/omacom/omarchy/pull/12200) — Document MacBookPro16,1 power tuning and validation | open | None | t2-power-docs |
| [omacom/omarchy#12201](https://github.com/omacom/omarchy/pull/12201) — lock: re-arm fingerprint reader after a missed or errored scan | closed | P12: context | None |
| [omacom/omarchy#12203](https://github.com/omacom/omarchy/pull/12203) — Keep EFI framebuffer on 2020 5K iMacs with Navi 14 | open | None | t2-imac-framebuffer |
| [omacom/omarchy#12210](https://github.com/omacom/omarchy/pull/12210) — Debounce lid-close suspend so a quick reopen does not sleep in the dark | open | P04: alternative | None |
| [omacom/omarchy#12211](https://github.com/omacom/omarchy/pull/12211) — Keep T1 MacBook Pros in S3 instead of an Alpine Ridge wake loop | open | None | alpine-ridge |
| [omacom/omarchy#12249](https://github.com/omacom/omarchy/pull/12249) — Install DKMS headers for the kernel that actually boots | open | P02: alternative | None |
| [omacom/omarchy#12267](https://github.com/omacom/omarchy/pull/12267) — Backlight: AIO kernel route and apple-panel-bl priority | open | None | brightness-routing |
| [omacom/omarchy#12286](https://github.com/omacom/omarchy/pull/12286) — Fix silent speakers on 12-inch MacBook (CS4208) | open | P11: alternative | None |
| [omacom/omarchy#12314](https://github.com/omacom/omarchy/pull/12314) — apple: rebind brcmfmac across suspend | open | P10: included | None |
| [omacom/omarchy#12328](https://github.com/omacom/omarchy/pull/12328) — Keep every Intel Mac on its kernel in the linux-omarchy migration | open | P13: included | None |
| [omacom/omarchy#12337](https://github.com/omacom/omarchy/pull/12337) — Make night light temperatures configurable in shell.json | open | None | outside-scope |
| [omacom/omarchy#12350](https://github.com/omacom/omarchy/pull/12350) — Ignore the Apple SMC power/lid device in the keyboard layout widget | open | P01: included | None |
| [omacom/omarchy#12420](https://github.com/omacom/omarchy/pull/12420) — lock: stop fingerprint scans while the display is blanked | open | P12: alternative | None |
| [omacom/omarchy#12426](https://github.com/omacom/omarchy/pull/12426) — lock: re-arm fingerprint reader with a fresh PAM context per attempt | open | P12: alternative | None |
| [omacom/omarchy#12428](https://github.com/omacom/omarchy/pull/12428) — Install rtkit so PipeWire gets realtime priority | open | None | audio-realtime |
| [omacom/omarchy#12435](https://github.com/omacom/omarchy/pull/12435) — Reclaim lock screen keyboard focus after resume from suspend | open | P04: alternative; P12: alternative | None |
| [omacom/omarchy#12502](https://github.com/omacom/omarchy/pull/12502) — Keep the keyboard backlight level across lock and suspend | open | P04: context; P12: context | None |
| [omacom/omarchy#12517](https://github.com/omacom/omarchy/pull/12517) — Position picture-in-picture from its final size, like webcam overlay | open | None | picture-in-picture |
| [omacom/omarchy#12590](https://github.com/omacom/omarchy/pull/12590) — Restore t2fanrd fan control after suspend/resume on T2 Macs | open | None | t2-fan-resume |
| [omacom/omarchy#12614](https://github.com/omacom/omarchy/pull/12614) — Fix lock password focus after resume | closed | P04: superseded; P12: superseded | None |
| [omacom/omarchy#12616](https://github.com/omacom/omarchy/pull/12616) — Stop counting Hyprland virtual outputs as external monitors | open | P04: alternative | None |
| [omacom/omarchy#12634](https://github.com/omacom/omarchy/pull/12634) — Wake displays before restoring keyboard and clamshell state | open | P04: context | None |
| [omacom/omarchy#12652](https://github.com/omacom/omarchy/pull/12652) — Fix lock password focus after resume | closed | P04: alternative; P12: alternative | None |
| [omacom/omarchy#12667](https://github.com/omacom/omarchy/pull/12667) — Accept keypad digits on the lock screen while NumLock is desynced | open | P12: context | None |
| [omacom/omarchy#2331](https://github.com/omacom/omarchy/pull/2331) — Keyboard brightness multimedia keys support | closed | None | keyboard-backlight-steps |
| [omacom/omarchy#5136](https://github.com/omacom/omarchy/pull/5136) — Add auto power profile switching for T2 MacBooks | open | None | cpu-power |
| [omacom/omarchy#5140](https://github.com/omacom/omarchy/pull/5140) — Add WiFi resume hook for T2 MacBooks | open | P10: alternative | wifi-t2-combo |
| [omacom/omarchy#5424](https://github.com/omacom/omarchy/pull/5424) — Set keyboard brightness to fixed values of 0, 1, 25 and 100. | open | None | keyboard-backlight-steps |
| [omacom/omarchy#5970](https://github.com/omacom/omarchy/pull/5970) — Fix suspend/resume on MacBookPro14,1 | open | None | alpine-ridge |
| [omacom/omarchy#6149](https://github.com/omacom/omarchy/pull/6149) — Fix intermittent suspend hang on T2 MacBooks (force synchronous device suspend) | open | None | t2-suspend |
| [omacom/omarchy#6533](https://github.com/omacom/omarchy/pull/6533) — Make keyboard backlight steps consistent in both directions | open | None | keyboard-backlight-steps |
| [omacom/omarchy#6834](https://github.com/omacom/omarchy/pull/6834) — Ignore T2 headset remotes when switching layouts | open | P01: included | None |
| [omacom/omarchy#6921](https://github.com/omacom/omarchy/pull/6921) — Install the CS4208 speaker driver on 12-inch MacBooks | open | P11: included | None |
| [omacom/omarchy#6928](https://github.com/omacom/omarchy/pull/6928) — Enable palm rejection on T2 MacBooks | open | None | t2-trackpad |
| [omacom/omarchy#6929](https://github.com/omacom/omarchy/pull/6929) — Add low-power Intel rendering mode for hybrid T2 MacBooks | open | None | t2-gmux |
| [omacom/omarchy#7044](https://github.com/omacom/omarchy/pull/7044) — Keep Thunderbolt USB-C xHCI awake on Intel MacBooks | open | None | alpine-ridge |
| [omacom/omarchy#7064](https://github.com/omacom/omarchy/pull/7064) — Add T1 Touch Bar firmware handoff and apple-ib-tb wiring | open | P12: alternative | None |
| [omacom/omarchy#7140](https://github.com/omacom/omarchy/pull/7140) — Install CS8409 speaker driver on 2016-2017 MacBook Pros | closed | P11: superseded | None |
| [omacom/omarchy#7146](https://github.com/omacom/omarchy/pull/7146) — Disable the panel by overlay alone in clamshell recovery | open | P04: alternative; P05: alternative | None |
| [omacom/omarchy#7177](https://github.com/omacom/omarchy/pull/7177) — Mark the T2 Mac internal trackpad as internal | open | None | t2-trackpad |
| [omacom/omarchy#7180](https://github.com/omacom/omarchy/pull/7180) — Work around Apple BCM4350 suspend failures | open | P10: alternative | None |
| [omacom/omarchy#7196](https://github.com/omacom/omarchy/pull/7196) — Lock the lid and idle the Radeon on 15-inch 2016–2017 MacBook Pros | open | None | t1-lid-gpu |
| [omacom/omarchy#7333](https://github.com/omacom/omarchy/pull/7333) — Reset Apple BCM4350/BCM43602 Wi-Fi around sleep | open | P10: partial | None |
| [omacom/omarchy#7343](https://github.com/omacom/omarchy/pull/7343) — Stop forcing hid_apple fnmode=2 on Apple keyboards | open | None | apple-fnmode |
| [omacom/omarchy#7348](https://github.com/omacom/omarchy/pull/7348) — Install PipeWire ALSA support on T2 Macs | open | None | t2-alsa |
| [omacom/omarchy#7410](https://github.com/omacom/omarchy/pull/7410) — Point T2 overlay Limine at /boot/efi and write linux-t2 | open | None | t2-installation |
| [omacom/omarchy#7487](https://github.com/omacom/omarchy/pull/7487) — Fix broken Wi-Fi on 2015–2017 MacBook Pros by shipping the missing NVRAM file | open | P10: context | None |
| [omacom/omarchy#7589](https://github.com/omacom/omarchy/pull/7589) — Fix Mac suspend loop after the first resume from sleep | closed | P10: alternative | None |
| [omacom/omarchy#7594](https://github.com/omacom/omarchy/pull/7594) — Prevent idle hard-freeze on 2011 MacBook Airs (intel_idle.max_cstate=1) | open | None | sandy-idle |
| [omacom/omarchy#7644](https://github.com/omacom/omarchy/pull/7644) — fix: Bluetooth audio dropouts on Macs with Broadcom BT | open | None | bluetooth-audio |
| [omacom/omarchy#7671](https://github.com/omacom/omarchy/pull/7671) — Install BCM43602 NVRAM so 2017 Touch Bar Macs see 5 GHz Wi-Fi | closed | P10: included | None |
| [omacom/omarchy#7732](https://github.com/omacom/omarchy/pull/7732) — Add MacBookPro13,1 hardware support | open | P06: alternative; P08: alternative; P11: alternative | mbp131-bundle |
| [omacom/omarchy#7890](https://github.com/omacom/omarchy/pull/7890) — Reject Voxtype on CPUs without AVX2 | open | None | cpu-instructions |
| [omacom/omarchy#7950](https://github.com/omacom/omarchy/pull/7950) — Rebind the T1 Touch Bar's display sub-device so it doesn't stay dark | open | P12: alternative | None |
| [omacom/omarchy#8053](https://github.com/omacom/omarchy/pull/8053) — Route an all-in-one's built-in panel to the kernel backlight | closed | None | brightness-routing |
| [omacom/omarchy#8149](https://github.com/omacom/omarchy/pull/8149) — Skip Claude and Pi on CPUs without SSE4.2/POPCNT | closed | None | cpu-instructions |
| [omacom/omarchy#8204](https://github.com/omacom/omarchy/pull/8204) — Stop probing the internal T2 network interface | open | None | t2-ethernet |
| [omacom/omarchy#8205](https://github.com/omacom/omarchy/pull/8205) — Read actual gmux display brightness | open | None | gmux-brightness |
| [omacom/omarchy#8221](https://github.com/omacom/omarchy/pull/8221) — Reference count the Wi-Fi scanner so a closed panel cannot scan | open | None | wifi-scanning |
| [omacom/omarchy#8285](https://github.com/omacom/omarchy/pull/8285) — Enable speakers on pre-T2 MacBooks with the Cirrus CS8409 bridge | open | P11: alternative | None |
| [omacom/omarchy#8371](https://github.com/omacom/omarchy/pull/8371) — Save Apple GMUX backlight brightness across reboot | open | None | gmux-brightness |
| [omacom/omarchy#8524](https://github.com/omacom/omarchy/pull/8524) — Fix brightness lockout on displays with small max_brightness ranges | open | None | brightness-range |
| [omacom/omarchy#8560](https://github.com/omacom/omarchy/pull/8560) — Restore lock screen password focus lost on suspend | open | P04: alternative; P12: alternative | None |
| [omacom/omarchy#8572](https://github.com/omacom/omarchy/pull/8572) — Keep the Bluetooth pairing agent from skipping late USB adapters | closed | None | bluetooth-discovery |
| [omacom/omarchy#8585](https://github.com/omacom/omarchy/pull/8585) — Add the 2020 Intel MacBook Air to the T2 device list | open | None | model-docs |
| [omacom/omarchy#8709](https://github.com/omacom/omarchy/pull/8709) — fix: arm signature verification for the T2 repo and close the quattro override window | open | None | t2-repository |
| [omacom/omarchy#8783](https://github.com/omacom/omarchy/pull/8783) — Update 44-mac-support.md to add t2linux wiki link | open | None | model-docs |
| [omacom/omarchy#8812](https://github.com/omacom/omarchy/pull/8812) — Fix legacy Broadcom wl conflict on BCM4350 Macs upgrading to Quattro | open | P10: deferred | wifi-legacy |
| [omacom/omarchy#8882](https://github.com/omacom/omarchy/pull/8882) — Recover low-range displays from zero brightness | closed | None | brightness-range |
| [omacom/omarchy#9062](https://github.com/omacom/omarchy/pull/9062) — docs(mac): fix T1 chip model identifiers and remove non-Touch Bar A1708 | open | None | model-docs |
| [omacom/omarchy#9105](https://github.com/omacom/omarchy/pull/9105) — Use s2idle on T2 Macs with a discrete GPU | open | None | t2-suspend |
| [omacom/omarchy#9131](https://github.com/omacom/omarchy/pull/9131) — Wait for Bluetooth before starting its agent | open | None | bluetooth-discovery |
| [omacom/omarchy#9181](https://github.com/omacom/omarchy/pull/9181) — Restore lock password focus after resume | closed | P04: alternative; P12: alternative | None |
| [omacom/omarchy#9195](https://github.com/omacom/omarchy/pull/9195) — Keep T2 Mac USB-C ports awake after suspend | open | None | t2-suspend |
| [omacom/omarchy#9202](https://github.com/omacom/omarchy/pull/9202) — Stop a stuck PROCHOT from pinning T2 Macs at 800 MHz | open | None | cpu-power |
| [omacom/omarchy#9210](https://github.com/omacom/omarchy/pull/9210) — Stop T2 Mac resume from waiting on the Thunderbolt controllers | open | None | t2-suspend |
| [omacom/omarchy#9211](https://github.com/omacom/omarchy/pull/9211) — Wake the lock screen on resume and keep wake keys out of the password | open | P04: alternative; P12: alternative | None |
| [omacom/omarchy#9218](https://github.com/omacom/omarchy/pull/9218) — Detect Apple bcm5974 trackpads in omarchy-hw-touchpad | open | None | bcm5974-trackpad |
| [omacom/omarchy#9238](https://github.com/omacom/omarchy/pull/9238) — Refuse hibernation setup on Apple T2 Macs by default | open | None | t2-hibernation |
| [omacom/omarchy#9409](https://github.com/omacom/omarchy/pull/9409) — Fail clearly when trackpad reset finds no supported driver | open | None | bcm5974-trackpad |
| [omacom/omarchy#9461](https://github.com/omacom/omarchy/pull/9461) — [codex] OM-SEC-05: Remove the unsigned Apple T2 package source | open | None | t2-repository |
| [omacom/omarchy#9516](https://github.com/omacom/omarchy/pull/9516) — Install CS8409 speaker driver on pre-T2 MacBook Pros and iMacs | closed | P11: included | None |
| [omacom/omarchy#9590](https://github.com/omacom/omarchy/pull/9590) — Clear stale graphical-session before uwsm so SDDM autologin is not a blank screen | open | None | session-start |
| [omacom/omarchy#9637](https://github.com/omacom/omarchy/pull/9637) — Restore brightness when the laptop lid opens | open | P04: deferred | None |
| [omacom/omarchy#9692](https://github.com/omacom/omarchy/pull/9692) — Use DKMS for Broadcom wl across kernel updates | open | P02: superseded | None |
| [omacom/omarchy#9730](https://github.com/omacom/omarchy/pull/9730) — Expose image picker cursor control over IPC | open | None | image-picker |
| [omacom/omarchy#9735](https://github.com/omacom/omarchy/pull/9735) — Force SPI PIO on MacBook8,1 so the built-in keyboard works | open | P07: included | None |
| [omacom/omarchy#9796](https://github.com/omacom/omarchy/pull/9796) — Stop the Apple Studio Display flickering at 5K on T2 Macs | open | None | external-modes |
| [omacom/omarchy#9803](https://github.com/omacom/omarchy/pull/9803) — Fix WPA3 on MacBookPro16,1 | open | P10: deferred | wifi-t2-connectivity |
| [omacom/omarchy#9830](https://github.com/omacom/omarchy/pull/9830) — Fix T2 Mac suspend: s2idle, d3cold, and brcmfmac | open | None | t2-suspend |
| [omacom/omarchy#9878](https://github.com/omacom/omarchy/pull/9878) — Re-apply hardware pacman repos after a refresh restore | open | None | t2-repository |
| [omacom/omarchy#9880](https://github.com/omacom/omarchy/pull/9880) — Stop installing the obsolete SPI keyboard DKMS package | open | P06: included | None |
| [omacom/omarchy#9899](https://github.com/omacom/omarchy/pull/9899) — fix(hardware): prevent ~130s sleep wake stall on MacBook Pro 2016-2017 | open | None | alpine-ridge |
| [omacom/omarchy#9910](https://github.com/omacom/omarchy/pull/9910) — Persist apple-gmux panel brightness across reboots | closed | None | gmux-brightness |
| [sunoxen-lab/omarchy#1](https://github.com/sunoxen-lab/omarchy/pull/1) — Complete CS4208 volume and suspend setup for Omarchy #6921 | open | P11: partial | None |

## Separate work tracks

These are retained scope, not completed consolidation PRs. Each source keeps its existing PR as the review/test target until the feature comparison is complete.

### alpine-ridge

Thunderbolt/USB controller recovery is a separate work track: DKMS/kernel correction, PCI removal/rescan, wake-source masking and global USB policy are not interchangeable. Keep model-specific source targets; no universal suspend policy is selected.

[omacom/omarchy-pkgs#349](https://github.com/omacom/omarchy-pkgs/pull/349), [omacom/omarchy-pkgs#544](https://github.com/omacom/omarchy-pkgs/pull/544), [omacom/omarchy#10140](https://github.com/omacom/omarchy/pull/10140), [omacom/omarchy#10758](https://github.com/omacom/omarchy/pull/10758), [omacom/omarchy#11570](https://github.com/omacom/omarchy/pull/11570), [omacom/omarchy#12211](https://github.com/omacom/omarchy/pull/12211), [omacom/omarchy#5970](https://github.com/omacom/omarchy/pull/5970), [omacom/omarchy#7044](https://github.com/omacom/omarchy/pull/7044), [omacom/omarchy#9899](https://github.com/omacom/omarchy/pull/9899)

### apple-fnmode

Keep the existing Apple keyboard function-row policy proposal separate from layout-widget device eligibility. Preserve administrator settings and the non-Apple keyboard behavior during eventual review.

[omacom/omarchy#7343](https://github.com/omacom/omarchy/pull/7343)

### applesmc-fans

Keep the single-fan applesmc supervisor package as an opt-in package review; no automatic fan-control installation is added to the 14 feature branches.

[omacom/omarchy-pkgs#476](https://github.com/omacom/omarchy-pkgs/pull/476)

### audio-realtime

Keep rtkit activation/retry behavior as an independent shared-audio proposal. The prior local experimental patch is not part of the published Cirrus roll-up.

[omacom/omarchy#12428](https://github.com/omacom/omarchy/pull/12428)

### baffin-capture

Keep the existing Baffin CPU-encoding workaround as a distinct capture proposal. It does not establish general Radeon or suspend stability.

[omacom/omarchy#10125](https://github.com/omacom/omarchy/pull/10125)

### battery-limits

Keep battery-state display and charge-threshold support as a separate feature. Administrative duplicate closure does not settle threshold parsing, pending-charge behavior or hardware support.

[omacom/omarchy-pkgs#516](https://github.com/omacom/omarchy-pkgs/pull/516), [omacom/omarchy#10196](https://github.com/omacom/omarchy/pull/10196), [omacom/omarchy#10502](https://github.com/omacom/omarchy/pull/10502)

### bcm5974-trackpad

Keep device recognition and reset error handling separate from SPI PIO and T2 internal-device tagging. Existing source targets retain the older bcm5974 coverage.

[omacom/omarchy#9218](https://github.com/omacom/omarchy/pull/9218), [omacom/omarchy#9409](https://github.com/omacom/omarchy/pull/9409)

### bluetooth-audio

Retain the ACL-priority and dropout work as distinct Bluetooth policies; similar audio symptoms do not establish compatible controller/transport changes.

[omacom/omarchy#10485](https://github.com/omacom/omarchy/pull/10485), [omacom/omarchy#7644](https://github.com/omacom/omarchy/pull/7644)

### bluetooth-discovery

Keep pairing-agent lifecycle and USB/controller power policy separate. Preserve the MacBookPro12,1 report and the explicit successor to #8572; Apple Silicon-only reports are adjacent evidence, not Intel validation.

[omacom/omarchy#10111](https://github.com/omacom/omarchy/pull/10111), [omacom/omarchy#11937](https://github.com/omacom/omarchy/pull/11937), [omacom/omarchy#8572](https://github.com/omacom/omarchy/pull/8572), [omacom/omarchy#9131](https://github.com/omacom/omarchy/pull/9131)

### brightness-range

A prior local experimental consolidation exists, but it was not one of the 14 published implementation branches. Retain both original patches and their differing minimum/step policies; do not describe the experiment as shipped in the ISO.

[omacom/omarchy#8524](https://github.com/omacom/omarchy/pull/8524), [omacom/omarchy#8882](https://github.com/omacom/omarchy/pull/8882)

### brightness-routing

Keep AIO kernel-backlight routing, missing-backlight software dimming and Apple Silicon panel preference separate. They require different output-ownership rules; no universal fallback is selected.

[omacom/omarchy#10234](https://github.com/omacom/omarchy/pull/10234), [omacom/omarchy#11312](https://github.com/omacom/omarchy/pull/11312), [omacom/omarchy#12267](https://github.com/omacom/omarchy/pull/12267), [omacom/omarchy#8053](https://github.com/omacom/omarchy/pull/8053)

### cpu-instructions

Keep AVX2 and SSE4.2/POPCNT application eligibility as separate older-CPU support. Track #8149 through its explicit #11514 successor; an x86_64 CPU alone does not prove every bundled application can execute.

[omacom/omarchy#11514](https://github.com/omacom/omarchy/pull/11514), [omacom/omarchy#7890](https://github.com/omacom/omarchy/pull/7890), [omacom/omarchy#8149](https://github.com/omacom/omarchy/pull/8149)

### cpu-power

Keep MacBook10,1 RAPL limits, pre-HWP profile mapping and T2 policy/PROCHOT changes separate. Their model-specific power values are not generalized to other Macs.

[omacom/omarchy#10313](https://github.com/omacom/omarchy/pull/10313), [omacom/omarchy#11432](https://github.com/omacom/omarchy/pull/11432), [omacom/omarchy#5136](https://github.com/omacom/omarchy/pull/5136), [omacom/omarchy#9202](https://github.com/omacom/omarchy/pull/9202)

### efi-preservation

Full-disk EFI preservation is an ISO delivery dependency, not a runtime driver feature. Both existing source commits are preserved in the revised ISO source; nine unit tests and a fresh VM disk-wipe round trip passed, including all three synthetic file hashes. Physical firmware preservation remains untested and requires an independent external backup. Historical B7 lacks the contribution.

[omacom/omarchy-iso#174](https://github.com/omacom/omarchy-iso/pull/174)

### external-modes

Retain the existing T2/Studio Display link proposal as a separate external-display test target. The 14 branches do not select link rates or certify 5K DSC behavior.

[omacom/omarchy#9796](https://github.com/omacom/omarchy/pull/9796)

### gmux-brightness

Separate reading actual gmux brightness from persistence across reboot. Retain #8205 independently and compare the #8371/#9910 persistence implementations despite duplicate closure.

[omacom/omarchy#8205](https://github.com/omacom/omarchy/pull/8205), [omacom/omarchy#8371](https://github.com/omacom/omarchy/pull/8371), [omacom/omarchy#9910](https://github.com/omacom/omarchy/pull/9910)

### haswell-voxtype

Retain the existing Haswell Vulkan-to-CPU backend proposal independently from CPU instruction gating and general VA-API selection.

[omacom/omarchy#11481](https://github.com/omacom/omarchy/pull/11481)

### imac-5k

Retain iMac18,3 documentation and reported gaps as a distinct model record. Adding a model name does not supply the linked patcher or validate all four gaps.

[omacom/omarchy#11464](https://github.com/omacom/omarchy/pull/11464)

### imac-gpu-boot

Retain the exact iMac20,2 AMD/Apple PCI-gated UCLK proposal as a separate GPU trial. Do not extend its power-feature mask to the available 13,3 or other iMac GPUs.

[omacom/omarchy#10169](https://github.com/omacom/omarchy/pull/10169)

### image-picker

Retain optional picker IPC as an independent desktop integration proposal. It is not required by the selected released T1Bridge provider and does not imply hardware enablement.

[omacom/omarchy#9730](https://github.com/omacom/omarchy/pull/9730)

### intel-video

Retain pre-Broadwell VA-API selection as its own installer proposal, including Haswell/Ivy Bridge evidence. No driver-generation correction is supplied by the current detection roll-up.

[omacom/omarchy#11592](https://github.com/omacom/omarchy/pull/11592)

### keyboard-backlight-state

Retain saved-state/restore ownership as a separate concern shared by lock, idle and sleep. Do not stack alternate save/restore implementations into T1Bridge automatically.

[omacom/omarchy#10366](https://github.com/omacom/omarchy/pull/10366), [omacom/omarchy#11404](https://github.com/omacom/omarchy/pull/11404)

### keyboard-backlight-steps

Retain old media bindings and the competing fixed-four-level versus symmetric-step policies separately; these are not the same feature as keyboard-device layout selection.

[omacom/omarchy#2331](https://github.com/omacom/omarchy/pull/2331), [omacom/omarchy#5424](https://github.com/omacom/omarchy/pull/5424), [omacom/omarchy#6533](https://github.com/omacom/omarchy/pull/6533)

### legacy-gpu

Retain the existing MacBookPro11,5 radeon selection as a model-specific driver trial. It is not a generic recommendation to switch or disable GPUs on Intel Macs.

[omacom/omarchy#11548](https://github.com/omacom/omarchy/pull/11548)

### mbp131-bundle

Keep the complete MacBookPro13,1 package/runtime bundle visible across camera, audio and SPI retirement. A single feature branch does not supersede all of its delivered behavior.

[omacom/omarchy-pkgs#182](https://github.com/omacom/omarchy-pkgs/pull/182), [omacom/omarchy#7732](https://github.com/omacom/omarchy/pull/7732)

### mbp133-bundle

Retain the broader MacBookPro13,3 bundle and its negative Radeon/suspend evidence. Selected calibration or NVMe components do not establish that the whole bundle is included or stable.

[omacom/omarchy#10141](https://github.com/omacom/omarchy/pull/10141)

### model-docs

Retain the separate model-list corrections and T2 resource link. Model documentation remains useful across the full Intel scope, independently of which machine is tested first.

[omacom/omarchy#10783](https://github.com/omacom/omarchy/pull/10783), [omacom/omarchy#8585](https://github.com/omacom/omarchy/pull/8585), [omacom/omarchy#8783](https://github.com/omacom/omarchy/pull/8783), [omacom/omarchy#9062](https://github.com/omacom/omarchy/pull/9062)

### older-macs

Keep pre-T1 graphics/Wi-Fi/application gaps and the iMac7,1 evidence visible. Core 2 Duo machines are in scope where x86_64-capable; 32-bit-only Intel Macs are not implied by broad year ranges.

[omacom/omarchy#10936](https://github.com/omacom/omarchy/pull/10936), [omacom/omarchy#10942](https://github.com/omacom/omarchy/pull/10942)

### outside-scope

Generic night-light temperature preference has no established Intel Mac compatibility requirement in the inventory evidence. Retain as excluded context, not as a missing hardware fix.

[omacom/omarchy#12337](https://github.com/omacom/omarchy/pull/12337)

### picture-in-picture

The prior local study retained the source unchanged. Keep the original as the independent desktop proposal; no additional consolidation branch is warranted for this single source.

[omacom/omarchy#12517](https://github.com/omacom/omarchy/pull/12517)

### pre-t2-hibernation

Retain delayed GPU initialization during hibernation as a separate boot/resume proposal; normal suspend and NVMe power-state changes do not cover it.

[omacom/omarchy#10065](https://github.com/omacom/omarchy/pull/10065)

### sandy-idle

Keep the existing MacBookAir4,1/4,2 C-state cap as a narrow model-specific trial, with its power tradeoff explicit. Do not generalize the cap to all older Intel CPUs.

[omacom/omarchy#7594](https://github.com/omacom/omarchy/pull/7594)

### sd-reader

Keep the Apple USB card-reader recovery as a separate peripheral track. Its GPIO and controller assumptions must not be inferred from the first physical test machine.

[omacom/omarchy#10139](https://github.com/omacom/omarchy/pull/10139)

### session-start

Keep the existing Macmini7,1 graphical-session cleanup proposal independent of lid handling and output enumeration; it changes session startup ownership.

[omacom/omarchy#9590](https://github.com/omacom/omarchy/pull/9590)

### t1-lid-gpu

Retain the existing stay-awake lid/GPU bundle separately. Avoiding suspend is a distinct policy with thermal implications, not evidence that suspend has been fixed.

[omacom/omarchy#7196](https://github.com/omacom/omarchy/pull/7196)

### t1-pcie

Retain the existing T1 PCIe command-line migration as its own upgrade proposal. Removing pcie_ports=compat and adding sleep defaults is not implied by T1Bridge or SPI retirement.

[omacom/omarchy#10886](https://github.com/omacom/omarchy/pull/10886)

### t2-alsa

Retain T2 overlay-install PipeWire ALSA availability separately from pre-T2 Cirrus packages; the driver stacks and installation paths differ.

[omacom/omarchy#7348](https://github.com/omacom/omarchy/pull/7348)

### t2-ethernet

Keep the T2 internal NCM exclusion pair as a separate network track, with #10224 closed in favor of #8204. External Ethernet must remain outside that exclusion.

[omacom/omarchy#10224](https://github.com/omacom/omarchy/pull/10224), [omacom/omarchy#8204](https://github.com/omacom/omarchy/pull/8204)

### t2-fan-resume

Retain the newly discovered iMac20,1 t2fanrd post-resume restart proposal as a separate T2 cooling track. It is not the pre-T2 single-fan afanctl package.

[omacom/omarchy#12590](https://github.com/omacom/omarchy/pull/12590)

### t2-gmux

Keep the T2 mux/rendering backend as a distinct model-specific graphics trial, including external-display and GPU-power limits. It is not transplanted onto pre-T2 gmux machines.

[omacom/omarchy#6929](https://github.com/omacom/omarchy/pull/6929)

### t2-hibernation

Retain the existing T2 hibernation refusal policy separately from changes that attempt to enable suspend; an S3 or s2idle report does not validate S4.

[omacom/omarchy#9238](https://github.com/omacom/omarchy/pull/9238)

### t2-imac-framebuffer

Retain the exact Navi 14 iMac20,x EFI-framebuffer proposal independently of the other iMac UCLK workaround; GPU IDs and failure stages differ.

[omacom/omarchy#12203](https://github.com/omacom/omarchy/pull/12203)

### t2-installation

Retain the existing T2 overlay ESP/Linux-entry migration as a separate installation track. It is not covered by full-disk T1 firmware preservation.

[omacom/omarchy#7410](https://github.com/omacom/omarchy/pull/7410)

### t2-power-docs

Retain the MacBookPro16,1 power/graphics guide as model-specific evidence and optional settings. Do not turn its local demand controller into a universal installer policy.

[omacom/omarchy#12200](https://github.com/omacom/omarchy/pull/12200)

### t2-repository

Retain signature-policy, signed-package replacement and repository-refresh proposals as distinct operations. Select authenticated available delivery before changing T2 package sources; the current roll-ups do not settle that repository migration.

[omacom/omarchy#8709](https://github.com/omacom/omarchy/pull/8709), [omacom/omarchy#9461](https://github.com/omacom/omarchy/pull/9461), [omacom/omarchy#9878](https://github.com/omacom/omarchy/pull/9878)

### t2-suspend

Keep model-specific async ordering, deep/s2idle, controller power and Wi-Fi lifecycle trials separate. Positive and contrary reports coexist; no single T2 sleep policy is selected from classifier similarity.

[omacom/omarchy#6149](https://github.com/omacom/omarchy/pull/6149), [omacom/omarchy#9105](https://github.com/omacom/omarchy/pull/9105), [omacom/omarchy#9195](https://github.com/omacom/omarchy/pull/9195), [omacom/omarchy#9210](https://github.com/omacom/omarchy/pull/9210), [omacom/omarchy#9830](https://github.com/omacom/omarchy/pull/9830)

### t2-trackpad

Keep the T2 internal-trackpad proposals together for comparison, preserving product-ID instability and logout/reboot evidence from closed #10890. Do not substitute SPI work for the USB/libinput classification change.

[omacom/omarchy#10890](https://github.com/omacom/omarchy/pull/10890), [omacom/omarchy#6928](https://github.com/omacom/omarchy/pull/6928), [omacom/omarchy#7177](https://github.com/omacom/omarchy/pull/7177)

### thunderbolt-kernel

The supplied reproduction uses an AMD mini PC with an Apple display, not an Intel Mac host. Retain adjacent kernel context until an Intel Mac requirement is established.

[omacom/omarchy-pkgs#509](https://github.com/omacom/omarchy-pkgs/pull/509)

### trackpad-defaults

Retain optional gesture documentation as a customization proposal, separate from input-driver or palm-rejection support.

[omacom/omarchy#11296](https://github.com/omacom/omarchy/pull/11296)

### wifi-country

Regulatory hinting remains a distinct P10 follow-up; preserve an existing deliberate country setting rather than deriving calibration policy from signal symptoms.

[omacom/omarchy#11748](https://github.com/omacom/omarchy/pull/11748)

### wifi-firmware

Firmware availability for non-T2 brcmfmac Macs remains a separate P10 delivery concern; two selected NVRAM files do not supply every model firmware.

[omacom/omarchy#10306](https://github.com/omacom/omarchy/pull/10306)

### wifi-legacy

Preserve BCM4322 b43, BCM43224 wl and BCM4350 upgrade-driver selection as distinct P10 tracks. Their driver/blacklist policies cannot be combined by chip-vendor name alone.

[omacom/omarchy#10910](https://github.com/omacom/omarchy/pull/10910), [omacom/omarchy#11311](https://github.com/omacom/omarchy/pull/11311), [omacom/omarchy#8812](https://github.com/omacom/omarchy/pull/8812)

### wifi-scanning

Retain shared UI scan ownership as a separate network-panel proposal, not a firmware or RF calibration change.

[omacom/omarchy#8221](https://github.com/omacom/omarchy/pull/8221)

### wifi-t2-combo

Keep T2 combo-device and simple post-resume recovery separate from the selected pre-T2 hook; inspect complete ordering and known failure reports before any T2 integration.

[omacom/omarchy#11536](https://github.com/omacom/omarchy/pull/11536), [omacom/omarchy#5140](https://github.com/omacom/omarchy/pull/5140)

### wifi-t2-connectivity

Keep MacBookPro16,1 SAE/WPA3 policy as its own P10 follow-up; current calibration and recovery do not implement it.

[omacom/omarchy#9803](https://github.com/omacom/omarchy/pull/9803)
