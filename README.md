# 🌱 Smart Garden – System Automatycznego Nawadniania

**Smart Garden** to inteligentny system monitorujący wilgotność gleby i poziom wody w zbiorniku, który automatycznie uruchamia nawadnianie lub umożliwia sterowanie ręczne. Dane telemetryczne są zapisywane w usłudze **Azure Table Storage**, a całość obsługuje backend napisany w Pythonie z użyciem **FastAPI**.

---

## 🔧 Funkcje

- Odczyt wilgotności gleby i poziomu wody przez urządzenie IoT (Arduino Nano / symulator)
- Automatyczne uruchamianie pompy, gdy wilgotność spada poniżej 30%
- Możliwość ręcznego włączenia pompy z interfejsu webowego
- Wizualizacja aktualnych danych (wilgotność, poziom wody, status pompy)
- Przechowywanie danych telemetrycznych w chmurze (Azure Table Storage)

---

## 🧰 Technologie

- **IoT**: Arduino Nano (symulator)
- **Backend**: Python + FastAPI
- **Frontend**: HTML/CSS/JS (prosty interfejs)
- **Chmura**: Microsoft Azure (IoT Hub + Table Storage)
- **Baza danych**: Azure Table Storage
- **Inne**: dotenv, Uvicorn, Azure SDK

📄 Wymagania

Python 3.10+
Azure Storage Account i Table Storage
Azure Storage Explorer

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



## 🚀 Instrukcja uruchomienia (lokalnie)

### 1. Klonowanie projektu

```bash
git clone https://github.com/twoj-uzytkownik/smart-garden.git
cd smart-garden/backend
```

### 2. Utworzenie i aktywacja środowiska wirtualnego

```bash
python -m venv venv
venv\Scripts\activate       # Windows
# lub
source venv/bin/activate    # Linux/macOS
```

### 3. Instalacja zależności

```bash
pip install -r requirements.txt
```

### 4. Plik `.env`

Utwórz plik `.env` w katalogu `backend/` i dodaj dane:

```env
AZURE_TABLE_CONN_STRING=DefaultEndpointsProtocol=... (Twoje dane z Azure Storage Explorer)
TABLE_NAME=telemetry
```

### 5. Uruchomienie backendu

```bash
uvicorn main:app --reload
```

### 6. Otwórz interfejs webowy

W przeglądarce wejdź na:

```
http://localhost:8000/
```

### 7. Wysyłanie danych z symulatora (opcjonalnie)

Uruchom skrypt symulujący dane lub użyj prawdziwego urządzenia IoT
