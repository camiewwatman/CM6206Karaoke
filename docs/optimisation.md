# Raspberry Pi 3B Startup Optimisation: Performance vs Trade-offs

This note documents the **optional Raspberry Pi startup optimisation** used with the CM6206 Audio Controller project. It is intentionally separate from the standard installer because the changes make sense for a **dedicated, headless audio appliance**, but not necessarily for a general-purpose Raspberry Pi.

## Measured result on the Raspberry Pi 3B

The optimisation work reduced the measured boot path on the test Raspberry Pi 3B from approximately **44.9 seconds** to approximately **32.2 seconds** to reach `multi-user.target`.

| Measurement | Before | After | Improvement |
|---|---:|---:|---:|
| Overall startup | 44.864 s | 32.204 s | **12.660 s faster** |
| Reduction |  |  | **~28.2%** |

The measured `multi-user.target` point also improved from approximately **34.8 seconds** in the initial run to approximately **26.1 seconds** after optimisation.

> **Important:** these figures are observations from the Raspberry Pi 3B used to develop this project. They are not a guaranteed benchmark. SD-card performance, Raspberry Pi OS version, DHCP/network behaviour, installed services, USB hardware and system configuration can materially change the result.

## What was actually slow

The CM6206 configuration itself was not the main source of the long boot time. During diagnosis, `systemd-analyze blame` showed several general-purpose Raspberry Pi OS services contributing substantially to startup, including:

- `NetworkManager.service`
- `cloud-init-main.service`
- `rpi-resize-swap-file.service`
- `apt-daily-upgrade.service`

The CM6206 setup service was subsequently measured at around **1.05 seconds**, so optimising the surrounding operating-system boot path produced a much larger benefit than aggressively trimming the audio setup itself.

## Optimisations and their trade-offs

### 1. Disable NetworkManager wait-online

The optimiser disables and masks:

`NetworkManager-wait-online.service`

**Benefit**

Boot no longer waits for NetworkManager to declare networking fully online before continuing. This is useful for the CM6206 appliance because the core audio routing does not require Internet access before it can start.

**Trade-off**

A service that genuinely requires a working network immediately at boot may now start before DHCP, DNS or the default route is ready.

This is acceptable for the CM6206 controller because Gunicorn can start independently and the network can become usable shortly afterward. It may not be appropriate if the same Pi hosts network storage, remote mounts, databases or other services with strict online dependencies.

### 2. Remove cloud-init

The optimiser removes:

- `cloud-init`
- `rpi-cloud-init-mods`
- retained `/etc/cloud` and `/var/lib/cloud` state

**Benefit**

A permanently configured Raspberry Pi appliance does not need a general cloud-provisioning framework to run during startup. On the development Pi, `cloud-init-main.service` accounted for several seconds in the original boot profile.

**Trade-off**

The system can no longer rely on cloud-init for automated provisioning, first-boot configuration, instance metadata or subsequent cloud-init workflows.

Do **not** apply this optimisation to an image or deployment process that still depends on cloud-init.

### 3. Disable automatic APT timers

The optimiser disables:

- `apt-daily.timer`
- `apt-daily-upgrade.timer`

**Benefit**

Package maintenance will not unexpectedly compete for CPU, SD-card I/O or network access around startup. This makes appliance behaviour more deterministic.

**Trade-off**

Automatic package updates are no longer being scheduled by these timers. The operator must deliberately maintain the Raspberry Pi, for example:

```bash
sudo apt update
sudo apt full-upgrade
```

For an Internet-connected device, this is a meaningful security responsibility rather than a free performance optimisation.

### 4. Mask the Raspberry Pi swap resize service

The optimiser masks:

`rpi-resize-swap-file.service`

**Benefit**

The system avoids running an unnecessary swap-resize operation during startup once the appliance's memory/swap configuration is already established.

**Trade-off**

If the storage layout or swap configuration is later changed, the automatic Raspberry Pi resize mechanism will no longer run unless it is explicitly restored.

This change does **not** inherently disable an existing zram swap device.

### 5. Boot to `multi-user.target`

The optimiser sets:

```bash
sudo systemctl set-default multi-user.target
```

**Benefit**

The Pi boots as a headless system rather than starting a graphical desktop that is unnecessary for a browser-controlled audio appliance.

**Trade-off**

A locally attached graphical desktop is no longer the default boot experience. Users wanting the Raspberry Pi desktop should use the standard installation or restore the graphical target.

## Why there are two installers

The project deliberately provides two installation paths.

### Standard

```bash
sudo ./install.sh
```

Use this if the Raspberry Pi is multipurpose, if you want normal Raspberry Pi OS background behaviour, or if you are unsure whether other workloads depend on the services above.

### Appliance-optimised

```bash
sudo ./install-optimised.sh
```

Use this for a dedicated Raspberry Pi 3B CM6206 controller where faster, more deterministic startup is worth giving up some general-purpose OS conveniences.

The optimisations themselves remain isolated in:

`optimisation/optimise-raspberry-pi.sh`

This keeps the audio/web installation modular and makes the appliance-level policy decision explicit.

## Reproducing the measurements

Before making changes:

```bash
systemd-analyze time
systemd-analyze blame
systemd-analyze critical-chain
```

Run the same commands again after installation and reboot. In particular, compare:

- total userspace startup time;
- time to `multi-user.target`;
- the largest entries in `systemd-analyze blame`;
- the dependency path reported by `systemd-analyze critical-chain`.

For meaningful comparisons, perform more than one boot and avoid treating a single run as a universal Raspberry Pi 3B benchmark.

## Bottom line

On the Raspberry Pi 3B used for this project, the optimisation work cut the observed overall startup from **44.864 seconds to 32.204 seconds**, a reduction of **12.660 seconds or about 28%**.

That improvement comes from turning a general-purpose Raspberry Pi OS installation into something closer to a dedicated appliance. The cost is less automatic provisioning, less automatic package maintenance, no default graphical desktop, and less conservative network startup behaviour.

For a dedicated CM6206 controller those are reasonable trade-offs. For a general-purpose Raspberry Pi, the standard installer is the safer default.
