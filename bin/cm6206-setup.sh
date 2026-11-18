#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later
set -euo pipefail
CTL=/usr/local/bin/cm6206ctl
log(){ echo "$*"; logger -t cm6206-setup "$*"; }
log "Starting CM6206 configuration"
CARD=""
for attempt in $(seq 1 30); do
  for path in /proc/asound/card*/id; do
    [[ -r "$path" && "$(<"$path")" == ICUSBAUDIO7D ]] || continue
    CARD="${path#/proc/asound/card}"; CARD="${CARD%/id}"; break 2
  done
  sleep 0.1
done
[[ -n "$CARD" ]] || { log "ERROR: ICUSBAUDIO7D ALSA card not found"; exit 1; }
for attempt in $(seq 1 15); do amixer -c "$CARD" scontrols >/dev/null 2>&1 && break; sleep 0.1; done
amixer -c "$CARD" sset 'PCM Capture Source' 'Mixer'
amixer -c "$CARD" sset 'Line' 80% cap unmute || true
amixer -c "$CARD" sset 'Line' 80% unmute || true
amixer -c "$CARD" sset 'Mic' 100% cap unmute || true
amixer -c "$CARD" sset 'Mic' 100% unmute || true
"$CTL" -r 1 -m 0x0007 -w 0x0001
"$CTL" -r 5 -m 0x0800 -w 0x0800
printf 'pcm\n' >/run/cm6206-mode
log "CM6206 configuration complete"
