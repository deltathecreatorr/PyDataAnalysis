from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from api.mpAPI import fetch_data
from PyQt5.QtCore import pyqtSignal

class DashboardPage(QWidget):
    backClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("DashboardPage")
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout(self)
        self.QLabel = QLabel("Enter a formula for the magnetic material", self)
        self.QLabel.setObjectName("InstructionLabel")
        self.layout.addWidget(self.QLabel)

        self.formulaInput = QLineEdit(self)
        self.formulaInput.setObjectName("FormulaInput")
        self.layout.addWidget(self.formulaInput)

        self.findButton = QPushButton("Find Magnetic Materials", self)
        self.findButton.setObjectName("FindButton")
        self.findButton.clicked.connect(self.onFindClicked)
        self.layout.addWidget(self.findButton)

    def onFindClicked(self):
        formula = self.formulaInput.text()
        fetch_data(formula)



        