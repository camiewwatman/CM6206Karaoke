# CM6206 Raspberry Pi controller

[![License: GPL v3+](https://img.shields.io/badge/License-GPLv3%2B-blue.svg)](LICENSE)

Modularised CM6206 audio routing and Flask control panel.

- `sudo ./install.sh`: standard installation, no startup optimisation.
- `sudo ./install-optimised.sh`: installation plus appliance boot optimisation.

The installers copy version-controlled files into `/usr/local`, `/etc/systemd/system`, `/etc/udev/rules.d`, `/etc/sudoers.d`, and `/opt/cm6206-web`.

## Licensing

The original code in this repository is released under **GPL-3.0-or-later**. See `LICENSE` and `THIRD_PARTY_NOTICES.md`. Third-party components retain their own licences.

The web service intentionally has `NoNewPrivileges=no` and no restrictive `CapabilityBoundingSet`, allowing its tightly scoped `sudo` rules to invoke only `cm6206-mode pcm` and `cm6206-mode encoded`. Gunicorn itself still runs as `cm6206-web`.
