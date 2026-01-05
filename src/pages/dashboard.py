from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QDoubleValidator
from api.mpAPI import fetch_data
from PyQt5.QtCore import pyqtSignal, Qt

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
        self.layout.addStretch()

        self.explanationLabel = QLabel("This is the Query Page! Search for materials by their chemical formula. The information retrieved is used to find suitable materials for a photocatalyst.", self)
        self.explanationLabel.setWordWrap(True)
        self.explanationLabel.setObjectName("ExplanationLabel")
        self.layout.addWidget(self.explanationLabel)

        self.instructionLabel = QLabel("Enter a band gap range and formula to find your photocatalyst material", self)
        self.instructionLabel.setObjectName("InstructionLabel")
        self.layout.addWidget(self.instructionLabel)

        sideBySideLayout = QHBoxLayout()

        self.minBandGapLabel = QLineEdit(self)
        self.minBandGapLabel.setObjectName("MinBandGapLabel")
        self.minBandGapLabel.setPlaceholderText("Minimum Band Gap (eV)")
        self.minBandGapLabel.setValidator(QDoubleValidator())
        sideBySideLayout.addWidget(self.minBandGapLabel)

        self.maxBandGapLabel = QLineEdit(self)
        self.maxBandGapLabel.setObjectName("MaxBandGapLabel")
        self.maxBandGapLabel.setPlaceholderText("Maximum Band Gap (eV)")
        self.maxBandGapLabel.setValidator(QDoubleValidator())
        sideBySideLayout.addWidget(self.maxBandGapLabel)

        self.layout.addLayout(sideBySideLayout)

        self.formulaInput = QLineEdit(self)
        self.formulaInput.setObjectName("FormulaInput")
        self.formulaInput.setPlaceholderText("Chemical Formula (e.g., Fe3O4)")
        self.layout.addWidget(self.formulaInput)

        self.findButton = QPushButton("Find Materials", self)
        self.findButton.setObjectName("FindButton")
        self.findButton.setEnabled(False)
        self.findButton.clicked.connect(self.onFindClicked)
        self.layout.addWidget(self.findButton)
        
        self.layout.addStretch()

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
        min_bg_text = self.minBandGapLabel.text()
        max_bg_text = self.maxBandGapLabel.text()

        min_bg = float(min_bg_text) if min_bg_text.strip() else None
        max_bg = float(max_bg_text) if max_bg_text.strip() else None

        if formula.strip():
            materialList = fetch_data(formula, min_band_gap=min_bg, max_band_gap=max_bg)
            if materialList is not None:
                self.materialsFound.emit(materialList)



        