from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QListWidget
from PyQt5.QtCore import pyqtSignal, Qt
from components.backButton import BackButton

class MaterialSelectionPage(QWidget):
    backClicked = pyqtSignal()
    materialSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("MaterialSelectionPage")
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout(self)

        topLayout = QHBoxLayout()
        self.backButton = BackButton()
        self.backButton.backClicked.connect(self.backClicked.emit)
        topLayout.addWidget(self.backButton)
        topLayout.addStretch()
        self.layout.addLayout(topLayout)

        self.optionLabel = QLabel("Select the material from the list below. Feel free to confirm with the Materials Project website to ensure it's the right molecule.", self)
        self.optionLabel.setObjectName("OptionLabel")
        self.optionLabel.setWordWrap(True)
        self.optionLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.optionLabel)

        self.materialListWidget = QListWidget(self)
        self.materialListWidget.setObjectName("MaterialListWidget")
        self.materialListWidget.itemClicked.connect(self.onMaterialSelected)
        self.layout.addWidget(self.materialListWidget)

    def updateMaterials(self, materials):
        self.materialListWidget.clear()
        for m_id, data in materials.items():
            formula = data.get('formula_pretty', 'Unknown')
            
            stats = []
            if 'spacegroup_symbol' in data:
                stats.append(f"Spacegroup: {data['spacegroup_symbol']}")
            if 'num_sites' in data:
                stats.append(f"Sites: {data['num_sites']}")
            if 'energy_above_hull' in data and isinstance(data['energy_above_hull'], (int, float)):
                stats.append(f"E_hull: {data['energy_above_hull']:.3f} eV")
            if 'band_gap' in data and isinstance(data['band_gap'], (int, float)):
                stats.append(f"Band Gap: {data['band_gap']:.3f} eV")
            if 'normalized_magnetisation_units' in data:
                stats.append(f"Mag: {data['normalized_magnetisation_units']} µB")
            if 'type' in data:
                stats.append(f"Type: {data['type']}")
            if 'is_magnetic' in data:
                mag_status = "Magnetic" if data['is_magnetic'] else "Non-magnetic"
                stats.append(mag_status)
            
            stats_str = " | ".join(stats)
            display_text = f"{formula} ({m_id})\n{stats_str}"
            self.materialListWidget.addItem(display_text)

    def onMaterialSelected(self, item):
        text = item.text()
        m_id = text.split('(')[-1].strip(')')
        self.materialSelected.emit(m_id)