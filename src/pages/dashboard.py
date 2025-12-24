from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class DashboardPage(QWidget):
    backClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("DashboardPage")
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout(self)
