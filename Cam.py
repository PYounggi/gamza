import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2

import preview
import Result

class CameraScreen(QDialog):
    def __init__(self):
        super(CameraScreen, self).__init__()
        loadUi("ui/camera.ui", self)

        self.start.clicked.connect(self.camstart)
        self.stop.clicked.connect(self.camstop)
        self.back.clicked.connect(self.goBack)
        self.recognize.clicked.connect(self.goResult)

    def camstart(self):
        if preview.running == False:
            preview.running = True
            self.display = preview.PlayStreaming()
            self.preview.addWidget(self.display)

    def camstop(self):
        if preview.running == True:
            preview.running = False
            self.display.close()

    def goResult(self):
        if preview.running == True:
            preview.running = False
            self.display.close()
            self.rlt = Result.ResultScreen()
            self.rlt.setFixedHeight(480)
            self.rlt.setFixedWidth(800)
            self.rlt.move(0, 0)
            # widget.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.rlt.setWindowFlag(Qt.FramelessWindowHint)
            self.rlt.show()
            self.close()

    def goBack(self):
        if preview.running == True:
            preview.running = False
            self.display.close()
        self.deleteLater()