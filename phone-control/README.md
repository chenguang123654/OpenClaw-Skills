# 📱 Phone Control Skill for OpenClaw

Complete phone control using OpenClaw nodes API - camera, calls, SMS, location, and more. Perfect for surveillance, monitoring, and automation.

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
```

## 📦 Features

### 📷 Camera
- Take photos (front/back camera)
- Record video with configurable duration
- Adjustable quality and resolution

### 📍 Location
- GPS location tracking
- Configurable accuracy levels
- Continuous monitoring support

### 🔔 Notifications
- Send push notifications
- Priority levels (passive, active, timeSensitive)
- Custom sounds

### 🎤 Audio
- Microphone recording
- Configurable duration

### 📺 Screen Recording
- Record screen activity
- Adjustable FPS and duration
- Bitrate control

### ⚙️ System
- Battery status monitoring
- WiFi connection info
- Device information
- Contact list

## 🚀 Advanced Examples

### Surveillance Mode (5-minute intervals)
```bash
while true; do
  nodes action=camera_snap facing=front maxWidth=1280 quality=70 \
    outPath="/sdcard/snapshot_$(date +%Y%m%d_%H%M%S).jpg"
  sleep 300
done
```

### Location Tracker
```bash
while true; do
  nodes action=location_get desiredAccuracy=precise \
    > "/sdcard/location_$(date +%Y%m%d_%H%M%S).json"
  sleep 60
done
```

## 📖 Documentation

See [SKILL.md](SKILL.md) for complete usage guide including:
- All parameters reference
- Advanced automation examples
- Troubleshooting guide
- Security notes

## 🛠️ Setup

1. Install Termux from F-Droid
2. Run `pkg install termux-api`
3. Grant permissions (camera, location, storage)
4. Pair device with OpenClaw nodes

## 📝 Version History

- **v1.1.0** - Added advanced examples, troubleshooting, parameters reference
- **v1.0.0** - Initial release

## 📄 License

MIT

## 👨‍💻 Author

**弹弓哥** - OpenClaw enthusiast

---

## 🔗 Links

- **GitHub**: https://github.com/chenguang123654/skills/tree/master/phone-control
- **OpenClaw Docs**: https://docs.openclaw.ai/
