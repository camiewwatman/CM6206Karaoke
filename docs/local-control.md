# Local Control and GPIO Integration

The CM6206 Audio Controller does not require the Flask web interface.

All core audio functions can be controlled locally using command-line tools. This also makes it straightforward to integrate the controller with:

- Physical GPIO buttons
- Toggle switches
- Shell scripts
- Python applications
- Home Assistant
- MQTT
- Node-RED
- Other automation systems

---

# Quick Reference

| Function | Command |
|---|---|
| Switch to PCM + microphone mixing | `sudo /usr/local/sbin/cm6206-mode pcm` |
| Switch to encoded/Dolby passthrough | `sudo /usr/local/sbin/cm6206-mode encoded` |
| Reapply complete CM6206 configuration | `sudo /usr/local/sbin/cm6206-setup.sh` |
| Check current mode | `cat /run/cm6206-mode` |
| Restart CM6206 setup service | `sudo systemctl restart cm6206-setup.service` |
| View setup logs | `journalctl -u cm6206-setup.service` |
| Find CM6206 ALSA card | `grep -H ICUSBAUDIO7D /proc/asound/card*/id` |
| Display ALSA controls | `amixer -c CARD scontrols` |
| Set Line In volume | `amixer -c CARD sset Line 50% cap` |
| Set microphone volume | `amixer -c CARD sset Mic 50% cap` |

Replace `CARD` with the ALSA card number assigned to `ICUSBAUDIO7D`.

---

# Mode Control

## PCM + Microphone Mixing

Switch the CM6206 into PCM/mixer mode:

```bash
sudo /usr/local/sbin/cm6206-mode pcm
```

This is the normal mode used for the following audio path:

```text
TOSLINK PCM Input
        |
        v
    Front Output
        |
        v
 External TRS Loop
        |
        v
      Line In
        +
    Microphone
        |
        v
       Mixer
        |
        v
   S/PDIF Output
```

Check the current mode:

```bash
cat /run/cm6206-mode
```

Expected result:

```text
pcm
```

---

## Dolby / Encoded S/PDIF Passthrough

Switch to encoded passthrough:

```bash
sudo /usr/local/sbin/cm6206-mode encoded
```

This bypasses the PCM microphone mixing path and is intended for encoded S/PDIF streams such as Dolby Digital.

Check the current mode:

```bash
cat /run/cm6206-mode
```

Expected result:

```text
encoded
```

---

# Volume Control

The volume commands require the ALSA card number assigned to the CM6206.

## Find the CM6206 ALSA Card

Run:

```bash
grep -H ICUSBAUDIO7D /proc/asound/card*/id
```

Example result:

```text
/proc/asound/card2/id:ICUSBAUDIO7D
```

In this example:

```text
CARD=2
```

The card can also be detected automatically:

```bash
CARD=$(grep -l '^ICUSBAUDIO7D$' /proc/asound/card*/id | sed -E 's#.*card([0-9]+)/id#\1#')
```

Verify the detected card:

```bash
echo "$CARD"
```

---

## List Available Mixer Controls

```bash
amixer -c "$CARD" scontrols
```

For full mixer information:

```bash
amixer -c "$CARD"
```

---

# Line In Volume

Set the Line In capture level:

```bash
amixer -c "$CARD" sset Line 50% cap
```

Examples:

```bash
amixer -c "$CARD" sset Line 0% cap
amixer -c "$CARD" sset Line 25% cap
amixer -c "$CARD" sset Line 50% cap
amixer -c "$CARD" sset Line 80% cap
```

The CM6206 web interface treats an 80% hardware Line In level as 100% UI volume.

For consistency with the web interface, 80% should therefore normally be treated as the maximum Line In level.

---

# Microphone Volume

Set the microphone capture level:

```bash
amixer -c "$CARD" sset Mic 50% cap
```

Examples:

```bash
amixer -c "$CARD" sset Mic 0% cap
amixer -c "$CARD" sset Mic 25% cap
amixer -c "$CARD" sset Mic 50% cap
amixer -c "$CARD" sset Mic 75% cap
amixer -c "$CARD" sset Mic 100% cap
```

---

# Relative Volume Adjustment

ALSA can also make relative volume changes.

## Microphone Volume Up

```bash
amixer -c "$CARD" sset Mic 5%+
```

## Microphone Volume Down

```bash
amixer -c "$CARD" sset Mic 5%-
```

## Line In Volume Up

```bash
amixer -c "$CARD" sset Line 5%+
```

## Line In Volume Down

```bash
amixer -c "$CARD" sset Line 5%-
```

