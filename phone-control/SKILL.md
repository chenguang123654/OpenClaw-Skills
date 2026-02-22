---
name: phone-control
description: Complete phone control via OpenClaw nodes - camera, call, SMS, location, audio, notifications, and more. Uses nodes tool for remote device management.
version: 1.1.0
author: 弹弓哥
tags: [android, phone, camera, termux, mobile, control, surveillance, monitoring]
---

# 📱 Phone Control Skill for OpenClaw

Complete phone control using OpenClaw nodes API - camera, calls, SMS, location, audio, and more. Perfect for surveillance, monitoring, and automation.

## 🎯 Use Cases

- 🏠 **Home Surveillance** - Monitor your home with front camera
- 📍 **Location Tracking** - Track device location in real-time
- 🔔 **Smart Alerts** - Get notifications for important events
- 🎥 **Remote Recording** - Record audio/video remotely
- 📊 **System Monitoring** - Monitor battery, wifi, and system status

## ⚡ Quick Start

```bash
# Take photo (front camera - good for surveillance)
nodes action=camera_snap facing=front outPath="/sdcard/snapshot.jpg"

# Get current location
nodes action=location_get

# Send notification
nodes action=notify title="提醒" body="监控触发" priority=active

# Check device status
nodes action=status
```

---

## 📷 Camera Control

### Take Photo

```bash
# Front camera (for surveillance)
nodes action=camera_snap facing=front maxWidth=1920 quality=75

# Back camera (high quality)
nodes action=camera_snap facing=back maxWidth=2560 quality=80

# Both cameras
nodes action=camera_snap facing=both

# With custom output path
nodes action=camera_snap facing=front outPath="/sdcard/surveillance_$(date +%Y%m%d_%H%M%S).jpg"
```

**Parameters:**
- `facing`: front, back, or both
- `maxWidth`: 640-4096 (default: 1920)
- `quality`: 10-100 (default: 80)
- `outPath`: output file path
- `delayMs`: delay before capture (1-5000ms)

### Record Video

```bash
# Record 30 seconds (back camera)
nodes action=camera_clip duration=30s facing=back fps=30

# Record 60 seconds (front camera)
nodes action=camera_clip duration=60s facing=front fps=24

# Record with max size limit
nodes action=camera_clip duration=60s maxSizeMb=100
```

**Parameters:**
- `duration`: 1-600 seconds
- `facing`: front or back
- `fps`: 15-60 (default: 30)
- `maxSizeMb`: size limit in MB
- `includeAudio`: true/false (default: true)

---

## 📍 Location Tracking

### Get Location

```bash
# Basic location
nodes action=location_get

# High accuracy (GPS)
nodes action=location_get desiredAccuracy=precise locationTimeoutMs=30000

# Fast response (network)
nodes action=location_get desiredAccuracy=coarse locationTimeoutMs=10000

# Balanced accuracy + battery
nodes action=location_get desiredAccuracy=balanced locationTimeoutMs=15000
```

**Output Example:**
```json
{
  "latitude": 31.234567,
  "longitude": 121.345678,
  "accuracy": 10,
  "timestamp": "2026-02-22T13:00:00Z"
}
```

### Continuous Tracking

```bash
# Track location every minute (bash loop)
while true; do
  nodes action=location_get desiredAccuracy=balanced > "/sdcard/location_$(date +%Y%m%d_%H%M%S).json"
  sleep 60
done
```

---

## 🔔 Notifications

### Send Notification

```bash
# Basic notification
nodes action=notify title="标题" body="内容"

# High priority (shows immediately)
nodes action=notify title="警告" body="电量低" priority=timeSensitive

# With sound
nodes action=notify title="提醒" body="有人入侵" sound=default priority=active

# Silent notification
nodes action=notify title="状态" body="运行正常" priority=passive
```

**Priority Levels:**
- `passive` - No interruption
- `active` - Shows in notification center
- `timeSensitive` - High priority, shows immediately

---

## 🎤 Audio Recording

### Microphone Recording

```bash
# Start recording
nodes action=run command=["termux-microphone-recording", "--start", "--file", "/sdcard/audio_$(date +%Y%m%d_%H%M%S).mp3"]

# Check recording status
nodes action=run command=["termux-microphone-recording", "--status"]

# Stop recording
nodes action=run command=["termux-microphone-recording", "--stop"]
```

### Record Short Clip

```bash
# Record 10 second clip
nodes action=run command=["termux-recorder", "-d", "10", "/sdcard/voice_$(date +%Y%m%d_%H%M%S).3gp"]
```

---

## 📺 Screen Recording

### Record Screen

