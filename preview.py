from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import cv2

running = False

class Thread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    scaled_size = QtCore.QSize(800, 480)

    def run(self):
        global running
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if running == True:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QtGui.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(self.scaled_size, QtCore.Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                cv2.imwrite("./recognize_img/test02.jpg", frame)
            if running == False:
                cap.release()

class PlayStreaming(QtWidgets.QLabel):
    reSize = QtCore.pyqtSignal(QtCore.QSize)

    def __init__(self):
        super(PlayStreaming, self).__init__()
        # create a label
        self.label = QtWidgets.QLabel(self)
        th = Thread(self)
        th.start()
        th.changePixmap.connect(self.setImage)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        if running == False:
            th.quit()

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