If relative controls are used for Line In, the controlling script should enforce the project's 80% maximum hardware level.

---

# Reapply the Complete Configuration

The complete CM6206 startup configuration can be reapplied manually:

```bash
sudo /usr/local/sbin/cm6206-setup.sh
```

Alternatively, restart the systemd service:

```bash
sudo systemctl restart cm6206-setup.service
```

Check its status:

```bash
systemctl status cm6206-setup.service
```

View its logs:

```bash
journalctl -u cm6206-setup.service
```

Follow the logs live:

```bash
journalctl -fu cm6206-setup.service
```

---

# Direct CM6206 Register Control

The higher-level `cm6206-mode` command should normally be used instead of directly manipulating CM6206 registers.

Direct register control is available for diagnostics, development and custom integrations.

## PCM Mode

The current PCM configuration uses:

```bash
sudo /usr/local/bin/cm6206ctl -r 1 -m 0x0007 -w 0x0001
sudo /usr/local/bin/cm6206ctl -r 5 -m 0x0800 -w 0x0800
```

The mixer capture source is then configured using ALSA:

```bash
amixer -c "$CARD" sset 'PCM Capture Source' 'Mixer'
```

For normal operation, prefer:

```bash
sudo /usr/local/sbin/cm6206-mode pcm
```

---

## Encoded Mode

The current encoded configuration uses:

```bash
sudo /usr/local/bin/cm6206ctl -r 5 -m 0x0800 -w 0x0000
sudo /usr/local/bin/cm6206ctl -r 1 -m 0x0007 -w 0x0004
```

For normal operation, prefer:

```bash
sudo /usr/local/sbin/cm6206-mode encoded
```

Direct register operations should be considered implementation details.

Using `cm6206-mode` provides a consistent interface if the underlying CM6206 register sequence changes in a future release.

---

# Running Without Flask

If only command-line or GPIO control is required, the Flask/Gunicorn web service can be disabled completely.

```bash
sudo systemctl disable --now cm6206-web.service
```

The underlying CM6206 setup service remains available:

```bash
systemctl status cm6206-setup.service
```

PCM mode can still be selected with:

```bash
sudo /usr/local/sbin/cm6206-mode pcm
```

Encoded mode can still be selected with:

```bash
sudo /usr/local/sbin/cm6206-mode encoded
```

The web interface can be restored later:

```bash
sudo systemctl enable --now cm6206-web.service
```

---

# GPIO Integration

Because mode control is exposed through simple local commands, physical buttons or switches can control the CM6206 without running Flask.

A GPIO application only needs to execute either:

```bash
sudo /usr/local/sbin/cm6206-mode pcm
```

or:

```bash
sudo /usr/local/sbin/cm6206-mode encoded
```

---

# Recommended GPIO Button Layout

A simple two-button arrangement could use:

| GPIO | Function |
|---|---|
| GPIO 17 | PCM mode |
| GPIO 27 | Encoded/Dolby mode |
| GND | Common button ground |

Each button connects its GPIO input to ground when pressed.

The Raspberry Pi's internal pull-up resistors can be used so external pull-up resistors are normally unnecessary.

> Important: Raspberry Pi GPIO uses 3.3 V logic. Do not apply 5 V directly to a GPIO pin.

---

# GPIO Mode Control with Python

The following example uses `gpiozero`.

Install it with:

```bash
sudo apt install python3-gpiozero
```

Create a GPIO controller:

```python
#!/usr/bin/env python3

from gpiozero import Button
from signal import pause
import subprocess

pcm = Button(17, pull_up=True, bounce_time=0.15)
encoded = Button(27, pull_up=True, bounce_time=0.15)


def set_pcm():
    subprocess.run(
        [
            "/usr/bin/sudo",
            "/usr/local/sbin/cm6206-mode",
            "pcm"
        ],
        check=True,
    )


def set_encoded():
    subprocess.run(
        [
            "/usr/bin/sudo",
            "/usr/local/sbin/cm6206-mode",
            "encoded"
        ],
        check=True,
    )


pcm.when_pressed = set_pcm
encoded.when_pressed = set_encoded

pause()
```

This provides two physical buttons:

- GPIO 17 selects PCM mode
- GPIO 27 selects encoded mode

---

# GPIO Toggle Switch

A physical toggle switch can instead represent the selected operating mode.

For example:

```text
Switch Open   -> PCM
Switch Closed -> Encoded
```

Using GPIO 17:

