#!/usr/bin/env python3

import time
import threading
from flask import Flask, jsonify, request, render_template_string
from pymodbus.client import ModbusTcpClient

# Setup Flask
app = Flask(__name__)

# Config: Your relay board
MODBUS_HOST = "10.194.10.154"  # <-- CHANGE to your relay board IP
MODBUS_PORT = 502

# Setup Modbus Client
client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
client.connect()

# Relay control functions
def get_relay_states():
    result = client.read_coils(address=0, count=8)
    if result.isError():
        return [False] * 8
    return result.bits[:8]

def set_relay(relay_id, state):
    address = relay_id - 1
    client.write_coil(address=address, value=state)

def pulse_relay(relay_id, duration=1.0):
    set_relay(relay_id, True)
    time.sleep(duration)
    set_relay(relay_id, False)

def set_all_relays(state):
    for i in range(1, 9):
        set_relay(i, state)
        time.sleep(0.05)

# Routes
@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/api/status')
def api_status():
    states = get_relay_states()
    return jsonify(states)

@app.route('/api/relay/<int:relay_id>/<action>', methods=["POST"])
def api_relay(relay_id, action):
    if action == "on":
        set_relay(relay_id, True)
    elif action == "off":
        set_relay(relay_id, False)
    elif action == "pulse":
        threading.Thread(target=pulse_relay, args=(relay_id,)).start()
    else:
        return jsonify({"error": "Invalid action"}), 400
    return jsonify({"success": True})

@app.route('/api/all/on', methods=["POST"])
def api_all_on():
    threading.Thread(target=lambda: set_all_relays(True)).start()
    return jsonify({"success": True})

@app.route('/api/all/off', methods=["POST"])
def api_all_off():
    threading.Thread(target=lambda: set_all_relays(False)).start()
    return jsonify({"success": True})

# HTML + JS frontend
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Modbus Relay Control</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; }
    .relay { display: flex; align-items: center; margin-bottom: 10px; }
    .relay button { width: 100px; height: 40px; margin-right: 10px; }
    .group-buttons { margin-bottom: 30px; }
    .on { background-color: lightgreen; }
    .off { background-color: lightgray; }
  </style>
</head>
<body>
  <h1>🔌 Modbus Relay Control Panel</h1>

  <div class="group-buttons">
    <button onclick="allOn()" style="background-color: lightgreen; width: 120px; height: 50px; margin-right: 10px;">All ON</button>
    <button onclick="allOff()" style="background-color: lightcoral; width: 120px; height: 50px;">All OFF</button>
  </div>

  <div id="relays"></div>

<script>
function updateRelays() {
  fetch('/api/status')
    .then(response => response.json())
    .then(states => {
      const container = document.getElementById('relays');
      container.innerHTML = '';
      states.forEach((state, index) => {
        const relayId = index + 1;
        const div = document.createElement('div');
        div.className = 'relay';
        const toggleBtn = document.createElement('button');
        toggleBtn.textContent = 'Relay ' + relayId + ' ' + (state ? 'ON' : 'OFF');
        toggleBtn.className = state ? 'on' : 'off';
        toggleBtn.onclick = () => {
          fetch('/api/relay/' + relayId + '/' + (state ? 'off' : 'on'), {method: 'POST'})
            .then(updateRelays);
        };
        const pulseBtn = document.createElement('button');
        pulseBtn.textContent = 'Pulse';
        pulseBtn.onclick = () => {
          fetch('/api/relay/' + relayId + '/pulse', {method: 'POST'})
            .then(updateRelays);
        };
        div.appendChild(toggleBtn);
        div.appendChild(pulseBtn);
        container.appendChild(div);
      });
    });
}

function allOn() {
  fetch('/api/all/on', {method: 'POST'}).then(() => setTimeout(updateRelays, 1000));
}

function allOff() {
  fetch('/api/all/off', {method: 'POST'}).then(() => setTimeout(updateRelays, 1000));
}

setInterval(updateRelays, 5000);
updateRelays();
</script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
