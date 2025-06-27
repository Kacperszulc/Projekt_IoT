from azure.iot.device import IoTHubDeviceClient, Message
import time
import threading
import random
import json

conn_str = "HostName=nawadnianiehub.azure-devices.net;DeviceId=nawadnianie-symulator;SharedAccessKey=dDX1zSSr56A4QQhimUP4Wu2Gc+ha7oA4730dNsfOkB0="

device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
device_client.connect()

def send_telemetry():
    while True:
        soil = round(random.uniform(20.0, 60.0), 1)
        tank = round(random.uniform(10.0, 100.0), 1)
        msg = Message(json.dumps({
            "soilMoisture": soil,
            "tankLevel": tank
        }))
        device_client.send_message(msg)
        print(f"Sent telemetry: {soil=}, {tank=}")
        time.sleep(10)

def listen_for_commands():
    while True:
        message = device_client.receive_message()
        print("💧 Odebrano komendę:", message.data.decode())
        if message.data.decode() == "WATER_ON":
            print("👉 Uruchamiam ręczne podlewanie!")

threading.Thread(target=send_telemetry, daemon=True).start()
threading.Thread(target=listen_for_commands, daemon=True).start()

while True:
    time.sleep(1)
