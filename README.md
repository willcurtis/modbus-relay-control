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

# 🌐 Web Control Panel (`app.py`)

A lightweight Flask web application is included to control and monitor the Modbus TCP relay board from your browser.

## 📦 Features
- View real-time relay states (ON/OFF)
- Toggle individual relays
- Pulse individual relays ON briefly (1 second)
- Auto-refresh every 5 seconds
- Simple, clean web UI (no extra frameworks)

## 🚀 How to Run

1. Install Flask and pymodbus if not already installed:
   ```bash
   pip install flask pymodbus
   ```

2. Edit `app.py` and set your relay board IP:
   ```python
   MODBUS_HOST = "your_relay_board_ip"
   ```

3. Start the web server:
   ```bash
   python3 app.py
   ```

4. Open your browser and visit:
   ```
   http://localhost:5555/
   ```

## ⚙️ Notes
- Default port is **5555** (changeable inside `app.py` if needed).
- Requires Python 3.7+.
- Works with pymodbus 3.x+ (uses keyword arguments for Modbus calls).
- Ensure your Modbus relay device is reachable on the network.

## 🖼️ Example Web Interface

<img width="546" alt="modbus_web_app" src="https://github.com/user-attachments/assets/7af08e21-c799-4ab9-87ea-2fa59299f4ca" />

> Relay dashboard showing 8 relays with real-time status and control buttons for toggling and pulsing.

---

## 📜 License

This project is licensed under the MIT License.

---

## ✨ Credits

Built with ❤️ for Modbus engineers, automation specialists, and hobbyists.

---



