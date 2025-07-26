# Gmail Automation with Appium

Automated Gmail sign-in testing for Android devices using Python and Appium.

## What it does

- Launches Gmail app on Android device/emulator
- Automates sign-in flow with configurable credentials
- Includes human-like delays and natural gestures
- Generates detailed test reports with pytest-html

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Appium 2.x:
```bash
npm install -g appium@2
appium driver install uiautomator2
```

3. Connect Android device or start emulator:
```bash
adb devices  # Should show your device
```

4. Update `config.json` with your device details and credentials

## Usage

```bash
# Test Gmail app launch only
python gmail_automation.py --launch-only

# Run full automation (including sign-in)
python gmail_automation.py

# Run tests with HTML reports
python run_tests.py --quick
```

## Testing

Run tests with HTML reports:

```bash
# Quick tests (fast)
python run_tests.py --quick

# All tests (includes full automation)
python run_tests.py --all

# Gmail launch tests only
python run_tests.py --launch-only
```

Test reports are saved in `reports/` folder.

## Configuration

Edit `config.json` to update:
- Email/password credentials
- Device settings (for emulator vs physical device)
- Timing delays

## Troubleshooting

**Device not found:**
```bash
adb devices
adb kill-server && adb start-server
```

**Appium issues:**
- Make sure Appium server is running: `appium --port 4723`
- Check device capabilities in `config.json`

**Gmail login blocked:**
- This is normal - Google blocks automated logins
- The script still tests the automation flow successfully

## Notes

- Uses test credentials only (stored in plain text)
- Works with Android 12+ devices and emulators
- Includes human-like delays to mimic real usage
- Educational/testing purposes only
