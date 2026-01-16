# hassio-bluetti-bt (Fork with AC2P Support)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Bluetti Integration for Home Assistant - **Fork with AC2P and encryption support**

> **Note**: This is a fork of [Patrick762/hassio-bluetti-bt](https://github.com/Patrick762/hassio-bluetti-bt) with modifications to support the Bluetti AC2P device.

## Why this fork?

The original integration was refactored to use an external library (`bluetti-bt-lib`) via pip. However, the **Bluetti AC2P** device presented several challenges that required modifications:

### Challenges with AC2P

1. **BLE Encryption Required**: Unlike older Bluetti devices, the AC2P uses **encrypted Bluetooth Low Energy (BLE) communication**. Without encryption, the device returns empty responses or "Characteristic not found" errors.

2. **Different BLE Characteristics**: The AC2P doesn't expose the standard `0000ff02-0000-1000-8000-00805f9b34fb` characteristic without establishing an encrypted session first.

3. **Protocol V2**: The AC2P uses a newer protocol (V2) with specific register addresses:
   - `102`: Total Battery Percent
   - `110-115`: Device Type
   - `116-119`: Serial Number
   - `140-147`: Power statistics (DC/AC output/input power)
   - `154`: Power Generation (kWh)
   - `1509`: AC Output On (returns value 3 when on, not 1)
   - `2012`: DC Output On
   - `2021`: Power Lifting On

4. **BoolField Handling**: The AC2P returns `3` instead of `1` for boolean "on" states, requiring modification of the `BoolField` parser to use `value != 0` instead of `value == 1`.

### Solution

This fork embeds the `bluetti_bt_lib` library directly within the custom component (instead of using pip), which allows:

- Full control over encryption implementation
- Custom handling of AC2P-specific register values
- Immediate testing without waiting for upstream library updates

## Installation

### Via HACS (Custom Repository)

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click the **⋮** menu (top right) → **Custom repositories**
4. Add: `https://github.com/atiweb/hassio-bluetti-bt`
5. Category: **Integration**
6. Click **Add**
7. Search for "Bluetti BT" and install

### Manual Installation

1. Copy the `custom_components/bluetti_bt` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Integrations**
2. Click **+ Add Integration**
3. Search for **Bluetti BT**
4. Select your device from the list
5. **Important for AC2P**: Enable encryption in the device options

### Enabling Encryption (Required for AC2P)

After adding the device:
1. Click on the device in the Bluetti BT integration
2. Click **Configure** (gear icon)
3. Enable **Use Encryption**
4. Save and restart Home Assistant

## Supported Devices

| Device | Status | Notes |
|--------|--------|-------|
| AC2P | ✅ Tested | Requires encryption enabled |
| AC2A | ✅ Supported | May require encryption |
| AC60 | ✅ Supported | |
| AC70 | ✅ Supported | |
| AC180 | ✅ Supported | |
| AC200L | ✅ Supported | |
| AC200M | ✅ Supported | |
| AC300 | ✅ Supported | |
| AC500 | ✅ Supported | |
| EB3A | ✅ Supported | |
| EP500 | ✅ Supported | |
| EP500P | ✅ Supported | |
| EP600 | ✅ Supported | |
| EP760 | ✅ Supported | |
| EP800 | ✅ Supported | |

## AC2P Sensors

| Sensor | Register | Description |
|--------|----------|-------------|
| Total Battery Percent | 102 | Battery level (0-100%) |
| DC Output Power | 140 | Power from USB/12V ports (W) |
| AC Output Power | 142 | Power from AC outlets (W) |
| DC Input Power | 144 | Solar/DC charging power (W) |
| AC Input Power | 146 | AC charging power (W) |
| Power Generation | 154 | Total energy generated (kWh) |
| AC Output | 1509 | AC outlets on/off status |
| DC Output | 2012 | USB/12V ports on/off status |
| Power Lifting | 2021 | Power lifting mode status |

## Troubleshooting

### Sensors show "Unavailable"

1. **Check encryption**: Make sure "Use Encryption" is enabled in device options
2. **Check Bluetooth**: Ensure the device is within range and powered on
3. **Check logs**: Look for errors in Home Assistant logs (`ha core logs | grep bluetti`)

### "Characteristic not found" errors

This means encryption is not enabled. Go to device options and enable "Use Encryption".

### Device not detected

- Make sure the AC2P is powered on
- Check that your Bluetooth adapter is working
- Try restarting Home Assistant

## Disclaimer

This integration is provided without any warranty or support by Bluetti. Use it at your own risk.

## Credits

- Original integration: [Patrick762/hassio-bluetti-bt](https://github.com/Patrick762/hassio-bluetti-bt)
- Encryption implementation based on community research
- AC2P testing and fixes: [@atiweb](https://github.com/atiweb)

