from PyQt5.QtWidgets import QStackedLayout, QApplication, QMainWindow, QLabel, QToolBar, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from components.titlebar import TitleBar
from pages.api_key import ApiKeyPage
from pages.dashboard import DashboardPage
from config import SERVICE_ID, USERNAME
from dotenv import load_dotenv
import sys
import keyring

load_dotenv()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Pyalysis")
        
        self.titlebar = TitleBar(self)
        self.setMenuWidget(self.titlebar)

        self.setupUi()

    def setupUi(self):
        self.toolbar = QToolBar("MainToolbar")
        self.toolbar.setObjectName("MainToolbar")
        self.addToolBar(self.toolbar)

        self.centralWidget = QWidget()
        self.centralWidget.setObjectName("CentralWidget")
        self.setCentralWidget(self.centralWidget)

        pageLayout = QVBoxLayout(self.centralWidget)
        self.stackLayout = QStackedLayout()
        pageLayout.addLayout(self.stackLayout)

        # Home Page
        self.homePage = QWidget()
        self.homePageLayout = QVBoxLayout(self.homePage)
        self.homePageLayout.setAlignment(Qt.AlignCenter)

        self.titleContainer = QWidget()
        self.titleContainer.setObjectName("TitleContainer")
        self.titleLayout = QHBoxLayout(self.titleContainer)
        self.titleLayout.setAlignment(Qt.AlignCenter)

        self.logoLabel = QLabel()
        self.logoLabel.setObjectName("LogoLabel")
        pixmap = QPixmap("src/assets/logo.png").scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logoLabel.setPixmap(pixmap)

        self.contentLabel = QLabel("Pyalysis")
        self.contentLabel.setObjectName("ContentLabel")
        self.contentLabel.setAlignment(Qt.AlignCenter)

        self.titleLayout.addWidget(self.logoLabel)
        self.titleLayout.addWidget(self.contentLabel)

        self.homePageLayout.addWidget(self.titleContainer)

        self.startButton = QPushButton("Get Started")
        self.startButton.setFixedSize(300, 50)
        self.startButton.setObjectName("StartButton")
        self.homePageLayout.addWidget(self.startButton, alignment=Qt.AlignCenter)
        self.startButton.clicked.connect(self.showGetStartedPage)

        self.stackLayout.addWidget(self.homePage)

        self.apiKeyPage = ApiKeyPage()
        self.apiKeyPage.backClicked.connect(self.showHomePage)
        self.apiKeyPage.submitted.connect(self.showDashboardPage)
        self.stackLayout.addWidget(self.apiKeyPage)

        self.dashboardPage = DashboardPage()
        self.dashboardPage.backClicked.connect(self.showHomePage)
        self.stackLayout.addWidget(self.dashboardPage)

    def showGetStartedPage(self):
        if keyring.get_password(SERVICE_ID, USERNAME):
            print("API Key already stored.")
            self.showDashboardPage()
        else:

            self.stackLayout.setCurrentWidget(self.apiKeyPage)

    def showHomePage(self):
        self.stackLayout.setCurrentWidget(self.homePage)
    
    def showDashboardPage(self):
        self.stackLayout.setCurrentWidget(self.dashboardPage)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("src/stylesheets/styles.qss", 'r') as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Stylesheet not found")
        
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())