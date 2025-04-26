import time
import sys
import argparse
import logging
import json
import os
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# Setup logging
logger = logging.getLogger("RelayController")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("relay_control.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

PROFILE_FILE = "relay_profiles.json"

class ModbusRelayController:
    def __init__(self, ip, port=502, timeout=5):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.client = ModbusTcpClient(host=ip, port=port, timeout=timeout)
        self.connected = self.connect()

    def connect(self, retries=3):
        for attempt in range(1, retries + 1):
            if self.client.connect():
                logger.info(f"✅ Connected to Modbus relay at {self.ip}:{self.port}")
                return True
            else:
                logger.warning(f"Attempt {attempt}/{retries}: Connection failed. Retrying...")
                time.sleep(1)
        logger.error("❌ Could not connect to Modbus relay after retries.")
        return False

    def set_relay_state(self, relay_id, state):
        if not self.connected:
            logger.error("❌ Not connected to Modbus relay.")
            return
        try:
            relay_address = relay_id - 1
            response = self.client.write_coil(address=relay_address, value=state)
            if response.isError():
                logger.error(f"❌ Failed to set Relay {relay_id} to {'ON' if state else 'OFF'}.")
            else:
                logger.info(f"✅ Relay {relay_id} set to {'ON' if state else 'OFF'} successfully.")
        except ModbusException as e:
            logger.error(f"❌ Modbus exception: {e}")

    def set_all_relays(self, state):
        if not self.connected:
            logger.error("❌ Not connected to Modbus relay.")
            return
        logger.info(f"🔄 Setting ALL relays to {'ON' if state else 'OFF'}...")
        for relay_id in range(1, 9):
            self.set_relay_state(relay_id, state)
            time.sleep(0.05)
        logger.info("✅ All relays updated.")

    def read_relay_state(self, relay_id):
        if not self.connected:
            logger.error("❌ Not connected to Modbus relay.")
            return None
        try:
            relay_address = relay_id - 1
            response = self.client.read_coils(address=relay_address, count=1)
            if response.isError():
                logger.error(f"❌ Failed to read state of Relay {relay_id}.")
                return None
            return response.bits[0]
        except ModbusException as e:
            logger.error(f"❌ Modbus exception: {e}")
            return None

    def read_all_relays(self):
        if not self.connected:
            logger.error("❌ Not connected to Modbus relay.")
            return
        try:
            response = self.client.read_coils(address=0, count=8)
            if response.isError():
                logger.error("❌ Failed to read relay states.")
                return
            states = response.bits[:8]
            logger.info("🔎 Relay Status:")
            for i, state in enumerate(states, start=1):
                logger.info(f"  Relay {i}: {'ON' if state else 'OFF'}")
            return states
        except ModbusException as e:
            logger.error(f"❌ Modbus exception: {e}")
            return None

    def close(self):
        if self.connected:
            self.client.close()
            logger.info("🔌 Connection closed.")

def save_profile(controller, profile_name):
    states = controller.read_all_relays()
    if states is None:
        logger.error("❌ Cannot save profile. Could not read relay states.")
        return
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            profiles = json.load(f)
    else:
        profiles = {}
    profiles[profile_name] = states
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=2)
    logger.info(f"✅ Profile '{profile_name}' saved.")

def load_profile(controller, profile_name):
    if not os.path.exists(PROFILE_FILE):
        logger.error("❌ No profiles found.")
        return
    with open(PROFILE_FILE, "r") as f:
        profiles = json.load(f)
    if profile_name not in profiles:
        logger.error(f"❌ Profile '{profile_name}' not found.")
        return
    states = profiles[profile_name]
    logger.info(f"🔄 Loading profile '{profile_name}'...")
    for relay_id, state in enumerate(states, start=1):
        controller.set_relay_state(relay_id, state)
        time.sleep(0.05)
    logger.info("✅ Profile applied.")

