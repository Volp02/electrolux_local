# Electrolux / AEG Local Control for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Volp02/electrolux_local)](https://github.com/Volp02/electrolux_local/releases)
[![License](https://img.shields.io/github/license/Volp02/electrolux_local)](LICENSE)

A custom component for **Home Assistant** that provides **local** control for Electrolux/AEG appliances (specifically AC units with Broadlink chips, type `0x4f9b`) without relying on the discontinued Electrolux Cloud API.

## 🌟 Features

*   **100% Local Control**: No cloud dependency, no internet required, and no risk of API deprecation.
*   **Fast Response**: Instant feedback compared to cloud polling.
*   **Full Climate Control**:
    *   Power (On/Off)
    *   Operation Modes (Auto, Cool, Heat, Dry, Fan Only)
    *   Fan Speeds (Auto, Low, Mid, High)
    *   Target Temperature
    *   Current Temperature Sensor
*   **Config Flow**: Easy setup via Home Assistant UI (manual IP entry).

## 🚀 Installation

### Option 1: HACS (Recommended)

1.  Open **HACS** in Home Assistant.
2.  Go to **Integrations** > 3 dots (top right) > **Custom repositories**.
3.  Add `https://github.com/Volp02/electrolux_local` with category **Integration**.
4.  Click **Add** and then **Download**.
5.  **Restart Home Assistant**.

### Option 2: Manual Installation

1.  Download the latest [Release](https://github.com/Volp02/electrolux_local/releases/latest).
2.  Extract the `custom_components/electrolux_local` folder.
3.  Copy this folder to your Home Assistant `config/custom_components/` directory.
4.  **Restart Home Assistant**.

## ⚙️ Configuration

1.  Navigate to **Settings** > **Devices & Services** > **Add Integration**.
2.  Search for **Electrolux Local Control**.
3.  Enter the **IP Address** of your AC unit (e.g., `192.168.1.100`).
    *   *Tip: Assign a static IP to your AC in your router settings to prevent connection issues.*
4.  The integration will detect the MAC address and add the device.

## 📋 Supported Devices

*   **Electrolux WP71-265WT** (Portable Air Conditioner)
*   Potentially other Electrolux/AEG devices using the Broadlink `0x4f9b` OEM chip.

## 🛠 Troubleshooting

**"Invalid handler specified" Error:**
If you see this during setup, it usually means Home Assistant needs a restart to load the new config flow files properly. Restart HA and try again.

**Device not found:**
Ensure the device is powered on and connected to the same Wi-Fi network as Home Assistant. You can verify connectivity by pinging the IP address.

## ❤️ Credits

*   Based on reverse-engineering work by the Home Assistant community.
*   Uses the [python-broadlink](https://github.com/mjg59/python-broadlink) library.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
