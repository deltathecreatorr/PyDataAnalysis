from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class BackButton(QWidget):
    """
    The Back Button widget.
    """
    
    backClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("backButtonWidget")
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setupButton()

    def setupButton(self):
            """
            Creates the widget for back button.
            """
            
            self.button = QPushButton("\u21d0")
            self.button.setObjectName("BackButton")
            self.button.setFixedSize(40, 40)
            self.button.clicked.connect(self.backClicked.emit)
            self.layout.addWidget(self.button)