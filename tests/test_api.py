import requests

BASE_URL = "http://localhost:8000"

def test_send_telemetry():
    payload = {
        "soilMoisture": 35,
        "tankLevel": 80
    }
    response = requests.post(f"{BASE_URL}/telemetry", json=payload)
    print("Telemetry response:", response.status_code, response.json())

def test_manual_watering():
    payload = {
        "turnOn": True
    }
    response = requests.post(f"{BASE_URL}/manual-watering", json=payload)
    print("Manual watering response:", response.status_code, response.json())

def test_get_latest_data():
    response = requests.get(f"{BASE_URL}/latest")
    print("Latest telemetry response:", response.status_code, response.json())

if __name__ == "__main__":
    print("== TESTING API ==")
    test_send_telemetry()
    test_manual_watering()
    test_get_latest_data()
