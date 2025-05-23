import random
import time
import json
import requests
from azure.iot.device import IoTHubDeviceClient, Message


CONNECTION_STRING = "HostName=nawadnianiehub.azure-devices.net;DeviceId=nawadnianie-symulator;SharedAccessKey=dDX1zSSr56A4QQhimUP4Wu2Gc+ha7oA4730dNsfOkB0=" 
BACKEND_URL = "http://127.0.0.1:8000/telemetry"  # lokalny FastAPI backend

#  Inicjalizacja klienta do Azure IoT Hub
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
device_client.connect()
print(" Połączono z Azure IoT Hub")

#  Pętla symulująca dane
try:
    while True:
        #  Generowanie przykładowych danych telemetrycznych
        soil_moisture = random.randint(10, 90)
        tank_level = random.randint(0, 100)

        telemetry_data = {
            "soilMoisture": soil_moisture,
            "tankLevel": tank_level
        }

        # Wysyłanie danych do Azure IoT Hub
        message = Message(json.dumps(telemetry_data))
        device_client.send_message(message)
        print(f" Wysłano do IoT Hub: {telemetry_data}")

        #  Wysyłanie danych do backendu FastAPI
        try:
            response = requests.post(BACKEND_URL, json=telemetry_data)
            if response.status_code == 200:
                print(" Wysłano do backendu FastAPI")
            else:
                print(f" Błąd HTTP: {response.status_code}")
        except Exception as e:
            print(f" Błąd połączenia z backendem: {e}")

        #  Odczekaj przed kolejną iteracją
        time.sleep(5)

except KeyboardInterrupt:
    print(" Przerwano przez użytkownika")

finally:
    print(" Rozłączanie z IoT Hub...")
    device_client.disconnect()
