import csv

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QTableView, QWidget, QVBoxLayout, QPushButton, QHeaderView, QAbstractItemView
from ..backend.universal_data import ProgramData
from PyQt6.QtCore import pyqtSignal


class AllTicketsWindow(QWidget):
    request_main_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("All Tickets")
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
        self.model = QStandardItemModel() #Inhalt als Modell, der den Inhalt aus csv Datei "im Kopf behält"
        self.tableview.setModel(self.model)

        # 'with' schließt die Datei automatisch, auch bei Fehlern
        with open("../../data/tickets.txt", "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            for entries in reader:
                if len(entries) >= 1:
                    content_only = entries[3:]
                    items = [QStandardItem(field) for field in content_only]
                    self.model.appendRow(items)

            self.model.setHorizontalHeaderLabels(ProgramData.myticket_columns)


        header = self.tableview.horizontalHeader()
        column_count = self.model.columnCount()

        if column_count > 0:
            # 1. Alle Spalten (AUßER der letzten) passen sich eng an den Inhalt an
            for col in range(column_count - 1):
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

            # 2. Die letzte Spalte (langer Text) wird gezwungen, den restlichen Platz
            # auszufüllen und darf NICHT über den Rand hinauswachsen.
            header.setSectionResizeMode(column_count - 1, QHeaderView.ResizeMode.Stretch)

        # 3. Jetzt, wo die Breite der Text-Spalte feststeht, kann die Höhe korrekt umbrechen
        self.tableview.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)