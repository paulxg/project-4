import sys
from PyQt6.QtWidgets import QApplication
from controller import Controller
#Todo Prioriation logik
#Todo

def main():
    # Die Basis für jede PyQt-App
    app = QApplication(sys.argv)

    # Der Controller wird erstellt und übernimmt ab hier
    app_controller = Controller()
    app_controller.show_start_screen()

    # Startet den Event-Loop (hält das Programm offen)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()