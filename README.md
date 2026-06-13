# 🎫 Ticket-System (Informatik-Projekt)
!! AI generated !!
Das Ticket-System ist eine Desktop-Anwendung, die mit **Python** und **PyQt6** entwickelt wurde. Sie ermöglicht es Benutzern, Support-Tickets zu erstellen und deren Bearbeitungsstatus zu verfolgen, während Administratoren die eingegangenen Tickets priorisieren, bearbeiten, kommentieren und mit den Benutzern über einen integrierten Chat kommunizieren können.

---

## 📁 Projektstruktur
Das Repository ist wie folgt strukturiert:
- **`ticket system 8/`**: Der Hauptordner des Projekts.
  - **`src/`**: Enthält den Quellcode der Anwendung.
    - [main.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/main.py): Startpunkt der Anwendung.
    - [controller.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/controller.py): Steuert den Wechsel zwischen den Fenstern (Fenster-Management).
    - **`backend/`**:
      - [database.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/backend/database.py): Verwaltet die MySQL-Datenbankverbindungen und SQL-Abfragen.
      - [prioritizing.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/backend/prioritizing.py): Definiert die ticketbezogenen Prioritätsgewichte.
      - [universal_data.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/backend/universal_data.py): Globale Variablen und Konfigurationsdaten (z. B. Support-Kategorien).
    - **`frontend/`**: Enthält die PyQt6-Benutzeroberflächen.
      - [start_window.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/frontend/start_window.py): Startbildschirm (Auswahl zwischen Login/Registrierung).
      - [login_window.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/frontend/login_window.py): Anmeldefenster.
      - [registration_window.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/frontend/registration_window.py): Registrierungsfenster.
      - [main_window.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/frontend/main_window.py): Hauptmenü nach dem Login.
      - [create_ticket.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/frontend/create_ticket.py): Formular zur Ticketerstellung.
      - [mytickets_window.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/frontend/mytickets_window.py): Ticket-Übersichtstabelle (Tabellenansicht, Detailansicht, Chat-Funktion).
  - **`data/`**: Datenbank-Dumps und Strukturdefinitionen.
    - [projekt_4_db_export.sql](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/data/projekt_4_db_export.sql): **Kompletter Datenbank-Export** (Struktur & Testdaten aller Tabellen - empfohlen).
    - [projekt_4_db_userdata.sql](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/data/projekt_4_db_userdata.sql): SQL-Dump für die Benutzerdatenbank (`userdata`).
    - [projekt_4_db_tickets.sql](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/data/projekt_4_db_tickets.sql): SQL-Dump für die Ticketdatenbank (`tickets`).
    - [userdata.txt](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/data/userdata.txt) / [tickets.txt](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/data/tickets.txt): Dokumentation des Spaltenaufbaus der Tabellen.

---

## 🛠️ Voraussetzungen & Installation

### 1. Python & Bibliotheken
Stelle sicher, dass Python 3 installiert ist. Installiere die benötigten Pakete über `pip`:
```bash
pip install PyQt6 mysql-connector-python
```

### 2. Datenbank aufsetzen
Die Anwendung benötigt eine lokale **MySQL/MariaDB**-Datenbank namens `projekt_4_db`.

