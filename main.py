# -*- coding: utf-8 -*-
import sys

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets

import requests
import json
import numpy as np

import Record
import Graph
import Cam

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
        self.cam = Cam.CameraScreen()
        self.cam.setFixedHeight(480)
        self.cam.setFixedWidth(800)
        self.cam.move(0, 0)
        # widget.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.cam.setWindowFlag(Qt.FramelessWindowHint)
        self.cam.show()

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
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(splash)
    widget.setFixedHeight(480)
    widget.setFixedWidth(800)
    widget.move(0, 0)
    #widget.setWindowFlags(Qt.WindowStaysOnTopHint)
    widget.setWindowFlag(Qt.FramelessWindowHint)
    widget.show()
    app.exec_()

