from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from api.database import fetch_data
from PyQt5.QtCore import pyqtSignal

class DashboardPage(QWidget):
    backClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("DashboardPage")
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout(self)
        self.button = QPushButton("fetch data")
        self.button.setObjectName("FetchDataButton")
        self.button.clicked.connect(fetch_data)
        self.layout.addWidget(self.button)



        