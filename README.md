# Gmail Automation with Appium

A Python automation script that uses Appium to automate Gmail sign-in flow on physical Android devices.

## Features

✅ **Automated Gmail Sign-in Flow**
- Launch Gmail app using package name
- Handle sign-in/add account flow
- Enter email and password credentials
- Navigate through login screens
- Wait for completion confirmation

💡 **Human-Like Behavior**
- Randomized wait times between actions (1.2s to 3.5s)
- Natural tap gestures with slight randomization
- Human-like typing with character delays
- Detailed logging with timestamps

📦 **Modular Code Structure**
- Separate functions for each automation step
- Configuration-driven approach with `config.json`
- Comprehensive error handling and logging
- Works with real Android devices via USB

## Prerequisites

### 1. Android Device Setup
- Android 12+ device connected via USB
- USB Debugging enabled in Developer Options
- Gmail app installed on the device

### 2. Development Environment
- Python 3.7+
- Node.js and npm (for Appium)
- Android SDK and ADB tools
- Java JDK 8+

### 3. Appium Server
Install Appium globally:
```bash
npm install -g appium
npm install -g @appium/driver-uiautomator2
```

## Installation

1. **Clone and setup the project:**
```bash
cd /Users/eliyahasan/TestSquadPoC/python-appium-demo
pip install -r requirements.txt
```

2. **Verify device connection:**
```bash
adb devices
```

3. **Start Appium server:**
```bash
appium --port 4723
```

## Configuration

Edit `config.json` to customize:

- **Credentials**: Update email/password
- **Delays**: Adjust timing for human-like behavior
- **Device**: Modify device capabilities if needed
- **Logging**: Change log level and format

## Usage

### Basic Usage
```bash
python gmail_automation.py
```

### Advanced Usage
```python
from gmail_automation import GmailAutomation

# Initialize with custom config
automation = GmailAutomation("custom_config.json")

# Run complete flow
success = automation.run_automation()

# Or run individual steps
automation.connect_device()
automation.launch_app()
automation.handle_sign_in_flow()
automation.enter_email()
automation.enter_password()
automation.wait_for_login_completion()
automation.cleanup()
```

## Script Flow

1. **Device Connection**: Connect to Android device via Appium
2. **App Launch**: Launch Gmail using package name `com.google.android.gm`
3. **Sign-in Detection**: Look for "Sign in" or "Add account" buttons
4. **Email Input**: Enter email address with human-like typing
5. **Navigation**: Tap "Next" and wait for password screen
6. **Password Input**: Enter password with delays
7. **Completion**: Wait for inbox or handle security blocks

## Logging

The script generates detailed logs with:
- Timestamp for each action
- Duration measurements
- Element detection details
- Error handling information

Log files are saved as: `gmail_automation_YYYYMMDD_HHMMSS.log`

## Troubleshooting

### Common Issues

**Device not detected:**
```bash
adb devices
adb kill-server
adb start-server
```

**Appium connection failed:**
- Ensure Appium server is running on port 4723
- Check device capabilities in config.json
- Verify Android SDK path

**Element not found:**
- Gmail UI may vary by version
- Check device screen resolution
- Update element selectors if needed

**Login blocked by Google:**
- This is expected behavior for security
- Script logs this as successful flow execution
- Focus is on automation flow, not bypassing security

### Debug Mode

Enable verbose logging in `config.json`:
```json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

## Security Notes

🛡️ **Important Security Considerations:**
- Credentials are stored in plain text in config.json
- Use test accounts only for automation
- Google may block login attempts from automation tools
- This is a PoC - not for production use

## License

This project is for educational and testing purposes only.
