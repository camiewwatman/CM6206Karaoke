# Hardware & Platform Testing Matrix

The CM6206 Audio Controller has currently been developed and tested primarily on a **Raspberry Pi 3 Model B**. Testing on the following platforms would help identify USB, ALSA, systemd, architecture, performance and installer compatibility issues.

## Raspberry Pi Hardware

- [x] **Raspberry Pi 3 Model B**
  - Current development/test platform
  - ARM
  - Baseline for startup optimisation testing

- [ ] **Raspberry Pi 3 Model B+**
  - Validate compatibility with the later Pi 3 platform
  - Compare boot performance with the Pi 3B

- [ ] **Raspberry Pi 4 Model B - 1 GB**
- [ ] **Raspberry Pi 4 Model B - 2 GB**
- [ ] **Raspberry Pi 4 Model B - 4 GB**
- [ ] **Raspberry Pi 4 Model B - 8 GB**
  - Validate newer USB controller behaviour
  - Validate CM6206 detection and reconnect handling
  - Compare boot optimisation results

- [ ] **Raspberry Pi 5 - 2 GB**
- [ ] **Raspberry Pi 5 - 4 GB**
- [ ] **Raspberry Pi 5 - 8 GB**
- [ ] **Raspberry Pi 5 - 16 GB**
  - Validate newest Raspberry Pi architecture/platform
  - Validate USB audio/HID behaviour
  - Compare whether startup optimisation remains beneficial

- [ ] **Raspberry Pi Zero 2 W**
  - Important low-power candidate
  - Test performance with Flask/Gunicorn
  - Test whether limited resources affect audio control responsiveness

- [ ] **Raspberry Pi 400**
  - Validate Pi 4-derived platform

- [ ] **Raspberry Pi Compute Module 4**
  - Useful for embedded/product deployments
  - Test USB implementation and carrier-board dependencies

- [ ] **Raspberry Pi Compute Module 5**
  - Useful for future embedded/commercial implementations

## Operating Systems

### Raspberry Pi OS

- [ ] **Raspberry Pi OS Lite 32-bit**
- [X] **Raspberry Pi OS Lite 64-bit**
- [ ] **Raspberry Pi OS Desktop 32-bit**
- [ ] **Raspberry Pi OS Desktop 64-bit**

Testing both Lite and Desktop is particularly important because the startup optimiser deliberately targets a headless/appliance configuration.

### Debian

- [ ] **Debian 12 Bookworm - ARM64**
- [ ] **Debian 13 Trixie - ARM64**
- [ ] **Debian 12 Bookworm - AMD64**
- [ ] **Debian 13 Trixie - AMD64**

### Ubuntu

- [ ] **Ubuntu Server 24.04 LTS - ARM64**
- [ ] **Ubuntu Server 24.04 LTS - AMD64**

## Non-Raspberry Pi ARM Systems

These are useful for determining whether the project is genuinely portable or still contains Raspberry Pi-specific assumptions.

- [ ] **Orange Pi**
- [ ] **Rock Pi**
- [ ] **ODROID**
- [ ] **NVIDIA Jetson**
- [ ] **Generic ARM64 Debian system**

## x86-64 Systems

Testing x86-64 is useful because `cm6206ctl`, HIDAPI, ALSA and the Flask application are not inherently limited to Raspberry Pi hardware.

- [ ] **Intel NUC / Mini PC**
- [ ] **AMD Mini PC**
- [ ] **Generic Debian x86-64**
- [ ] **Generic Ubuntu x86-64**

## Virtualised Systems

USB passthrough should specifically be tested.

- [ ] **Proxmox VM with USB passthrough**
- [ ] **VMware VM with USB passthrough**
- [ ] **Hyper-V VM with USB redirection/passthrough**
- [ ] **VirtualBox VM with USB passthrough**

> Virtual machines are primarily useful for installer and software compatibility testing. Audio timing, USB reset and S/PDIF behaviour may differ significantly from physical hardware.

# Tests to Perform on Each Platform

## Installation

