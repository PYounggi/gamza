import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ResultScreen(QDialog):
    def __init__(self):
        super(ResultScreen, self).__init__()
        loadUi("ui/result.ui", self)
        self.img.setPixmap(QPixmap('recognize_img/test02.jpg').scaledToWidth(600).scaledToHeight(390))
        self.end.clicked.connect(self.goBack)

    def goBack(self):
        self.deleteLater()

