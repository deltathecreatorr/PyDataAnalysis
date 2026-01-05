from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem
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
        """
        
        self.layout = QVBoxLayout(self)

        topLayout = QHBoxLayout()
        self.backButton = BackButton()
        self.backButton.backClicked.connect(self.backClicked.emit)
        topLayout.addWidget(self.backButton)
        topLayout.addStretch()
        self.layout.addLayout(topLayout)

        self.optionLabel = QLabel("Select the material from the list below. Feel free to confirm with the Materials Project website to ensure it's the right molecule. Please note that only materials that have density of state data are listed.", self)
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
            if 'energy_above_hull' in data and isinstance(data['energy_above_hull'], (int, float)):
                stats.append(f"E_hull: {data['energy_above_hull']:.3f} eV")
            if 'band_gap' in data and isinstance(data['band_gap'], (int, float)):
                stats.append(f"Band Gap: {data['band_gap']:.3f} eV")
            
            stats_str = " | ".join(stats)
            display_text = f"{formula} ({m_id})\n{stats_str}"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, m_id)
            self.materialListWidget.addItem(item)

    def onMaterialSelected(self, item):
        """
        Gets the material id from the data dictionary and emits the material id.
        
        **Arguments**
            *item* (QListWidgetItem):
                - The item clicked in the material list widget.
        """
        
        m_id = item.data(Qt.UserRole)
        self.materialSelected.emit(m_id)