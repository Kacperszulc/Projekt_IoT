from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from azure.data.tables import TableServiceClient
from datetime import datetime
import os

load_dotenv()

AZURE_TABLE_CONN_STRING = os.getenv("AZURE_TABLE_CONN_STRING")
TABLE_NAME = os.getenv("TABLE_NAME")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

table_service = TableServiceClient.from_connection_string(conn_str=AZURE_TABLE_CONN_STRING)
table_client = table_service.get_table_client(table_name=TABLE_NAME)

try:
    table_client.create_table()
except:
    pass

class Telemetry(BaseModel):
    soilMoisture: float
    tankLevel: float

latest_telemetry = None
watering_active = False

def record_watering_event(is_watering: bool):
    entity = {
        "PartitionKey": "watering",
        "RowKey": str(datetime.utcnow().timestamp()).replace('.', ''),
        "watering": "true" if is_watering else "false",
        "timestamp": datetime.utcnow().isoformat()
    }
    table_client.create_entity(entity=entity)

@app.post("/telemetry")
async def post_telemetry(data: Telemetry):
    global latest_telemetry, watering_active
    latest_telemetry = data

    # Automatyczne włączanie podlewania jeśli wilgotność < 30%
    if data.soilMoisture < 30:
        if not watering_active:
            watering_active = True
            record_watering_event(is_watering=True)
    else:
        if watering_active:
            watering_active = False
            record_watering_event(is_watering=False)

    entity = {
        "PartitionKey": "telemetry",
        "RowKey": str(datetime.utcnow().timestamp()).replace('.', ''),
        "soilMoisture": str(data.soilMoisture),
        "tankLevel": str(data.tankLevel),
        "watering": "true" if watering_active else "false",
        "timestamp": datetime.utcnow().isoformat()
    }
    table_client.create_entity(entity=entity)

    return {"status": "ok"}

@app.get("/latest")
async def get_latest():
    if latest_telemetry is None:
        return {"detail": "No telemetry data yet"}, 404
    return {
        "soilMoisture": latest_telemetry.soilMoisture,
        "tankLevel": latest_telemetry.tankLevel,
        "watering": watering_active
    }

@app.post("/manual-watering")
async def manual_watering():
    global watering_active
    if not watering_active:
        watering_active = True
        record_watering_event(is_watering=True)
    return {"watering": "on"}