```python
#!/usr/bin/env python3

from gpiozero import Button
from signal import pause
import subprocess

mode = Button(17, pull_up=True, bounce_time=0.15)


def set_pcm():
    subprocess.run(
        [
            "/usr/bin/sudo",
            "/usr/local/sbin/cm6206-mode",
            "pcm"
        ],
        check=True,
    )


def set_encoded():
    subprocess.run(
        [
            "/usr/bin/sudo",
            "/usr/local/sbin/cm6206-mode",
            "encoded"
        ],
        check=True,
    )


mode.when_released = set_pcm
mode.when_pressed = set_encoded

# Apply the physical switch position when the service starts.
if mode.is_pressed:
    set_encoded()
else:
    set_pcm()

pause()
```

This approach is useful for a standalone appliance because the physical switch indicates the intended operating mode even after a reboot.

---

# GPIO Volume Buttons

Physical buttons can also control ALSA volume levels.

One possible layout is:

| GPIO | Function |
|---|---|
| GPIO 5 | Microphone volume up |
| GPIO 6 | Microphone volume down |
| GPIO 22 | Line In volume up |
| GPIO 23 | Line In volume down |

The GPIO controller can execute the same ALSA commands used manually.

## Microphone Up

```bash
amixer -c "$CARD" sset Mic 5%+
```

## Microphone Down

```bash
amixer -c "$CARD" sset Mic 5%-
```

## Line In Up

```bash
amixer -c "$CARD" sset Line 5%+
```

## Line In Down

```bash
amixer -c "$CARD" sset Line 5%-
```

A GPIO implementation should enforce the project's 80% Line In limit rather than allowing repeated volume-up operations to increase the control to 100%.

---

# GPIO Permissions

A GPIO service should run as a dedicated non-root user where practical.

For example:

```text
cm6206-gpio
```

If the GPIO controller needs to execute `cm6206-mode` through `sudo`, only the required commands should be permitted.

Example `/etc/sudoers.d/cm6206-gpio`:

```sudoers
cm6206-gpio ALL=(root) NOPASSWD: /usr/local/sbin/cm6206-mode pcm
cm6206-gpio ALL=(root) NOPASSWD: /usr/local/sbin/cm6206-mode encoded
```

Validate the sudoers file:

```bash
sudo visudo -cf /etc/sudoers.d/cm6206-gpio
```

Do not grant unrestricted passwordless sudo to the GPIO service.

---

# Running GPIO Control Automatically

A GPIO controller can run as a systemd service independently of Flask.

Example:

```ini
[Unit]
Description=CM6206 GPIO Controller
Requires=cm6206-setup.service
After=cm6206-setup.service

[Service]
Type=simple
User=cm6206-gpio
Group=audio
ExecStart=/usr/bin/python3 /opt/cm6206-gpio/gpio-control.py
Restart=on-failure
RestartSec=1

[Install]
WantedBy=multi-user.target
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable and start the GPIO controller:

```bash
sudo systemctl enable --now cm6206-gpio.service
```

Check its status:

```bash
systemctl status cm6206-gpio.service
```

View its logs:

```bash
journalctl -u cm6206-gpio.service
```

Follow the logs:

```bash
journalctl -fu cm6206-gpio.service
```

---

# Useful Diagnostics

## USB Devices

```bash
lsusb
```

## ALSA Playback Devices

```bash
aplay -l
```

## ALSA Capture Devices

```bash
arecord -l
```

## Find the CM6206 ALSA Card

```bash
grep -H ICUSBAUDIO7D /proc/asound/card*/id
```

## Display Mixer Controls

```bash
amixer -c "$CARD" scontrols
```

## Display Full Mixer State

```bash
amixer -c "$CARD"
```

## Current CM6206 Mode

```bash
cat /run/cm6206-mode
```

## CM6206 Setup Service

```bash
systemctl status cm6206-setup.service
```

## CM6206 Reconnect Service

```bash
systemctl status cm6206-reconnect.service
```

## Recent CM6206 Logs

```bash
journalctl \
    -u cm6206-setup.service \
    -u cm6206-reconnect.service \
    -n 100 \
    --no-pager
```

---

# Local Control Architecture

The recommended integration model is for external systems to use the project's high-level commands rather than implementing CM6206 register manipulation independently.

```text
Web UI
GPIO
Shell
Home Assistant
Node-RED
Other Automation
        |
        v
  cm6206-mode
     /     \
    /       \
  pcm     encoded
    \       /
     \     /
  ALSA + cm6206ctl
        |
        v
      CM6206
```

This keeps the Flask web interface optional while providing a common CM6206 control layer for every integration method.