from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from api.mpAPI import fetch_data
from PyQt5.QtCore import pyqtSignal

class DashboardPage(QWidget):
    """
    The page where the user enters a chemical formula to be searched for, from either the internal or materials project database.
    
    """
    
    backClicked = pyqtSignal()
    materialsFound = pyqtSignal(dict) # Emitted when materials are found for the given formula

    def __init__(self):
        super().__init__()
        self.setObjectName("DashboardPage")
        self.setupUi()

    def setupUi(self):
        """
        Sets up the UI for the dashboard page
        """
        
        self.layout = QVBoxLayout(self)

        self.explanationLabel = QLabel("This is the Query Page! Search up magnetic materials by their chemical formula. The information retrieved is used to find suitable materials for a magnetic data storage drive.", self)
        self.explanationLabel.setWordWrap(True)
        self.explanationLabel.setObjectName("ExplanationLabel")
        self.layout.addWidget(self.explanationLabel)

        self.instructionLabel = QLabel("Enter a formula to find your magnetic material, for example, Fe3O4.", self)
        self.instructionLabel.setObjectName("InstructionLabel")
        self.layout.addWidget(self.instructionLabel)

        self.formulaInput = QLineEdit(self)
        self.formulaInput.setObjectName("FormulaInput")
        self.layout.addWidget(self.formulaInput)

        self.findButton = QPushButton("Find Magnetic Materials", self)
        self.findButton.setObjectName("FindButton")
        self.findButton.setEnabled(False)
        self.findButton.clicked.connect(self.onFindClicked)
        self.layout.addWidget(self.findButton)

        self.formulaInput.textChanged.connect(self.onTextChanged)

    def onTextChanged(self, text):
        """
        Checks if the chemical formula input is empty so that the user cant search for an empty formula.
        """
        
        if text.strip():
            self.findButton.setEnabled(True)
        else:
            self.findButton.setEnabled(False)

    def onFindClicked(self):
        """
        Strips the formula input and fetches the data from either the local database or the materials project API.
        """
        
        formula = self.formulaInput.text()
        if formula.strip():
            materialList = fetch_data(formula)
            if materialList is not None:
                self.materialsFound.emit(materialList)



        