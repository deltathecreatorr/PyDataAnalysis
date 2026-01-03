from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget
from components.backButton import BackButton
from api.database import find_record

class AnalysisPage(QWidget):
    backClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("AnalysisPage")
        self.material_id = None
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout(self)
        topLayout = QHBoxLayout()
        self.backButton = BackButton()
        self.backButton.backClicked.connect(self.backClicked.emit)
        topLayout.addWidget(self.backButton)
        topLayout.addStretch()
        self.layout.addLayout(topLayout)

        self.analysisLabel = QLabel("No material selected", self)
        self.analysisLabel.setObjectName("AnalysisLabel")
        self.analysisLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.analysisLabel)

    def setMaterial(self, material_id):
        self.material_id = material_id
        record = find_record(material_id)
        if record:
            self.analysisLabel.setText(f"Analysis for Material ID: {material_id}\nData: {record}")
        else:
            self.analysisLabel.setText(f"Material ID: {material_id} not found in database.")