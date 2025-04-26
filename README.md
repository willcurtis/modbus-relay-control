# Modbus Relay Controller CLI

Control an 8-relay Modbus TCP device easily using a command-line tool or an interactive menu.

Supports:
- Turning individual relays ON/OFF
- Turning all relays ON/OFF
- Reading relay states
- Saving relay states as profiles
- Loading relay states from profiles
- Listing available profiles (no device connection needed)

---

## 📦 Features

- **Command-line mode** for scripting and automation
- **Interactive menu** for manual control
- **Relay profiles** to save and load common relay configurations
- **Logging** of all actions to `relay_control.log`
- **Automatic reconnection** on startup
- **Timeouts and error handling**

---

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/modbus-relay-cli.git
   cd modbus-relay-cli
   ```

2. Install dependencies:
   ```bash
   pip install pymodbus
   ```

---

## ⚙️ Usage

### Command-Line Mode

Run one-off commands:

- **Turn a specific relay ON or OFF**
  ```bash
  python modbus_relay_cli.py --ip 10.194.10.14 --relay 3 --state on
  ```

- **Turn ALL relays ON or OFF**
  ```bash
  python modbus_relay_cli.py --ip 10.194.10.14 --all --state off
  ```

- **Read all relay statuses**
  ```bash
  python modbus_relay_cli.py --ip 10.194.10.14 --status
  ```

- **Save current relay states as a profile**
  ```bash
  python modbus_relay_cli.py --ip 10.194.10.14 --save-profile myprofile
  ```

- **Load a saved profile**
  ```bash
  python modbus_relay_cli.py --ip 10.194.10.14 --load-profile myprofile
  ```

- **List available profiles (no device required)**
  ```bash
  python modbus_relay_cli.py --list-profiles
  ```


### Interactive Menu

Just run without extra options:

```bash
python modbus_relay_cli.py --ip 10.194.10.14
```

You’ll see a simple menu:
```
🔹 Modbus Relay Control Menu 🔹
1️⃣  Toggle Relay ON/OFF
2️⃣  Enable/Disable ALL Relays
3️⃣  Show Relay Status
4️⃣  Save Profile
5️⃣  Load Profile
6️⃣  List Profiles
7️⃣  Exit
```

---

## 🛠 Configuration

- **Default Modbus TCP port**: `502`
- **Relay address mapping**: Relay 1 → Coil 0, Relay 2 → Coil 1, etc.
- **Profiles**: Stored in `relay_profiles.json`
- **Logs**: Stored in `relay_control.log`

---

## 📋 Requirements

- Python 3.7+
- `pymodbus`
- A reachable Modbus TCP relay device (8 coils expected)

---

## 📜 License

This project is licensed under the MIT License.

---

## ✨ Credits

Built with ❤️ for Modbus engineers, automation specialists, and hobbyists.

---

