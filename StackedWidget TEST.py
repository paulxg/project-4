import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create pages
        self.page1 = QWidget()
        self.page2 = QWidget()

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

        # Set up page 1
        layout1 = QVBoxLayout()
        button1 = QPushButton("Go to Page 2")
        button1.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page2))
        layout1.addWidget(button1)
        self.page1.setLayout(layout1)

        # Set up page 2
        layout2 = QVBoxLayout()
        button2 = QPushButton("Go to Page 1")
        button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout2.addWidget(button2)
        self.page2.setLayout(layout2)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