```bash
# Record 60 seconds (30 FPS)
nodes action=screen_record duration=60s fps=30

# Record 5 minutes (lower FPS for smaller size)
nodes action=screen_record duration=300s fps=24

# Record with bitrate
nodes action=screen_record duration=60s bitrate=8000000

# Stop recording
nodes action=run command=["termux-screenrecord", "--stop"]
```

**Parameters:**
- `duration`: 1-1800 seconds
- `fps`: 15-60
- `bitrate`: 1-20000000 (bps)
- `size`: widthxheight (e.g., 1080x1920)

---

## 📞 Phone Calls

### Check Call Status

```bash
# Check if device is in call
nodes action=run command=["termux-telephony-call", "--status"]
```

---

## 💬 SMS

### Send SMS

```bash
# Send SMS to number
nodes action=run command=["termux-sms-send", "-n", "1234567890", "-s", "500", "Hello, this is a test message"]

# Send to multiple recipients
nodes action=run command=["termux-sms-send", "-n", "1234567890;9876543210", "Message content"]
```

---

## 📋 Contacts

### Read Contacts

```bash
# List all contacts
nodes action=run command=["termux-contact-list"]

# Output as JSON
nodes action=run command=["termux-contact-list", "--json"]
```

---

## ⚙️ System Commands

### Battery Status

```bash
nodes action=run command=["termux-battery-status"]
```

**Output:**
```json
{
  "level": 85,
  "percentage": 85,
  "status": "CHARGING",
  "health": "GOOD",
  "temperature": 28.5
}
```

### WiFi Connection

```bash
nodes action=run command=["termux-wifi-connectioninfo"]
```

### WiFi Scan

```bash
nodes action=run command=["termux-wifi-scaninfo"]
```

### Device Info

```bash
nodes action=run command=["termux-device-info"]
```

---

## 🔧 Advanced Examples

### Surveillance Mode (Front Camera Every 5 Minutes)

```bash
#!/bin/bash
# Save as: surveillance.sh

OUT_DIR="/sdcard/surveillance"
mkdir -p $OUT_DIR

while true; do
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  FILENAME="$OUT_DIR/snapshot_$TIMESTAMP.jpg"
  
  # Take photo
  nodes action=camera_snap facing=front maxWidth=1280 quality=70 outPath="$FILENAME"
  
  # Log
  echo "[$(date)] Captured: $FILENAME"
  
  # Wait 5 minutes
  sleep 300
done
```

### Motion Detection Alert

```bash
#!/bin/bash
# Save as: motion-alert.sh

# Capture baseline
nodes action=camera_snap facing=front outPath="/tmp/baseline.jpg"

# Monitor for changes (simplified - compare file sizes)
while true; do
  nodes action=camera_snap facing=front outPath="/tmp/current.jpg"
  
  SIZE_BEFORE=$(stat -f%z /tmp/baseline.jpg 2>/dev/null || stat -c%s /tmp/baseline.jpg 2>/dev/null)
  SIZE_AFTER=$(stat -f%z /tmp/current.jpg 2>/dev/null || stat -c%s /tmp/current.jpg 2>/dev/null)
  
  # If file size differs significantly (>10%)
  if [ $(echo "scale=2; ($SIZE_AFTER - $SIZE_BEFORE) / $SIZE_BEFORE * 100" | bc 2>/dev/null || echo "0") -gt 10 ]; then
    nodes action=notify title="⚠️  Motion Detected" body="有人移动！检查监控" priority=timeSensitive sound=default
    cp /tmp/current.jpg "/sdcard/motion_$(date +%Y%m%d_%H%M%S).jpg"
  fi
  
  mv /tmp/current.jpg /tmp/baseline.jpg
  sleep 10
done
```

### Location Tracker (Every Minute)

```bash
#!/bin/bash
# Save as: location-tracker.sh

LOG_FILE="/sdcard/location_tracking.csv"
echo "timestamp,latitude,longitude,accuracy" > $LOG_FILE

while true; do
  RESULT=$(nodes action=location_get desiredAccuracy=precise)
  
  TIMESTAMP=$(date -Iseconds)
  LAT=$(echo $RESULT | jq -r '.latitude')
  LON=$(echo $RESULT | jq -r '.longitude')
  ACC=$(echo $RESULT | jq -r '.accuracy')
  
  echo "$TIMESTAMP,$LAT,$LON,$ACC" >> $LOG_FILE
  echo "[$(date)] Location: $LAT, $LON (accuracy: ${ACC}m)"
  
  sleep 60
done
```

### System Health Monitor

