# Hardware validation boundaries

The ISO is a shared candidate, not a statement that every Intel Mac boots or that every inventoried PR is implemented. In particular, a 64-bit CPU does not by itself establish compatibility with this ISO's boot firmware and graphics requirements. Old EFI/graphics generations need their own trial.

| Hardware family / concern | Coordination target or retained track | Evidence still required |
| --- | --- | --- |
| Shared keyboard UI, headers and sysfs detection | P01–P03 | Real Mac input and installed kernel/header combinations; non-Apple VM software checks passed |
| Lid, display topology and lock recovery across pre-T1/T1/T2 | P04–P05, P12 alternatives | Real lid switches, internal/external outputs and reader behavior; these are not inferred from a virtual monitor |
| Legacy SPI and MacBook8,1 PIO | P06–P07 | SPI initramfs/encrypted unlock; MacBook8,1 controller behavior; prepared provider migration |
| Broadcom PCIe FaceTime camera | P08 | PCIe camera capture on the supported physical hardware; T1 USB camera results do not substitute |
| Apple NVMe at selected controller/model boundary | P09 | Confirm vendor/device/address and real sleep behavior; MacBookPro13,3 is excluded by the selected installer |
| BCM4350/BCM43602 pre-T2 recovery and model-specific calibration | P10 | Chip/subsystem/model matrix, traffic and sleep cycles; custom-kernel #422 remains a separate trial |
| T2 Broadcom combo devices and firmware delivery | P10 alternatives + retained T2 tracks | Complete Wi-Fi/Bluetooth lifecycle on actual T2 hardware; no extrapolation from 13,3 |
| CS4208 MacBooks, CS8409 MacBooks, CS4208/CS8409 iMacs | P11 and package companion | Separate codec/model speaker and input results; source closures do not remove iMac evidence |
| T1Bridge on 2016–2017 Touch Bar models | P12 and package companion; ISO #174 | Firmware preservation, manual provider setup, Touch Bar/camera/ALS/Touch ID on each model |
| Shared fingerprint lock UI, including T2 reports | P12 | Device enrollment and failure/recovery behavior; VM tests cover password fallback and software lifecycle only |
| Apple kernel exceptions and proposed custom kernels | P13 | Hardware/kernel-specific results; #422 and package #544 are alternatives, not both installed automatically |
| Suspend diagnostics | P14 | Observations from actual failing/resuming machines; diagnostics do not prove a causal fix |
| T2 kernel/input/audio/network, fan/charge policy, Bluetooth, Thunderbolt, hibernation, GPU and old EFI work outside selected groups | Named separate work tracks in INVENTORY.md | Remain reviewed/triaged only to the stated depth, with original PRs retained as work targets. Not claimed implemented by this ISO. |

The first available machine is MacBookPro13,3. Record its outcome without changing the project's inclusion scope. Keep unsupported, deferred and competing implementations visible for owners of other hardware.
