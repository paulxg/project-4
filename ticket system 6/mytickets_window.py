import csv

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMainWindow, QTableView, QWidget, QVBoxLayout, QPushButton
from universal_data import CurrentUserdata,ProgramData
from PyQt6.QtCore import pyqtSignal


class MyTicketsWindow(QWidget):
    request_main_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyTickets")
        self.setFixedSize(400, 400)

        #Widget bekommt Tabellenraster
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.tableview = QTableView()
        self.backmain = QPushButton("Back to Main Window")
        self.backmain.clicked.connect(self.request_main_window.emit)
        layout.addWidget(self.tableview)
        layout.addWidget(self.backmain)

        #model-Variable füllt als QStandardItemModel das Tabellenraster mit Inhalt
        self.model = QStandardItemModel()
        self.tableview.setModel(self.model)

        # 'with' schließt die Datei automatisch, auch bei Fehlern
        with open("tickets.txt", "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=',',quotechar='"')
            for entries in reader:
                if len(entries) >= 1:
                    if entries[0] == CurrentUserdata.id:

                        content_only = entries[1:]

                        items = [QStandardItem(field) for field in content_only]
                        self.model.appendRow(items)
                        self.model.setHorizontalHeaderLabels(ProgramData.myticket_columns)

            self.tableview.resizeColumnsToContents()