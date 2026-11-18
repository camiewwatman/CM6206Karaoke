#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later
set -euo pipefail
[[ $(id -u) -eq 0 ]] || { echo "Run with sudo: sudo $0" >&2; exit 1; }
ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
put(){ install -D -m "$1" "$ROOT/$2" "$3"; }
apt-get update
apt-get install -y git build-essential libhidapi-dev libhidapi-libusb0 alsa-utils usbutils vim-common sox python3-venv sudo
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
git clone --depth 1 https://github.com/vestom/cm6206ctl.git "$tmp/cm6206ctl"
gcc "$tmp/cm6206ctl/cm6206ctl.c" -l hidapi-libusb -o "$tmp/cm6206ctl-bin"
install -m 755 "$tmp/cm6206ctl-bin" /usr/local/bin/cm6206ctl
put 755 bin/cm6206-setup.sh /usr/local/sbin/cm6206-setup.sh
put 755 bin/cm6206-mode /usr/local/sbin/cm6206-mode
put 644 systemd/cm6206-setup.service /etc/systemd/system/cm6206-setup.service
put 644 systemd/cm6206-reconnect.service /etc/systemd/system/cm6206-reconnect.service
put 644 systemd/cm6206-web.service /etc/systemd/system/cm6206-web.service
put 644 udev/99-cm6206.rules /etc/udev/rules.d/99-cm6206.rules
put 440 sudoers/cm6206-web /etc/sudoers.d/cm6206-web
visudo -cf /etc/sudoers.d/cm6206-web
id cm6206-web >/dev/null 2>&1 || useradd --system --home /opt/cm6206-web --shell /usr/sbin/nologin --user-group cm6206-web
usermod -a -G audio cm6206-web
install -d -o cm6206-web -g cm6206-web -m 755 /opt/cm6206-web
put 644 web/app.py /opt/cm6206-web/app.py
python3 -m venv /opt/cm6206-web/venv
/opt/cm6206-web/venv/bin/pip install --upgrade pip
/opt/cm6206-web/venv/bin/pip install flask gunicorn
chown -R cm6206-web:cm6206-web /opt/cm6206-web
systemctl daemon-reload
udevadm control --reload-rules
systemctl enable cm6206-setup.service cm6206-web.service
systemctl restart cm6206-setup.service cm6206-web.service
bash "$ROOT/optimisation/optimise-raspberry-pi.sh"
systemctl show cm6206-web.service -p User -p Group -p NoNewPrivileges
sudo -u cm6206-web sudo -n /usr/local/sbin/cm6206-mode pcm
echo 'Installed. Open http://<raspberry-pi-ip>/'
