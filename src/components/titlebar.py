from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtGui


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Title Label
        self.title_label = QLabel("Pyalysis")
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(Qt.AlignCenter)

        #Logo
        self.logo = QLabel(self)
        self.logo.setPixmap(QtGui.QPixmap("src/assets/logo.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Control Buttons
        self.btn_minimize = QPushButton("\u2014")
        self.btn_minimize.setObjectName("btn_minimize")
        self.btn_minimize.clicked.connect(self.minimize_window)

        self.btn_maximize = QPushButton("\u21F1")
        self.btn_maximize.setObjectName("btn_maximize")
        self.btn_maximize.clicked.connect(self.maximize_window)

        self.btn_close = QPushButton("\u2715")
        self.btn_close.setObjectName("btn_close")
        self.btn_close.clicked.connect(self.close_window)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.logo)
        self.layout.addStretch()
        self.layout.addWidget(self.btn_minimize)
        self.layout.addWidget(self.btn_maximize)
        self.layout.addWidget(self.btn_close)

        # Mouse Tracking
        self.start = QPoint(0, 0)
        self.pressing = False

    # Button Actions
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def minimize_window(self):
        self.window().showMinimized()

    def maximize_window(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def close_window(self):
        self.window().close()

    def mouseReleaseEvent(self, event):
        self.pressing = False

    def mouseMoveEvent(self, event):
        if self.pressing:
            end = self.mapToGlobal(event.pos())
            movement = end - self.start
            self.window().setGeometry(self.window().x() + movement.x(),
                                    self.window().y() + movement.y(),
                                    self.window().width(),
                                    self.window().height())
            self.start = end