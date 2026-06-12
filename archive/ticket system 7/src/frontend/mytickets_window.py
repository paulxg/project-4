from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMainWindow, QTableView, QWidget, QVBoxLayout, QPushButton, QHeaderView, QAbstractItemView
from backend.universal_data import CurrentUserdata, ProgramData
from backend.database import Database
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

        self.tableview = QTableView() #sorgt für das tabellenartige Aussehen
        self.tableview.setWordWrap(True)  # Erlaube Textumbruch in Tabelle

        self.tableview.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) #Unterbindung editing

        self.backtomain = QPushButton("Back to Main Window")
        self.backtomain.clicked.connect(self.request_main_window.emit)

        layout.addWidget(self.tableview)
        layout.addWidget(self.backtomain)

        # model-Variable füllt als QStandardItemModel das Tabellenraster mit Inhalt
        self.model = QStandardItemModel()
        self.tableview.setModel(self.model)

        db = Database()
        tickets = db.get_user_tickets(CurrentUserdata.id)
        for row in tickets:
            items = [QStandardItem(str(field) if field else "") for field in row]
            self.model.appendRow(items)
        self.model.setHorizontalHeaderLabels(ProgramData.myticket_columns)


        header = self.tableview.horizontalHeader()
        column_count = self.model.columnCount()

        if column_count > 0:
            for col in range(column_count - 1):
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

            header.setSectionResizeMode(column_count - 1, QHeaderView.ResizeMode.Stretch)

        self.tableview.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)