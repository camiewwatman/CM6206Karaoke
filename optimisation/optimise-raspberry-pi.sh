#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later
set -euo pipefail
[[ $(id -u) -eq 0 ]] || { echo 'Run with sudo' >&2; exit 1; }
systemctl disable --now NetworkManager-wait-online.service 2>/dev/null || true
systemctl mask NetworkManager-wait-online.service 2>/dev/null || true
systemctl disable --now apt-daily-upgrade.timer apt-daily.timer 2>/dev/null || true
systemctl mask rpi-resize-swap-file.service 2>/dev/null || true
apt-get purge -y cloud-init rpi-cloud-init-mods 2>/dev/null || true
rm -rf /etc/cloud /var/lib/cloud
systemctl set-default multi-user.target
systemctl daemon-reload