- [ ] Standard installer completes successfully
- [ ] Optimised installer completes successfully
- [ ] Required packages install correctly
- [ ] `cm6206ctl` compiles successfully
- [ ] Python virtual environment builds successfully
- [ ] Flask installs successfully
- [ ] Gunicorn installs successfully
- [ ] systemd units install correctly
- [ ] udev rules install correctly
- [ ] sudoers validation succeeds

## CM6206 Detection

- [ ] CM6206 USB device detected
- [ ] `ICUSBAUDIO7D` ALSA card detected
- [ ] HID interface accessible
- [ ] `cm6206ctl` can communicate with device
- [ ] ALSA controls are available

## Audio

- [ ] TOSLINK PCM input works
- [ ] PCM output works
- [ ] Microphone input works
- [ ] Line input works
- [ ] Microphone + Line mixing works
- [ ] S/PDIF output works
- [ ] Encoded/Dolby passthrough works
- [ ] Switching back to PCM works correctly
- [ ] Multiple repeated PCM/Encoded transitions work reliably

## Web Interface

- [ ] Web UI starts automatically
- [ ] Web UI accessible on port 80
- [ ] `/api/status` works
- [ ] PCM mode switching works
- [ ] Dolby/Encoded mode switching works
- [ ] Line volume control works
- [ ] Microphone volume control works
- [ ] Slider updates work reliably
- [ ] Web service survives repeated requests

## USB Reconnection

- [ ] Disconnect CM6206
- [ ] Reconnect CM6206
- [ ] udev event detected
- [ ] CM6206 setup automatically reapplied
- [ ] ALSA controls restored
- [ ] Web UI continues working
- [ ] PCM mode works after reconnect
- [ ] Encoded mode works after reconnect

## Reboot Testing

- [ ] Cold boot
- [ ] Warm reboot
- [ ] CM6206 connected during boot
- [ ] CM6206 disconnected during boot
- [ ] CM6206 connected after boot
- [ ] Web service starts successfully
- [ ] Audio routing configured automatically

## Startup Optimiser

Run:

    systemd-analyze time
    systemd-analyze blame
    systemd-analyze critical-chain

Record:

- [ ] Baseline boot time
- [ ] Optimised boot time
- [ ] Time saved
- [ ] Percentage improvement
- [ ] Time to `multi-user.target`
- [ ] `NetworkManager` impact
- [ ] `cloud-init` impact
- [ ] APT service/timer impact
- [ ] Swap service impact
- [ ] CM6206 setup-service duration

# Test Result Template

| Platform | OS | Arch | Install | PCM | Encoded | Mic | Web UI | Reconnect | Optimiser | Result |
|---|---|---|---|---|---|---|---|---|---|---|
| Raspberry Pi 3B | Raspberry Pi OS | ARM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Tested |
| Raspberry Pi 3B+ | TBD | ARM | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Needed |
| Raspberry Pi 4B | TBD | ARM64 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Needed |
| Raspberry Pi 5 | TBD | ARM64 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Needed |
| Raspberry Pi Zero 2 W | TBD | ARM | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | Needed |
| Debian PC | Debian | AMD64 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | N/A | Needed |
| Ubuntu PC | Ubuntu | AMD64 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | N/A | Needed |

## Highest-Priority Community Testing

If hardware availability is limited, testing should be prioritised in this order:

1. **Raspberry Pi 4B running Raspberry Pi OS Lite 64-bit**
2. **Raspberry Pi 5 running Raspberry Pi OS Lite 64-bit**
3. **Raspberry Pi Zero 2 W**
4. **Raspberry Pi 3B+**
5. **Debian ARM64**
6. **Ubuntu Server ARM64**
7. **Debian/Ubuntu AMD64**
8. **Other ARM single-board computers**
9. **Virtual machines with USB passthrough**

The most valuable test reports should include the exact Raspberry Pi model, OS release, architecture, CM6206 USB identification, installer used, `systemd-analyze time` output, and whether PCM, encoded passthrough, microphone mixing and USB reconnect handling all passed.