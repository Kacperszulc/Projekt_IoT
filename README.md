# 🌱 Smart Garden – IoT System for Automatic Plant Watering

Smart Garden to aplikacja IoT umożliwiająca zdalne monitorowanie poziomu wilgotności gleby i stanu zbiornika na wodę oraz automatyczne/ręczne sterowanie podlewaniem roślin.

---


🧑‍🌾 User Stories

1. Jako właściciel ogrodu,
chcę mieć możliwość monitorowania wilgotności gleby i poziomu wody w zbiorniku,
aby podejmować decyzje o nawadnianiu roślin w sposób świadomy i oszczędny.

2. Jako użytkownik aplikacji,
chcę widzieć, kiedy system sam uruchomił podlewanie,
aby upewnić się, że działa on automatycznie, gdy rośliny tego potrzebują.

3. Jako użytkownik,
chcę mieć możliwość ręcznego włączenia nawadniania,
aby podlewać rośliny niezależnie od automatycznych decyzji systemu.


## 📦 Skład projektu

- **Backend (Python + Flask)**: Odbiera dane z IoT Hub, zapisuje do Azure Table Storage, udostępnia API.
- **Frontend (HTML + JS)**: Pokazuje dane telemetryczne, umożliwia ręczne uruchomienie podlewania.
- **IoT Device (Symulator)**: Wysyła dane telemetryczne do Azure IoT Hub.
- **Azure Resources**:
  - IoT Hub
  - Azure Table Storage
  - App Service (Web App for Containers)
  - Application Insights (opcjonalnie)

---

## ⚙️ Jak działa

1. **Symulator** wysyła dane (`soilMoisture`, `tankLevel`) do **Azure IoT Hub**.
2. **Backend** nasłuchuje Event Hub Endpoint z IoT Huba, przetwarza dane i zapisuje je do **Azure Table Storage**.
3. **Frontend** cyklicznie pobiera najnowsze dane z endpointu `/latest` i je wyświetla.
4. Użytkownik może ręcznie włączyć podlewanie przyciskiem. Informacja ta również trafia do Storage.

---

## 🔧 Uruchomienie lokalne

1. Utwórz plik `.env` z wymaganymi zmiennymi:
   ```env
   AZURE_IOTHUB_EVENT_HUB_CONN_STRING=...
   AZURE_IOTHUB_CONSUMER_GROUP=$Default
   AZURE_TABLE_CONN_STRING=...
