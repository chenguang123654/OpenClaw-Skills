---
name: phone-control
description: Complete phone control via OpenClaw nodes - camera, call, SMS, location, audio, and more. Uses nodes tool for remote device management.
version: 1.0.0
author: 弹弓哥
tags: [android, phone, camera, termux, mobile, control]
---

# 📱 Phone Control Skill

Complete phone control using OpenClaw nodes API.

## Features

- 📷 **Camera** - Take photos, record video, live snapshot
- 📞 **Calls** - Make phone calls, check status
- 💬 **SMS** - Send and receive messages
- 📍 **Location** - GPS coordinates tracking
- 🎤 **Audio** - Record audio, microphone control
- 📺 **Screen** - Screen recording
- 🔔 **Notifications** - Send notifications
- 📋 **Contacts** - Read contacts
- ⚙️ **System** - Run commands, check device info

## Usage

### Camera

```bash
# Take photo (front camera)
nodes action=camera_snap facing=front

# Take photo (back camera)
nodes action=camera_snap facing=back

# Record video (30 seconds)
nodes action=camera_clip duration=30s facing=back

# Live snapshot
nodes action=camera_snap maxWidth=1920 quality=80
```

### Phone Calls

```bash
# Make call
nodes action=run command=["tel:", "1234567890"]

# Get device status
nodes action=status
```

### SMS

```bash
# Send SMS via termux API
nodes action=run command=["termux-sms-send", "-n", "1234567890", "Hello!"]
```

### Location

```bash
# Get current location
nodes action=location_get

# Track location
nodes action=location_get desiredAccuracy=precise locationTimeoutMs=30000
```

### Audio Recording

```bash
# Record audio
nodes action=run command=["termux-microphone-recording", "--start"]

# Stop recording
nodes action=run command=["termux-microphone-recording", "--stop"]
```

### Screen Recording

```bash
# Start screen recording
nodes action=screen_record duration=60s fps=30

# Stop recording
nodes action=run command=["termux-screenrecord", "--stop"]
```

### Notifications

```bash
# Send notification
nodes action=notify title="提醒" body="测试消息" priority=active

# With sound
nodes action=notify title="警告" body="电量低" sound=default
```

### Contacts

```bash
# Read contacts
nodes action=run command=["termux-contact-list"]
```

### System Commands

```bash
# Run any termux command
nodes action=run command=["termux-battery-status"]
nodes action=run command=["termux-wifi-connectioninfo"]
nodes action=run command=["uptime"]
```

## Requirements

- OpenClaw with nodes tool enabled
- Termux app installed on Android
- Termux API installed (termux-api package)

## Setup

1. Install Termux from F-Droid or Play Store
2. Install termux-api: `pkg install termux-api`
3. Configure OpenClaw nodes pairing
4. Grant necessary permissions on Android device

## Examples

### Monitor Mode

```bash
# Front camera snapshot every 5 minutes
while true; do
  nodes action=camera_snap facing=front maxWidth=1280 quality=70 outPath="/sdcard/snapshot_$(date +%s).jpg"
  sleep 300
done
```

### Location Tracking

```bash
# Track location every minute
while true; do
  nodes action=location_get desiredAccuracy=balanced > location_$(date +%Y%m%d_%H%M%S).json
  sleep 60
done
```

## Notes

- Camera quality affects file size (70-80% recommended)
- Videos create large files, use appropriate duration
- Location tracking drains battery
- Some features require Android permissions

## Author

**弹弓哥** - OpenClaw user

---

MIT License
