from PyQt6.QtWidgets import QTableView, QWidget, QVBoxLayout, QPushButton, QHeaderView, QAbstractItemView
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from backend.database import Database
from backend.universal_data import CurrentUserdata


class MyTicketsWindow(QWidget):
    request_main_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyTickets")
        self.resize(896, 504)
        self.setMinimumSize(600, 400)

        # Widget bekommt Tabellenraster
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tableview = QTableView() #sorgt für das tabellenartige Aussehen
        self.tableview.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) #Unterbindung editing

        #Tabellenanpassung an Fenstergröße
        self.tableview.resizeColumnsToContents()
        self.tableview.resizeRowsToContents()
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableview.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.backtomain = QPushButton("Back to Main Window")
        self.backtomain.clicked.connect(self.request_main_window.emit)

        layout.addWidget(self.tableview)
        layout.addWidget(self.backtomain)

        user_id = CurrentUserdata.id

        db = Database()
        data = db.get_user_tickets(user_id)
        self.load_table_data(data)

    def load_table_data(self, mysql_data):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ticket number", "time of issuing", "category", "short description", "detailed description"])
        for row in mysql_data:
            items = [QStandardItem(str(field) if field else "") for field in row]
            model.appendRow(items)
        self.tableview.setModel(model)

#todo dummy_id austauschen mit richtiger id
#todo Sortierung überlegen
#todo Spaltenbreite anpassen