from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QListWidget
from PyQt5.QtCore import pyqtSignal, Qt
from components.backButton import BackButton

class MaterialSelectionPage(QWidget):
    """
    The page where the user has to select the right molecule from the materials with the given formula.
    """
    
    backClicked = pyqtSignal()
    materialSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("MaterialSelectionPage")
        self.setupUi()

    def setupUi(self):
        """
        Sets up all the widget for the UI, and handles all the information from the database.
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        
        self.layout = QVBoxLayout(self)

        topLayout = QHBoxLayout()
        self.backButton = BackButton()
        self.backButton.backClicked.connect(self.backClicked.emit)
        topLayout.addWidget(self.backButton)
        topLayout.addStretch()
        self.layout.addLayout(topLayout)

        self.optionLabel = QLabel("Select the material from the list below. Feel free to confirm with the Materials Project website to ensure it's the right molecule. Please note that only ferromagnetic and ferrimagnetic materials are listed, as only those types are suitable for data storage.", self)
        self.optionLabel.setObjectName("OptionLabel")
        self.optionLabel.setWordWrap(True)
        self.optionLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.optionLabel)

        self.materialListWidget = QListWidget(self)
        self.materialListWidget.setObjectName("MaterialListWidget")
        self.materialListWidget.itemClicked.connect(self.onMaterialSelected)
        self.layout.addWidget(self.materialListWidget)

    def updateMaterials(self, materials):
        """
        Handles the labels for the data from the database.
        
        **Arguments**
            *Materials* (dict):
                - The materials data fetched from the database. Stored as a dictionary with material IDs as keys and their data as values.
        """
        
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
            
            stats_str = " | ".join(stats)
            display_text = f"{formula} ({m_id})\n{stats_str}"
            self.materialListWidget.addItem(display_text)

    def onMaterialSelected(self, item):
        """
        Gets the material id from the data dictionary and emits the material id.
        
        **Arguments**
            *item* (QListWidgetItem):
                - The item clicked in the material list widget.
        """
        
        text = item.text()
        m_id = text.split('(')[-1].strip(')')
        self.materialSelected.emit(m_id)