```bash
#!/bin/bash
# Monitor battery and send alerts

BATTERY_WARN=20
BATTERY_CRITICAL=10

while true; do
  BATTERY=$(nodes action=run command=["termux-battery-status"] | jq '.percentage')
  
  if [ $BATTERY -le $BATTERY_CRITICAL ]; then
    nodes action=notify title="🔴 低电量警告" body="电量仅剩${BATTERY}%，请立即充电！" priority=timeSensitive sound=default
  elif [ $BATTERY -le $BATTERY_WARN ]; then
    nodes action=notify title="🟡 电量不足" body="电量仅剩${BATTERY}%" priority=active
  fi
  
  sleep 300  # Check every 5 minutes
done
```

---

## 📊 Parameters Reference

### Camera Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `facing` | string | front | front, back, or both |
| `maxWidth` | number | 1920 | Image width (640-4096) |
| `quality` | number | 80 | JPEG quality (10-100) |
| `outPath` | string | auto | Output file path |
| `delayMs` | number | 0 | Capture delay in ms |
| `fps` | number | 30 | Video frame rate |
| `duration` | number | 30 | Recording duration in seconds |
| `includeAudio` | boolean | true | Include audio in video |

### Location Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `desiredAccuracy` | string | balanced | coarse, balanced, or precise |
| `locationTimeoutMs` | number | 30000 | Timeout in milliseconds |

### Notification Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | required | Notification title |
| `body` | string | required | Notification body |
| `priority` | string | active | passive, active, timeSensitive |
| `sound` | string | - | Sound name (default, notification, etc.) |
| `delivery` | string | system | system, overlay, auto |

### Screen Recording Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `duration` | number | 60 | Recording duration (1-1800s) |
| `fps` | number | 30 | Frame rate (15-60) |
| `bitrate` | number | - | Video bitrate in bps |
| `size` | string | - | Video size (WxH) |

---

## 🔒 Security Notes

1. **Permission Required**: Grant camera, location, and storage permissions in Android settings
2. **Privacy**: Be aware of local laws regarding surveillance
3. **Storage**: Regularly clean up captured media to save space
4. **Battery**: Location tracking and camera use drain battery quickly
5. **Network**: Ensure secure connection for remote access

---

## 🛠️ Setup Instructions

### Prerequisites

1. **Termux** - Install from F-Droid (recommended over Play Store)
2. **Termux API** - Install in Termux: `pkg install termux-api`
3. **OpenClaw** - Configure nodes tool in OpenClaw
4. **Android Permissions** - Grant necessary permissions:
   - Camera
   - Location
   - Storage
   - Microphone (for audio recording)

### Installation

```bash
# Install termux-api
pkg update && pkg install termux-api

# Grant permissions (in Termux)
termux-setup-storage
termux-camera-permission

# Restart Termux
exit
```

### Pairing with OpenClaw

1. Open OpenClaw Gateway
2. Pair Android device as a node
3. Test connection:
   ```bash
   nodes action=status
   ```

---

## 🚨 Troubleshooting

### Camera Issues

```bash
# Check camera permission
nodes action=run command=["termux-camera-permission"]

# List available cameras
nodes action=run command=["termux-camera-list"]

# If camera not working, try:
termux-camera-permission
```

### Location Issues

```bash
# Check location permission
nodes action=run command=["termux-location-permission"]

# Enable GPS
nodes action=run command=["termux-location", "-r", "network"]
```

### Permission Denied

```bash
# Grant all permissions
termux-setup-storage
termux-camera-permission
termux-location-permission
termux-microphone-permission

# Restart termux
```

### Storage Issues

```bash
# Check available storage
nodes action=run command=["df", "-h", "/sdcard"]

# Clear cache
nodes action=run command=["rm", "-rf", "/data/data/com.termux/files/home/.cache"]
```

---

## 📝 Changelog

### v1.1.0 (2026-02-22)
- ✅ Added advanced examples (surveillance, motion detection, location tracking)
- ✅ Added troubleshooting section
- ✅ Added parameters reference table
- ✅ Added security notes
- ✅ Improved documentation structure

### v1.0.0 (2026-02-22)
- 🎉 Initial release
- ✅ Camera control (photo/video)
- ✅ Location tracking
- ✅ Notifications
- ✅ Audio recording
- ✅ Screen recording
- ✅ System commands

---

## 📦 Related Skills

- [agent-browser](https://clawhub.ai/skills/agent-browser) - Browser automation
- [server-health-agent](https://clawhub.ai/skills/server-health-agent) - Server monitoring

---

## 📄 License

MIT License

## 👨‍💻 Author

**弹弓哥** - OpenClaw enthusiast

---

## 🔗 Links

- **GitHub**: https://github.com/chenguang123654/skills/tree/master/phone-control
- **Report Issues**: https://github.com/chenguang123654/skills/issues
- **OpenClaw Docs**: https://docs.openclaw.ai/
