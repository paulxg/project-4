import csv

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QTableView, QWidget, QVBoxLayout, QPushButton, QHeaderView, QAbstractItemView
from backend.universal_data import ProgramData
from PyQt6.QtCore import pyqtSignal
from backend.database import Database


class AllTicketsWindow(QWidget):
    request_main_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        print("AllTicketsWindow")
        self.setWindowTitle("All Tickets")
        self.resize(896, 504)
        self.setMinimumSize(600, 400)

        # Widget bekommt Tabellenraster
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tableview = QTableView() #sorgt für das tabellenartige Aussehen
        self.tableview.setWordWrap(True)  # Erlaube Textumbruch in Tabelle

        self.tableview.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) #Unterbindung editing

        self.backtomain = QPushButton("Back to Main Window")
        self.backtomain.clicked.connect(self.request_main_window.emit)

        layout.addWidget(self.tableview)
        layout.addWidget(self.backtomain)

        db = Database()
        data = db.get_all_tickets()
        self.load_table_data(data)

    def load_table_data(self, mysql_data):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(
            ["ticket number", "time of issuing", "category", "short description", "detailed description"])
        for row in mysql_data:
            items = [QStandardItem(str(field) if field else "") for field in row]
            model.appendRow(items)
        self.tableview.setModel(model)