# Electrolux Local for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Volp02/electrolux_local)](https://github.com/Volp02/electrolux_local/releases)

A custom component for **Home Assistant** that interacts with **Electrolux** appliances locally.

## 🌟 Features

* **Local Control**: Communicates directly with devices on your network (reducing latency and reliance on the cloud).
* **Sensors**: Reads status, time remaining, and other sensor data.
* **Controls**: Start/Stop/Pause functionality (depending on device support).
* **Plug & Play**: Designed to work with the standard Home Assistant architecture.

## 🚀 Installation

### Option 1: HACS (Recommended)

1.  Open **HACS** in your Home Assistant instance.
2.  Go to **Integrations**.
3.  Click the three dots in the top right corner and select **Custom repositories**.
4.  Paste the URL of this repository:
    `https://github.com/Volp02/electrolux_local`
5.  Select **Integration** as the category.
6.  Click **Add**.
7.  Once added, close the modal, search for "Electrolux Local," and install it.
8.  **Restart Home Assistant**.

### Option 2: Manual Installation

1.  Download the latest release as a ZIP file.
2.  Extract the `custom_components/electrolux_local` folder.
3.  Copy this folder into your Home Assistant's `config/custom_components/` directory.
4.  **Restart Home Assistant**.

## ⚙️ Configuration

1.  Go to **Settings** > **Devices & Services**.
2.  Click **+ Add Integration**.
3.  Search for **Electrolux Local**.
4.  Follow the configuration steps (you may need to provide the IP address of your appliance or your Electrolux account credentials if a token is required).

## 📋 Supported Devices

* [List devices here, e.g., Electrolux Washers]
* [e.g., Electrolux Air Purifiers]
* [e.g., AEG equivalents]

## 🛠 Troubleshooting

If you encounter issues:
1.  Enable debug logging in your `configuration.yaml`:
    ```yaml
    logger:
      default: info
      logs:
        custom_components.electrolux_local: debug
    ```
2.  Check the Home Assistant logs for errors.
3.  Open an issue on GitHub with your log output.

## ❤️ Credits

* Maintained by [Volp02](https://github.com/Volp02)

## 📄 License

[License Name, e.g., MIT or Apache 2.0]