# Third-Party Notices

This project installs, invokes, or depends on third-party software. Those components are not relicensed by this repository and remain subject to their respective licences.

## cm6206ctl

- Source: https://github.com/vestom/cm6206ctl
- Upstream licence: GPL-2.0-or-later (GPL-2.0+)
- The installer downloads and builds cm6206ctl as a separate executable. Its upstream copyright and licence remain applicable.

## HIDAPI

- Source: https://github.com/libusb/hidapi
- HIDAPI is separately licensed by its upstream project. It is used by the separately-built cm6206ctl executable through the system HIDAPI package.

## Flask

- Source: https://github.com/pallets/flask
- Licence: BSD-3-Clause
- Installed separately with pip.

## Gunicorn

- Source: https://github.com/benoitc/gunicorn
- Licence: MIT
- Installed separately with pip.

## Distribution packages

The installation scripts may install packages including ALSA utilities, SoX, Git, GCC, sudo, usbutils, Python and HIDAPI from the host Linux distribution. Each remains subject to its own upstream and distribution licensing terms.
