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

## 🚀 Instrukcja wdrożenia

### ✅ Wymagania

- Konto [Azure](https://azure.microsoft.com/)
- Zainstalowane lokalnie:
  - Python 3.11
  - Git
- Utworzone zasoby na Azure:
  - Azure IoT Hub (zarejestrowane urządzenie symulatora)
  - Azure Table Storage
  - Azure App Service (Linux, Python 3.11)

---

### 🛠️ Krok po kroku

#### 1. Sklonuj repozytorium

git clone https://github.com/Kacperszulc/Projekt_IoT.git
cd Projekt_IoT

2. Utwórz plik .env (opcjonalnie dla lokalnych testów)

AZURE_IOTHUB_EVENT_HUB_CONN_STRING=Endpoint=sb://<...>
AZURE_IOTHUB_CONSUMER_GROUP=$Default
AZURE_TABLE_CONN_STRING=DefaultEndpointsProtocol=https;AccountName=<...>;AccountKey=<...>

4. Zainstaluj zależności

pip install -r requirements.txt

6. Uruchom lokalnie

python main.py
Aplikacja dostępna pod adresem:
http://localhost:8000

7. Wdrożenie na Azure
Zaloguj się:

az login
Zainicjuj repozytorium (jeśli nie było wcześniej):

git init
git remote add origin https://github.com/Kacperszulc/Projekt_IoT.git
git add .
git commit -m "Initial commit"
git push -u origin main --force
Wejdź na Azure Portal → App Service → Configuration
i dodaj jako Application settings:

AZURE_IOTHUB_EVENT_HUB_CONN_STRING

AZURE_IOTHUB_CONSUMER_GROUP

AZURE_TABLE_CONN_STRING

Ustaw Startup Command:

python main.py

Po restarcie aplikacja uruchomi się automatycznie.
