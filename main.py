import sys

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets

import base64
import io
from PIL import Image

import requests
import json
import numpy as np
from datetime import datetime, date
import pandas
from dateutil.relativedelta import relativedelta

import preview
import Result
import Record
import Graph

class SplashScreen(QDialog):
    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("ui/splash.ui", self)
        self.image.setPixmap(QPixmap('image/CC.jpg'))
        spl_img = self.image
        clickable(spl_img).connect(self.gotomain)

    def gotomain(self):
        widget.removeWidget(splash)
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("ui/main.ui", self)

        #사물 인식
        self.recognize.clicked.connect(self.goCam)
        #그래프
        self.graph.clicked.connect(self.goGraph)
        #기록
        self.record.clicked.connect(self.goRecord)
        #설정
        self.shutdown.clicked.connect(self.Shutdown)

    def goCam(self):
        widget.addWidget(cam)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goRecord(self):
        self.rcd = Record.RecordScreen()
        self.rcd.setFixedHeight(480)
        self.rcd.setFixedWidth(800)
        self.rcd.move(0, 0)
        # widget.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.rcd.setWindowFlag(Qt.FramelessWindowHint)
        self.rcd.show()

    def goGraph(self):
        self.gph = Graph.GraphScreen()
        self.gph.setFixedHeight(480)
        self.gph.setFixedWidth(800)
        self.gph.move(0, 0)
        # widget.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.gph.setWindowFlag(Qt.FramelessWindowHint)
        self.gph.show()

    def Shutdown(self):
        widget.deleteLater()

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
        self.w = Result.ResultScreen()
        self.w.setFixedHeight(480)
        self.w.setFixedWidth(800)
        self.w.move(0, 0)
        # widget.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.w.setWindowFlag(Qt.FramelessWindowHint)
        self.w.show()
        widget.removeWidget(cam)

    def goBack(self):
        if preview.running == True:
            preview.running = False
            self.display.close()
        widget.removeWidget(cam)

def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True

            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


if __name__ == "__main__" :
    app = QApplication(sys.argv)

    splash = SplashScreen()

    main = MainScreen()
    cam = CameraScreen()

    widget = QtWidgets.QStackedWidget()
    widget.addWidget(splash)
    widget.setFixedHeight(480)
    widget.setFixedWidth(800)
    widget.move(0, 0)
    #widget.setWindowFlags(Qt.WindowStaysOnTopHint)
    widget.setWindowFlag(Qt.FramelessWindowHint)
    widget.show()
    app.exec_()

