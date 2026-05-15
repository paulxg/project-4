from PyQt6.QtWidgets import QTableView, QWidget, QVBoxLayout, QPushButton, QHeaderView, QAbstractItemView, QHBoxLayout, \
    QLineEdit
from PyQt6.QtCore import pyqtSignal
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
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tableview = QTableView() #sorgt für das tabellenartige Aussehen
        self.tableview.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) #Unterbindung editing

        #Tabellenanpassung an Fenstergröße
        self.tableview.resizeColumnsToContents()
        self.tableview.resizeRowsToContents()
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableview.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.backtomain = QPushButton("Back to Main Window")
        self.backtomain.clicked.connect(self.request_main_window.emit)

        self.layout.addWidget(self.tableview)
        self.layout.addWidget(self.backtomain)

        user_id = CurrentUserdata.id

        self.db = Database()
        data = self.db.get_user_tickets(user_id)
        self.load_table_data(data)
        self.check_rank()

    def check_rank(self):
        if CurrentUserdata.rank == "admin":
            self.admin_features()

    def load_table_data(self, mysql_data):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ticket number", "time of issuing", "category", "short description", "detailed description"])
        for row in mysql_data:
            items = [QStandardItem(str(field) if field else "") for field in row]
            model.appendRow(items)
        self.tableview.setModel(model)

    def admin_features(self):
        editing_layout = QHBoxLayout()

        ticket_number_button = QLineEdit("Ticket number to be edited") #todo Text ausgrauen
        delete_button = QPushButton("Delete Ticket")

        ticket_number = ticket_number_button.text()

        print("jetzt delete methode aufrufen")
        #delete = self.db.delete_ticket(ticket_number)
        print("jetzt delete methode aufrufen")
        #delete_button.clicked.connect(delete)

        editing_layout.addWidget(ticket_number_button)
        editing_layout.addWidget(delete_button)
        self.layout.addLayout(editing_layout)
        #User functions