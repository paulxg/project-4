import sys
from PyQt6.QtWidgets import QApplication
from controller import Controller
from backend.database import Database
#Todo Prioriation logik
#Todo

def main():
    # Die Basis für jede PyQt-App
    app = QApplication(sys.argv)

    # Tabellen anlegen falls nicht vorhanden
    try:
        Database().create_messages_table()
    except Exception as e:
        print(f"Fehler beim Anlegen der Tabellen: {e}")

    # Der Controller wird erstellt und übernimmt ab hier
    app_controller = Controller()
    app_controller.show_start_screen()

    # Startet den Event-Loop (hält das Programm offen)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()