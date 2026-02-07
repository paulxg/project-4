import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow

app = QApplication([])
window = QWidget()

layout = QHBoxLayout()

window.setWindowTitle("Sign in/Sign up")
window.setFixedSize(800,600)
window.setLayout(layout)

signin=QPushButton("Sign in")
signin.setFixedSize(150,150)
signin.setCheckable(True)

signup=QPushButton("Sign up")
signup.setFixedSize(150,150)

layout.addWidget(signin)
layout.addWidget(signup)


window.show()
sys.exit(app.exec())

