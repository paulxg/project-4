from PyQt6.QtWidgets import QTableView, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from backend.UniversalData import CurrentUserdata, ProgramData
from PyQt6.QtCore import pyqtSignal


class MyTicketsWindow(QWidget):
    request_main_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyTickets")
        self.setFixedSize(896, 504)

        # Widget bekommt Tabellenraster
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.backtomain = QPushButton("Back to Main Window")
        self.backtomain.clicked.connect(self.request_main_window.emit)


        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("backend/database.db")

        if not self.db.open():
            print ("Error connecting to database")
            return

        query = QSqlQuery("SELECT date, category, shortdescription, longdescription FROM tickets")
        self.model = QSqlQueryModel()
        self.model.setQuery(query)


        #todo id filter einbauen

        self.view = QTableView()
        self.view.setModel(self.model)

        layout.addWidget(self.view)
        layout.addWidget(self.backtomain)