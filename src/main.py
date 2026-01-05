from PyQt5.QtWidgets import QStackedLayout, QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from components.titlebar import TitleBar
from components.toolbar import Toolbar
from pages.api_key import ApiKeyPage
from pages.dashboard import DashboardPage
from pages.materialSelection import MaterialSelectionPage
from pages.analysis import AnalysisPage
from config import SERVICE_ID, USERNAME
from dotenv import load_dotenv
import sys
import keyring

load_dotenv()

class MainWindow(QMainWindow):
    """
    The Main Window of the program, holds the management of the different windows and menus by hiding menu widgets.
    
    **Arguments**
        *QMainWindow*
            - Main window class from PyQt5.QtWidgets
    **Returns**
        *MainWindow object*
            - The main window object for the program 
    """
    
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Pyalysis")
        
        self.titlebar = TitleBar(self)
        self.setMenuWidget(self.titlebar)

        self.toolbar = Toolbar(self)
        self.addToolBar(self.toolbar)
        self.toolbar.hide()

        self.setupUi()

    def setupUi(self):
        """
        Creates all of the widgets for the start window and holds the widgets for the different menus.
        """
        
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
        self.startButton.clicked.connect(self.checkApiKey)

        self.stackLayout.addWidget(self.homePage)

        self.apiKeyPage = ApiKeyPage()
        self.apiKeyPage.backClicked.connect(self.showHomePage)
        self.apiKeyPage.submitted.connect(self.showDashboardPage)
        self.stackLayout.addWidget(self.apiKeyPage)

        self.dashboardPage = DashboardPage()
        self.dashboardPage.backClicked.connect(self.showHomePage)
        self.dashboardPage.materialsFound.connect(self.showMaterialSelectionPage)
        self.stackLayout.addWidget(self.dashboardPage)

        self.materialSelectionPage = MaterialSelectionPage()
        self.materialSelectionPage.backClicked.connect(self.showDashboardPage)
        self.materialSelectionPage.materialSelected.connect(self.showAnalysisPage)
        self.stackLayout.addWidget(self.materialSelectionPage)

        self.analysisPage = AnalysisPage()
        self.analysisPage.backClicked.connect(self.showMaterialSelectionPage)
        self.stackLayout.addWidget(self.analysisPage)

    def checkApiKey(self):
        """
        Checks if API key is stored and shows either the api key page or the dashboard page after pressing the get started button.
        """
        
        if keyring.get_password(SERVICE_ID, USERNAME):
            print("API Key already stored.")
            self.showDashboardPage()
        else:
            self.toolbar.hide()
            self.stackLayout.setCurrentWidget(self.apiKeyPage)

    def showHomePage(self):
        """
        Shows the start page with the get started button.
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        
        self.toolbar.hide()
        self.stackLayout.setCurrentWidget(self.homePage)

    def showApiKeyPage(self):
        """
        Shows the page where the user has to register their api key if not initialised previously.
        """
        
        self.toolbar.hide()
        self.stackLayout.setCurrentWidget(self.apiKeyPage)
    
    def showDashboardPage(self):
        """
        Shows the dashboard page where the user has to input a chemical formula.
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        
        self.toolbar.show()
        self.stackLayout.setCurrentWidget(self.dashboardPage)

    def showMaterialSelectionPage(self, materialList=None):
        """
        Shows a page where the user has to pick between all the molecules with the formula they inputted.
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        
        self.toolbar.show()
        if materialList:
            self.materialSelectionPage.updateMaterials(materialList)
        self.stackLayout.setCurrentWidget(self.materialSelectionPage)
    
    def showAnalysisPage(self, material_id):
        """
        Shows the page where the user analyses the molecule.
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        
        self.toolbar.show()
        self.analysisPage.setMaterial(material_id)
        self.stackLayout.setCurrentWidget(self.analysisPage)



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