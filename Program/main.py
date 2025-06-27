import os
import threading
import asyncio
import json
from datetime import datetime, timezone
from flask import Flask, jsonify, request, render_template, redirect, url_for
from azure.data.tables import TableServiceClient
from azure.eventhub.aio import EventHubConsumerClient


app = Flask(__name__)

# === Konfiguracja zmiennych środowiskowych ===
IOTHUB_CONN_STR = os.getenv("AZURE_IOTHUB_EVENT_HUB_CONN_STRING")
CONSUMER_GROUP = os.getenv("AZURE_IOTHUB_CONSUMER_GROUP", "$Default")
STORAGE_CONN_STR = os.getenv("AZURE_TABLE_CONN_STRING")
TABLE_NAME = "telemetry"

# === Inicjalizacja klienta tabeli ===
table_service = TableServiceClient.from_connection_string(STORAGE_CONN_STR)
table_client = table_service.get_table_client(TABLE_NAME)

# === Zmienna globalna do aktualnego stanu ===
latest_data = {}

# === Odbieranie danych z EventHub ===
async def on_event(partition_context, event):
    global latest_data
    try:
        data = json.loads(event.body_as_str())
        soil_moisture = round(float(data.get("soilMoisture", 0)), 1)
        tank_level = round(float(data.get("tankLevel", 0)), 1)
        watering = latest_data.get("watering", False)

        if soil_moisture < 30:
            watering = True
        else:
            watering = False

        timestamp = datetime.now(timezone.utc)
        entity = {
            "PartitionKey": "telemetry",
            "RowKey": str(timestamp.timestamp()).replace('.', ''),
            "soilMoisture": str(soil_moisture),
            "tankLevel": str(tank_level),
            "watering": str(watering).lower(),
            "timestamp": timestamp.isoformat()
        }
        table_client.create_entity(entity=entity)

        latest_data = {
            "soilMoisture": soil_moisture,
            "tankLevel": tank_level,
            "watering": watering
        }

        await partition_context.update_checkpoint(event)
    except Exception as e:
        print("❌ Błąd odbioru z EventHub:", e)

async def receive_loop():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=IOTHUB_CONN_STR,
        consumer_group=CONSUMER_GROUP
    )
    async with client:
        await client.receive(on_event=on_event, starting_position="-1")

def start_receiver():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(receive_loop())

# === Uruchom odbieranie w tle po starcie aplikacji ===
threading.Thread(target=start_receiver, daemon=True).start()

# === ROUTES ===
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/latest")
def latest():
    return jsonify(latest_data if latest_data else {})

@app.route("/manual-watering", methods=["POST"])
def manual_watering():
    global latest_data
    timestamp = datetime.now(timezone.utc)
    entity = {
        "PartitionKey": "telemetry",
        "RowKey": str(timestamp.timestamp()).replace('.', ''),
        "soilMoisture": latest_data.get("soilMoisture", "0"),
        "tankLevel": latest_data.get("tankLevel", "0"),
        "watering": "true",
        "timestamp": timestamp.isoformat()
    }
    table_client.create_entity(entity=entity)
    latest_data["watering"] = True
    return redirect(url_for("waiting"))

@app.route("/waiting")
def waiting():
    return "<h2>💧 Ręczne podlewanie... Proszę czekać na aktualizację danych.</h2><script>setTimeout(()=>window.location='/', 5000)</script>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)