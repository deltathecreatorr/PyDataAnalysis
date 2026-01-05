
from PyQt5.QtWidgets import QToolBar, QAction, QMenu, QToolButton

class Toolbar(QToolBar):
    """
    The Custom Toolbar widget that allows the user to go directly to the menu where they can change their api key.
    """
    
    def __init__(self, parent=None):
        super().__init__("MainToolbar", parent)
        self.setObjectName("MainToolbar")
        self.setupActions()

    def setupActions(self):
        """
        Sets up the toolbar individual widgets.
        """
        
        self.file_button = QToolButton(self)
        self.file_button.setText("File")
        self.file_button.setObjectName("FileButton")
        self.file_button.setPopupMode(QToolButton.InstantPopup)

        self.file_menu = QMenu(self.file_button)
        self.file_menu.setObjectName("FileMenu")
        self.file_button.setMenu(self.file_menu)

        self.api_key_action = QAction("Change API Key", self)
        self.api_key_action.setStatusTip("API Key")
        self.api_key_action.triggered.connect(self.api_keyClicked)
        
        self.file_menu.addAction(self.api_key_action)
        
        self.addWidget(self.file_button)

    def api_keyClicked(self):
        """
        Redirects the user to the api key menu.
        """
        
        if self.parent():
            self.parent().showApiKeyPage()