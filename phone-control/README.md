# 📱 Phone Control Skill for OpenClaw

Complete phone control using OpenClaw nodes API - camera, calls, SMS, location, and more.

## Quick Start

```bash
# Take photo (front camera)
nodes action=camera_snap facing=front

# Get location
nodes action=location_get

# Send notification
nodes action=notify title="标题" body="内容"
```

## Features

- 📷 Camera control (photo/video)
- 📍 GPS location tracking
- 🔔 Notifications
- 🎤 Audio recording
- 📺 Screen recording
- ⚙️ System commands

## Installation

This is an OpenClaw skill. Install via ClawHub:

```bash
npx clawhub install phone-control
```

## Documentation

See [SKILL.md](SKILL.md) for complete usage guide.

## License

MIT

## Author

弹弓哥
