# Modbus Relay Control CLI

Control 8-channel Modbus TCP relay boards easily using a command-line tool or an interactive menu.

Supports:
- Turning individual relays ON/OFF
- Momentary pulse control (ON then OFF)
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
- **Homebrew support** for easy installation

---

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/willcurtis/modbus-relay-control.git
   cd modbus-relay-control
   ```

2. Install dependencies:
   ```bash
   pip install pymodbus
   ```

3. (Optional) Install via Homebrew:
   ```bash
   brew tap willcurtis/modbus
   brew install modbus-relay-control
   ```

---

## ⚙️ Usage

### Command-Line Mode

Run one-off commands:

- **Turn a specific relay ON or OFF**
  ```bash
  modbus-relay --ip 10.194.10.14 --relay 3 --state on
  ```

- **Pulse a specific relay ON then OFF**
  ```bash
  modbus-relay --ip 10.194.10.14 --relay 3 --momentary --duration 1
  ```

- **Turn ALL relays ON or OFF**
  ```bash
  modbus-relay --ip 10.194.10.14 --all --state off
  ```

- **Read all relay statuses**
  ```bash
  modbus-relay --ip 10.194.10.14 --status
  ```

- **Save current relay states as a profile**
  ```bash
  modbus-relay --ip 10.194.10.14 --save-profile myprofile
  ```

- **Load a saved profile**
  ```bash
  modbus-relay --ip 10.194.10.14 --load-profile myprofile
  ```

- **List available profiles (no device required)**
  ```bash
  modbus-relay --list-profiles
  ```


### Interactive Menu

Just run without extra options:

```bash
modbus-relay --ip 10.194.10.14
```

You’ll see a simple menu:
```
🔹 Modbus Relay Control Menu 🔹
1️⃣  Toggle Relay ON/OFF
2️⃣  Enable/Disable ALL Relays
3️⃣  Show Relay Status
4️⃣  Pulse a Relay ON momentarily
5️⃣  Save Profile
6️⃣  Load Profile
7️⃣  List Profiles
8️⃣  Exit
```

---

## 🛠 Configuration

- **Default Modbus TCP port**: `502`
- **Relay address mapping**: Relay 1 → Coil 0, Relay 2 → Coil 1, etc.
- **Profiles**: Stored in `relay_profiles.json`
- **Logs**: Stored in `relay_control.log`

---

## 📋 Requirements

- macOS, Linux (tested)
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



