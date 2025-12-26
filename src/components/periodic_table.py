from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

elements_positions = {
    'H': (0, 0), 'He': (0, 17),
    'Li': (1, 0), 'Be': (1, 1), 'B': (1, 12), 'C': (1, 13), 'N': (1, 14), 'O': (1, 15), 'F': (1, 16), 'Ne': (1, 17),
    'Na': (2, 0), 'Mg': (2, 1), 'Al': (2, 12), 'Si': (2, 13), 'P': (2, 14), 'S': (2, 15), 'Cl': (2, 16), 'Ar': (2, 17),
    'K': (3, 0), 'Ca': (3, 1), 'Sc': (3, 2), 'Ti': (3, 3), 'V': (3, 4), 'Cr': (3, 5), 'Mn': (3, 6), 'Fe': (3, 7), 'Co': (3, 8), 'Ni': (3, 9), 'Cu': (3, 10), 'Zn': (3, 11), 'Ga': (3, 12), 'Ge': (3, 13), 'As': (3, 14), 'Se': (3, 15), 'Br': (3, 16), 'Kr': (3, 17),
    'Rb': (4, 0), 'Sr': (4, 1), 'Y': (4, 2), 'Zr': (4, 3), 'Nb': (4, 4), 'Mo': (4, 5), 'Tc': (4, 6), 'Ru': (4, 7), 'Rh': (4, 8), 'Pd': (4, 9), 'Ag': (4, 10), 'Cd': (4, 11), 'In': (4, 12), 'Sn': (4, 13), 'Sb': (4, 14), 'Te': (4, 15), 'I': (4, 16), 'Xe': (4, 17),
    'Cs': (5, 0), 'Ba': (5, 1), 'La': (5, 2), 'Ce': (8, 3), 'Pr': (8, 4), 'Nd': (8, 5), 'Pm': (8, 6), 'Sm': (8, 7), 'Eu': (8, 8), 'Gd': (8, 9), 'Tb': (8, 10), 'Dy': (8, 11), 'Ho': (8, 12), 'Er': (8, 13), 'Tm': (8, 14), 'Yb': (8, 15), 'Lu': (5, 15),
    'Hf': (6, 3), 'Ta': (6, 4), 'W': (6, 5), 'Re': (6, 6), 'Os': (6, 7), 'Ir': (6, 8), 'Pt': (6, 9), 'Au': (6, 10), 'Hg': (6, 11), 'Tl': (6, 12), 'Pb': (6, 13), 'Bi': (6, 14), 'Po': (6, 15), 'At': (6, 16), 'Rn': (6, 17),
    'Fr': (7, 0), 'Ra': (7, 1), 'Ac': (7, 2), 'Th': (7, 3), 'Pa': (7, 4), 'U': (7, 5), 'Np': (7, 6), 'Pu': (7, 7), 'Am': (7, 8), 'Cm': (7, 9), 'Bk': (7, 10), 'Cf': (7, 11), 'Es': (7, 12), 'Fm': (7, 13), 'Md': (7, 14), 'No': (7, 15), 'Lr': (7, 16), 'Rf': (7, 17),
    'Db': (8, 2), 'Sg': (8, 10), 'Bh': (8, 11), 'Hs': (8, 16), 'Mt': (8, 17), 'Ds': (9, 2), 'Rg': (9, 10), 'Cn': (9, 11), 'Nh': (9, 16), 'Fl': (9, 17), 'Mc': (10, 2), 'Lv': (10, 10), 'Ts': (10, 11), 'Og': (10, 16)
}

class Element(QWidget):
    def __init__(self, symbol, name, atomic_number):
        super().__init__()
        self.setObjectName("Element")
        self.symbol = symbol
        self.name = name
        self.atomic_number = atomic_number
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout(self)

class PeriodicTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("PeriodicTable")
        self.setupUi()

    def setupUi(self):
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.selectedElement = []
        self.buttons = {}

