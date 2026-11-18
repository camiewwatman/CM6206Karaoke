# CM6206 based USB 5.1 Audio Sound Card + Raspberry Pi Karaoke Mixer


[![License: GPL v3+](https://img.shields.io/badge/License-GPLv3%2B-blue.svg)](LICENSE)

This project outlines the process I went through (with assistance from Microsoft CoPilot) to develop a Karaoke Box using a cheap $30 [CM6206 TOSLINK/SPDIF Sound Card](https://www.amazon.com.au/Sound-Card-Channel-Output-Adapter/dp/B0CGX1WDFW) from Amazon and a Raspberry Pi to build a full Karaoke Mixer. This utilises modularised CM6206 audio routing and a Flask control panel.

## Installation

Clone the repository:

```bash
git clone https://github.com/camiewwatman/CM6206Karaoke.git
```

Enter the project directory:

```bash
cd CM6206Karaoke
```

Then choose one of the following installation methods.

### Standard Installation

Installs the CM6206 controller without making Raspberry Pi startup optimisations:

```bash
sudo ./install.sh
```

### Optimised Installation

Installs the CM6206 controller and applies the optional Raspberry Pi appliance startup optimisations:

```bash
sudo ./install-optimised.sh
```

> The optimised installer is intended for a dedicated, headless Raspberry Pi. See [`Docs/Optimisation.md`](docs/optimisation.md) for the changes and trade-offs before using it.

## How It Works
This project is built around a CM6206-based USB S/PDIF sound card.
![Photograph of the CM6206 Kareoke Box showing TOSLINK Input/Output and TRS Link](docs/photos/photo1.jpg)

The hardware has an important limitation: the audio interface normally allows only one input source to be selected at a time, such as:

- Line In
- Microphone In
- S/PDIF In

That makes it difficult to mix audio arriving over S/PDIF with a microphone signal.

### The Workaround

To get around this limitation, the project uses the CM6206's HID controls to change how audio is routed internally. If you want more info on this, visit the [Audio Routing](docs/audio-routing.md) page.

The incoming stereo S/PDIF signal is routed to the card's 5.1 analogue outputs, including the Front, Rear and Centre/Bass outputs. The Front stereo output is then physically looped back into the Line In using a short 3.5 mm TRS cable.

This creates the following signal path:
`S/PDIF In → Front Out → TRS Loopback Cable → Line In → Internal Mixer → S/PDIF Out`

Because the CM6206 can internally mix Line In and Microphone In, the looped-back S/PDIF audio can now be combined with the microphone.

The Raspberry Pi controls the Line In and microphone levels using ALSA commands, either directly from the command line or through the Flask web interface.

The resulting mixed PCM audio is then sent through S/PDIF Out to a soundbar, AV receiver or speaker system.

### Microphone Connection

The sound card has a 3.5 mm microphone input. My microphone uses a 6.35 mm connector, so I used a simple 6.35 mm-to-3.5 mm adapter.

The microphone used during development has a very low output level, so the project currently defaults the microphone input to **100%**.

> **Warning:** 100% microphone gain may be extremely loud with more sensitive microphones. When connecting a microphone for the first time, mute the downstream speakers or microphone where possible and have the Flask volume controls ready. Start at a low listening volume and increase it gradually.

## Hardware Warnings
Although these audio interfaces list 5.1 is supported, 5.1 Dolby/ACS Encrypted Audio will not work with this solution as it cannot be decrypted and mixed. The Web Interface running on port 80 of the system allows the user to switch between Dolby Bypass (no Microphone Mix) and PCM + Microphone Mode.

## Local Control and GPIO
If you don't want to use the Flask Server to control Levels and the SPDIF Bypass for 5.1 Encrypted Audio, visit the [Local Control](docs/local-control.md) page for details on the commands you can run from the Terminal to control all aspects, as well as guidance on connecting this to GPIO Controls.

## Startup Optimisation Script
Original build was on a Raspberry Pi 3B, but this should work on any Ubuntu System. 
The [Startup Optimiser Script](docs/optimisation.md) is built solely with *Raspberry Pi OS Lite* in mind - utilisation of Boot Optimiser script is with full discretion of the user and is recommended only if the Raspberry Pi system is dedicated to this project. Impacted system services may be impacted by this change.

## Testing
Testing has currently been completed on a Raspberry Pi 3 Model B, covering installation, PCM/encoded mode switching, microphone mixing, web control, USB reconnect handling, and startup optimisation. See the [Testing](Docs/Testing.md) page for the full test matrix, results, and platforms still requiring validation.

## Local Files and Permissions
The installers copy version-controlled files into `/usr/local`, `/etc/systemd/system`, `/etc/udev/rules.d`, `/etc/sudoers.d`, and `/opt/cm6206-web`.
The web service intentionally has `NoNewPrivileges=no` and no restrictive `CapabilityBoundingSet`, allowing its tightly scoped `sudo` rules to invoke only `cm6206-mode pcm` and `cm6206-mode encoded`. Gunicorn itself still runs as `cm6206-web`.

## Licensing
The original code in this repository is released under **GPL-3.0-or-later**. See `LICENSE` and `THIRD_PARTY_NOTICES.md`. Third-party components retain their own licences.
