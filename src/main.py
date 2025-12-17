from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import Qt, QSize
import sys

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")

        button = QPushButton("Click Me")

        self.setCentralWidget(button)


app = QApplication(sys.argv)
window = MainMenu()
window.show()

app.exec()