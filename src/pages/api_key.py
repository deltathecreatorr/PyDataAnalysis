from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from components.backButton import BackButton
from config import SERVICE_ID, USERNAME
import keyring


class ApiKeyPage(QWidget):
    """
    The page where the user enters the api key or confirms they want to only use the local database with the system.
    """
    
    backClicked = pyqtSignal()
    submitted = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("apiKeyPage")
        self.setupUi()

    def setupUi(self):
        """
        Sets up the widgets for the UI.
        """
        
        self.layout = QVBoxLayout(self)

        # Top bar with back button
        topLayout = QHBoxLayout()
        self.backButton = BackButton()
        self.backButton.backClicked.connect(self.backClicked.emit)
        topLayout.addWidget(self.backButton)
        topLayout.addStretch()
        self.layout.addLayout(topLayout)

        self.layout.addStretch()

        centerLayout = QVBoxLayout()
        centerLayout.setAlignment(Qt.AlignCenter)
        centerLayout.setSpacing(20)

        self.label = QLabel("Enter Your API Key from the Materials Project Dashboard")
        self.label.setObjectName("ApiKeyLabel")
        self.label.setAlignment(Qt.AlignCenter)
        centerLayout.addWidget(self.label)

        self.apiKeyInput = QLineEdit()
        self.apiKeyInput.setPlaceholderText("API Key")
        self.apiKeyInput.setObjectName("ApiKeyInput")
        self.apiKeyInput.setFixedWidth(300)
        centerLayout.addWidget(self.apiKeyInput, alignment=Qt.AlignCenter)

        self.submitButton = QPushButton("Submit")
        self.submitButton.setObjectName("SubmitButton")
        self.submitButton.setFixedWidth(100)
        centerLayout.addWidget(self.submitButton, alignment=Qt.AlignCenter)
        self.submitButton.clicked.connect(self.getApiKey)

        self.layout.addLayout(centerLayout)
        self.layout.addStretch()

    def getApiKey(self):
        """
        Uses the user's credential manager to store the api key for the program, so the user does not need to re-enter the api key every time the program is opened.
        """
        
        api_key = self.apiKeyInput.text()
        keyring.set_password(SERVICE_ID, USERNAME, api_key)
        self.submitted.emit()