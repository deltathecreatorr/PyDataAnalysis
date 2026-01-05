from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from components.backButton import BackButton
from api.database import find_record
from api.mpAPI import fetch_dos
import numpy as np
import json
from scipy.constants import h, c, e

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

        self.materialTitleLabel = QLabel("No material selected", self)
        self.materialTitleLabel.setObjectName("MaterialTitleLabel")
        self.materialTitleLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.materialTitleLabel)

        infoLayout = QVBoxLayout()
        infoLayout.setSpacing(5) 
        infoLayout.addStretch()   
        
        self.bandGapLabel = QLabel("", self)
        self.bandGapLabel.setWordWrap(True)
        self.bandGapLabel.setObjectName("BandGapLabel")
        self.bandGapLabel.setAlignment(Qt.AlignCenter)

        self.energyAHLabel = QLabel("", self)
        self.energyAHLabel.setWordWrap(True)
        self.energyAHLabel.setObjectName("EnergyAHLabel")
        self.energyAHLabel.setAlignment(Qt.AlignCenter)

        self.wavelengthLabel = QLabel("", self)
        self.wavelengthLabel.setWordWrap(True)
        self.wavelengthLabel.setObjectName("WavelengthLabel")
        self.wavelengthLabel.setAlignment(Qt.AlignCenter)

        self.cbmLabel = QLabel("", self)
        self.cbmLabel.setWordWrap(True)
        self.cbmLabel.setObjectName("CBMLabel")
        self.cbmLabel.setAlignment(Qt.AlignCenter)

        self.vbmLabel = QLabel("", self)
        self.vbmLabel.setWordWrap(True)
        self.vbmLabel.setObjectName("VBMLabel")
        self.vbmLabel.setAlignment(Qt.AlignCenter)
    

        self.disclaimerLabel = QLabel("Disclaimer: The Materials Project uses DFT to calculate the band gap, which is known to underestimate values, compared to experimental ones.", self)
        self.disclaimerLabel.setObjectName("DisclaimerLabel")
        self.disclaimerLabel.setWordWrap(True)
        self.disclaimerLabel.setAlignment(Qt.AlignCenter)
        
        infoLayout.addWidget(self.wavelengthLabel)
        infoLayout.addWidget(self.bandGapLabel)
        infoLayout.addWidget(self.energyAHLabel)
        infoLayout.addWidget(self.cbmLabel)
        infoLayout.addWidget(self.vbmLabel)
        infoLayout.addStretch()   

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addLayout(infoLayout)

        self.plotLayout = QVBoxLayout()
        horizontalLayout.addLayout(self.plotLayout)
        self.layout.addLayout(horizontalLayout)
        self.layout.addWidget(self.disclaimerLabel)

    def setMaterial(self, material_id):
        self.material_id = material_id
        record_str = find_record(material_id)
        
        self.clearPlot()

        if record_str:
            try:
                record = json.loads(record_str)
                formula = record.get('formula_pretty', 'Unknown Formula')
                bandGap = record.get('band_gap', 'N/A')
                energyAH = record.get('energy_above_hull', 'N/A')
                cbm = record.get('cbm', 'N/A')
                vbm = record.get('vbm', 'N/A')

                self.bandGapLabel.setText(f"Band Gap: {bandGap} eV")
                self.energyAHLabel.setText(f"Energy Above Hull: {energyAH} eV")
                self.materialTitleLabel.setText(f"Analysis for {formula} (ID: {material_id})")
                self.cbmLabel.setText(f"Conduction Band Minimum (CBM): {cbm} eV")
                self.vbmLabel.setText(f"Valence Band Maximum (VBM): {vbm} eV")

                wavelength = self.calculate_wavelength(bandGap)
                if 380 <= wavelength <= 750:
                    self.wavelengthLabel.setText(f"Wavelength: {wavelength:.2f} nm. This material can utilize visible light.")
                elif wavelength > 750:
                    self.wavelengthLabel.setText(f"Wavelength: {wavelength:.2f} nm. This material utilizes infrared light.")
                elif 0 < wavelength < 380:
                    self.wavelengthLabel.setText(f"Wavelength: {wavelength:.2f} nm. This material utilizes ultraviolet light.")
                else:
                    self.wavelengthLabel.setText("Wavelength: N/A")
            except json.JSONDecodeError:
                self.materialTitleLabel.setText(f"Analysis for ID: {material_id} (Error parsing data)")
            
            dos_data = fetch_dos(material_id)
            if dos_data:
                self.plotDOS(dos_data)
            else:
                current_text = self.materialTitleLabel.text()
                self.materialTitleLabel.setText(f"{current_text}\nNo DOS Data available.")
        else:
            self.materialTitleLabel.setText(f"Material ID: {material_id} not found in database.")

    def clearPlot(self):
        while self.plotLayout.count():
            child = self.plotLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def plotDOS(self, dos_data):
        energies = np.array(dos_data['energies'])
        efermi = dos_data['efermi']
        adjusted_energies = energies - efermi
        
        densities = dos_data['densities']
 
        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas.updateGeometry()
        
        ax = fig.add_subplot(111)
        
        if '1' in densities:
            ax.plot(adjusted_energies, densities['1'], color='teal', label='Spin Up')
       
        if '-1' in densities:
            ax.plot(adjusted_energies, [-d for d in densities['-1']], color='orange', label='Spin Down')

        ax.set_xlabel('Energy (eV) relative to Fermi Level')
        ax.set_ylabel('Density of States')
        ax.set_title(f'Electronic Structure: {self.material_id}')
        ax.axvline(x=0, color='red', linestyle='--', alpha=0.7, label="Fermi Level")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Set dark theme colors
        fig.patch.set_facecolor('#1d2d44')
        ax.set_facecolor('#2b4257')
        
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        for spine in ax.spines.values():
            spine.set_color('white')

        fig.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.9)
        
        self.plotLayout.addWidget(canvas)

    def calculate_wavelength(self, eV):
        """
        Converts energy in electron volts into wavelength to see what spectrum of light the photocatalyst uses
        **Arguments**
            *eV* (float):
                - The energy in electron volts to convert to wavelength.
        **Returns**
            *float*:
                - The wavelength in nanometers.
        """
        if eV <= 0:
            return 0
        wavelength_m = (h * c) / (eV * e)  # Wavelength in meters
        wavelength_nm = wavelength_m * 1e9  # Convert to nanometers
        return wavelength_nm