import csv

from PyQt6.QtWidgets import (QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel, QComboBox, QFileDialog, QTextEdit,
                             QMessageBox)
from backend.UniversalData import CurrentUserdata,ProgramData
from PyQt6.QtCore import pyqtSignal
from backend.Prioritizing import Prioritizing
from datetime import datetime

class CreateTicket(QWidget):
    request_main_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Ticket")
        self.setFixedSize(550,600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        #Dropdown Menü
        self.dropdown = QComboBox()
        self.dropdown_Items = ProgramData.support_categories
        self.dropdown.addItems(self.dropdown_Items)
        self.category = ""

        # Begrenzung der Anzeige
        self.dropdown.setMaxVisibleItems(5)

        # Label für Dropdown
        self.label = QLabel("I have a problem with:")
        layout.addWidget(self.label)
        layout.addWidget(self.dropdown)

        #Problem-Kurzbeschreibung
        problem_label = QLabel("Describe your problem briefly:")
        self.problem = QLineEdit()
        self.problem.setPlaceholderText("max. 30 characters")
        self.problem.setMaxLength(30)

        layout.addWidget(problem_label)
        layout.addWidget(self.problem)

        #detaillierte Problembeschreibung
        long_problem_label = QLabel("Describe your problem in detail:")
        self.description = QTextEdit()
        self.description.setFixedHeight(125)
        self.description.setPlaceholderText("Max 200 characters")
        layout.addWidget(long_problem_label)
        layout.addWidget(self.description)

        # Character Counter
        self.character_counter = QLabel("0/250")

        # Signal für das Counter-Updating
        self.description.textChanged.connect(self.update_character_counter)

        # Attachment anhängen
        self.attachment_label = QLabel("Attachment:")
        self.attachment_button = QPushButton("Attach")
        layout.addWidget(self.character_counter)

        self.attachment_button.clicked.connect(self.choose_attachment)

        layout.addWidget(self.attachment_label)
        layout.addWidget(self.attachment_button)

        # Submit Button
        self.submit_button = QPushButton("Submit")

        #Layouting des Submit Button
        self.submit_button.setStyleSheet("""
                QPushButton {
                    background-color: #003B00;      
                    color: #FFFFFF;
                }
                QPushButton:hover {
                    background-color: #004200;      
                }
                QPushButton:pressed {
                    background-color: #003B00;      
                }
                """)
        self.submit_button.clicked.connect(self.submit)

        layout.addWidget(self.submit_button)

        # Back to Main Button
        self.backmain = QPushButton("Back to Main Window")
        self.backmain.clicked.connect(self.request_main_window.emit)

        # layouting des Back to Main Button
        self.backmain.setStyleSheet("""
        QPushButton {
            background-color: #3B0000;      
            color: #FFFFFF;
        }
        QPushButton:hover {
            background-color: #420000;      
        }
        QPushButton:pressed {
            background-color: #3B0000;      
        }
        """)

        layout.addWidget(self.backmain)
        self.problem_quick = ""
        self.datetime = ""
        self.factor = ""

        self.final_factor = ""

# Update des Character Counters
    def update_character_counter(self):
        text = self.description.toPlainText()
        length = len(text)
        max_len = 250

        if length >= 230:
            self.character_counter.setStyleSheet("color: orange;")
        if length >= max_len:
            self.character_counter.setStyleSheet("color: red;")
        if length < 230:
            self.character_counter.setStyleSheet("color: white;")

        self.character_counter.setText(f"{length}/{max_len}")

# Funktion des Submit Button
    def submit(self):
        self.category = self.dropdown.currentText()
        self.problem_quick = self.problem.text()
        self.factor = ProgramData.support_categories[self.category]
        self.datetime = datetime.now().strftime("%d/%m/%Y")
        text = self.description.toPlainText()
        text_to_single_line = text.replace("\n", " ").replace("\r", "")
        if len(text_to_single_line) > 250 and self.problem_quick != "":

            #PopUp wenn zu lang und Submitted
            notification = QMessageBox()
            notification.setWindowTitle("Error")
            notification.setText("geht nich, mach kürzer aber füll alles aus! (hab nicht den ganzen Tag Zeit)")
            notification.setIcon(QMessageBox.Icon.Warning)
            notification.exec()

        else:
            Prioritizing.status_calculation(self)
            with open("../tickets.txt", "a", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    CurrentUserdata.id,
                    self.final_factor,
                    self.datetime,
                    self.category,
                    self.problem_quick,
                    text_to_single_line
                    ])

# Inputs in die Textboxen löschen nach dem schreiben (noch im "with")
            inputs1 = self.findChildren(QLineEdit)
            for input_field in inputs1:
                input_field.clear()

            inputs2 = self.findChildren(QTextEdit)
            for input_field in inputs2:
                input_field.clear()
            self.success_notification()

    def success_notification(self):
        success = QMessageBox()
        choice = self.dropdown.currentText()
        success.setWindowTitle("Success")
        success.setText(f"Your Ticket concerning {choice} has been received!")
        success.exec()

    def choose_attachment(self):
        file = QFileDialog.getOpenFileName(self, "Open File", " ",
                                            "All Files ();; Pictures (.png .jpg.jpeg);;PDF (*.pdf)")

        if file:
            self.attachment_label.setText(f"Attachment: {file}")
            print("Attachment: ", file)