def list_profiles():
    if not os.path.exists(PROFILE_FILE):
        logger.error("❌ No profiles found.")
        return
    with open(PROFILE_FILE, "r") as f:
        profiles = json.load(f)
    logger.info("📋 Available Profiles:")
    for name in profiles.keys():
        logger.info(f" - {name}")

def interactive_menu(controller):
    while True:
        print("\n🔹 Modbus Relay Control Menu 🔹")
        print("1️⃣  Toggle Relay ON/OFF")
        print("2️⃣  Enable/Disable ALL Relays")
        print("3️⃣  Show Relay Status")
        print("4️⃣  Save Profile")
        print("5️⃣  Load Profile")
        print("6️⃣  List Profiles")
        print("7️⃣  Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            try:
                relay_id = int(input("\nEnter relay number (1-8): "))
                if 1 <= relay_id <= 8:
                    state_choice = input("Turn relay ON or OFF? (on/off): ").strip().lower()
                    if state_choice == "on":
                        controller.set_relay_state(relay_id, True)
                    elif state_choice == "off":
                        controller.set_relay_state(relay_id, False)
                    else:
                        logger.error("❌ Invalid choice. Please enter 'on' or 'off'.")
                else:
                    logger.error("❌ Invalid relay number. Please enter between 1 and 8.")
            except ValueError:
                logger.error("❌ Invalid input. Please enter a number.")

        elif choice == "2":
            state_choice = input("\nEnable or Disable ALL relays? (on/off): ").strip().lower()
            if state_choice == "on":
                controller.set_all_relays(True)
            elif state_choice == "off":
                controller.set_all_relays(False)
            else:
                logger.error("❌ Invalid choice. Please enter 'on' or 'off'.")

        elif choice == "3":
            controller.read_all_relays()

        elif choice == "4":
            profile_name = input("Enter profile name to save: ").strip()
            save_profile(controller, profile_name)

        elif choice == "5":
            profile_name = input("Enter profile name to load: ").strip()
            load_profile(controller, profile_name)

        elif choice == "6":
            list_profiles()

        elif choice == "7":
            controller.close()
            sys.exit(0)

        else:
            logger.error("❌ Invalid menu choice.")

def run_cli_command(controller, args):
    if args.save_profile:
        save_profile(controller, args.save_profile)
    elif args.load_profile:
        load_profile(controller, args.load_profile)
    elif args.list_profiles:
        list_profiles()
    elif args.all:
        state = args.state.lower() == "on"
        controller.set_all_relays(state)
    elif args.relay:
        state = args.state.lower() == "on"
        controller.set_relay_state(args.relay, state)
    elif args.status:
        controller.read_all_relays()
    controller.close()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Control Modbus TCP Relay Board.")
    parser.add_argument("--ip", help="IP address of the relay board")
    parser.add_argument("--port", type=int, default=502, help="TCP port (default 502)")
    parser.add_argument("--relay", type=int, help="Relay number to toggle (1-8)")
    parser.add_argument("--state", choices=["on", "off"], help="State to set relay or all relays")
    parser.add_argument("--all", action="store_true", help="Set all relays on/off")
    parser.add_argument("--status", action="store_true", help="Read status of all relays")
    parser.add_argument("--save-profile", type=str, help="Save current relay state as a profile")
    parser.add_argument("--load-profile", type=str, help="Load relay states from a saved profile")
    parser.add_argument("--list-profiles", action="store_true", help="List all available profiles")
    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.list_profiles:
        list_profiles()
        sys.exit(0)

    if not args.ip:
        print("❌ Error: --ip is required unless using --list-profiles.")
        sys.exit(1)

    controller = ModbusRelayController(args.ip, args.port)

    if not controller.connected:
        sys.exit(1)

    if args.relay or args.all or args.status or args.save_profile or args.load_profile:
        run_cli_command(controller, args)
    else:
        interactive_menu(controller)

if __name__ == "__main__":
    main()
