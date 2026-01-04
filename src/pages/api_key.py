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
        self.setupOffline()

    def setupUi(self):
        """
        Sets up the widgets for the Ui.
        
        Keyword arguments:
        argument -- description
        Return: return_description
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

    def setupOffline(self):
        """
        Sets up the widgets for the UI, where the user can confirm they want only ues the local database.
        """
        
        self.offlineLabel = QLabel("You can also use Pyalysis in offline mode without an API key. This will mean that only materials previously fetched will be accessible. This is not recommended if you are using Pyalysis for the first time.")
        self.offlineLabel.setWordWrap(True)
        self.offlineLabel.setObjectName("OfflineLabel")
        self.offlineLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.offlineLabel)

        self.offlineButton = QPushButton("Continue Offline")
        self.offlineButton.setObjectName("OfflineButton")
        self.offlineButton.setFixedWidth(150)
        self.layout.addWidget(self.offlineButton, alignment=Qt.AlignCenter)

        self.layout.addStretch()

    def getApiKey(self):
        """
        Uses the user's credential manager to store the api key for the program, so the user does not need to re-enter the api key every time the program is opened.
        """
        
        api_key = self.apiKeyInput.text()
        keyring.set_password(SERVICE_ID, USERNAME, api_key)
        self.submitted.emit()