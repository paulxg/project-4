import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel

class DatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQLite in PyQt anzeigen")
        self.resize(600, 400)

        # 1. Datenbankverbindung herstellen
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('database.db') # Pfad zu deiner .db Datei

        if not self.db.open():
            print("Datenbank konnte nicht geöffnet werden!")
            sys.exit(1)

        # 2. Modell erstellen und Tabelle festlegen
        self.model = QSqlTableModel()
        self.model.setTable('userdata') # Name der Tabelle in der DB
        self.model.select() # Daten aus der Tabelle laden

        # 3. View erstellen und Modell zuweisen
        self.view = QTableView()
        self.view.setModel(self.model)

        # Layout setzen
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

app = QApplication(sys.argv)
window = DatabaseApp()
window.show()
sys.exit(app.exec())