1. Starte deinen MySQL-Server (z. B. über **XAMPP Control Panel** -> MySQL starten).
2. Öffne **phpMyAdmin** (meist unter http://localhost/phpmyadmin/).
3. Erstelle eine neue leere Datenbank mit dem Namen `projekt_4_db`.
4. Importiere die Datenbankstruktur:
   - **Empfohlen (inklusive Testdaten):** Importiere die vollständige Export-Datei [projekt_4_db_export.sql](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/data/projekt_4_db_export.sql) über den Reiter "Importieren" in phpMyAdmin. Diese Datei erstellt alle Tabellen (`userdata`, `tickets`, `ticket_messages`) und fügt einige Testbenutzer sowie Tickets und Chat-Nachrichten hinzu.
   - **Alternativ (nur Tabellen einzeln):** Importiere nacheinander `projekt_4_db_userdata.sql` und `projekt_4_db_tickets.sql`.

Die Verbindungsdaten in der [database.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/backend/database.py) sind standardmäßig auf eine lokale Instanz konfiguriert:
- **Host**: `localhost`
- **User**: `root`
- **Passwort**: *(leer)*
- **Datenbank**: `projekt_4_db`

---

## 🔐 Registrierung und manuelle Rollenvergabe

> [!IMPORTANT]
> **Erzeugung von Admin- und Company-Accounts**
> 
> Über die Registrierungsoberfläche der Anwendung ([registration_window.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/frontend/registration_window.py)) können sich Benutzer standardmäßig selbst registrieren. Jeder neu erstellte Account erhält automatisch die Rolle `user` (Spalte `rank`) und den Status `private` (Spalte `status`).
>
> Die Zuweisung von Administrator-Rechten oder Firmen-Prioritäten (**Admin** und **Company**) ist **ausschließlich manuell direkt in der Datenbank** möglich.
> 
> Gehe dazu in deiner SQL-Verwaltung (z.B. phpMyAdmin, MySQL Workbench) in die Tabelle `userdata` und ändere die entsprechenden Spalten für den gewünschten Account:
> - **Admin-Account**: Setze den Wert in der Spalte `rank` auf `'admin'`.
> - **Company-Account (Firmenkunde)**: Setze den Wert in der Spalte `status` auf `'company'`.
>
> *Beispiel-SQL-Befehl für die Zuweisung:*
> ```sql
> UPDATE userdata SET rank = 'admin', status = 'company' WHERE username = 'DeinBenutzername';
> ```

---

## 📈 Funktionsweise & Features

### 1. Dynamische Ticket-Priorisierung
Das System verwendet eine SQL-Berechnung in der [database.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/backend/database.py) unter `get_user_tickets()`, um Tickets für Administratoren nach Dringlichkeit zu sortieren. Die Priorität errechnet sich wie folgt:
- Jede Support-Kategorie hat ein vordefiniertes Basisgewicht (z. B. *Security or Privacy* = 15, *Network Issues* = 8, *Suggestions* = 1; definiert in [universal_data.py](file:///c:/Users/Paul/Desktop/Documents/GitHub/project-4%20(PC)/ticket%20system%208/src/backend/universal_data.py)).
- Wenn der Ersteller des Tickets ein Firmenkunde (`status = 'company'`) ist, wird das Basisgewicht mit einem Faktor von **1.3** multipliziert.
- Jedes Ticket gewinnt täglich an Dringlichkeit (**+0.2** Punkte pro Tag, berechnet über `DATEDIFF(NOW(), date_time) * 0.2`).
- Geschlossene Tickets (`status = 'closed'`) werden mit einer Priorität von `0` einsortiert.

### 2. Ticket-Detailansicht und Chat
- Sobald ein Ticket den Status `in progress` (in Bearbeitung) oder `closed` (geschlossen) erreicht, wird ein interaktiver Chat zwischen dem Benutzer und dem Support-Team freigeschaltet.
- Beim Schließen eines Tickets (`closed`) ist die Eingabe eines finalen Kommentars durch den Administrator zwingend erforderlich.

### 3. Benutzerrollen
- **Benutzer (Rank: `user`)**: Kann Tickets erstellen, die eigenen Tickets einsehen, im Chat schreiben und eigene Tickets löschen.
- **Administratoren (Rank: `admin`)**: Können alle Tickets des Systems einsehen, den Status von Tickets ändern (open ➔ in progress ➔ closed), Chatnachrichten verfassen und Tickets löschen.

---

## 🚀 Anwendung starten
Navigiere in der Konsole in das Verzeichnis `ticket system 8` und führe die Hauptdatei aus:
```powershell
cd "ticket system 8"
python src/main.py
```
