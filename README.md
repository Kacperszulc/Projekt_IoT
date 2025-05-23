Smart Garden - README

📘 Opis projektu

Smart Garden to inteligentny system monitorowania wilgotności gleby i poziomu wody w zbiorniku, z automatycznym oraz ręcznym sterowaniem podlewaniem. Dane przesyłane są do backendu opartego na FastAPI, a następnie zapisywane w Azure Table Storage.
Frontend udostępnia użytkownikowi dashboard z aktualnymi odczytami i umożliwia ręczne uruchomienie nawadniania.

🚀 Funkcjonalności

Wysyłanie danych telemetrycznych (symulowanych): wilgotność gleby, poziom wody
Automatyczne włączanie nawadniania, gdy wilgotność < 30%
Ręczne włączanie pompy z poziomu interfejsu WWW
Zapis danych do Azure Table Storage
Dashboard HTML z aktualnymi odczytami i statusem pompy

📄 Wymagania

Python 3.10+
Azure Storage Account i Table Storage
Konto w Azure Portal (do konfiguracji)

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
