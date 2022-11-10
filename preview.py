# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
import cv2
from datetime import datetime
import os

day = datetime.now().strftime("%Y-%m-%d")
running = False


class Thread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    scaled_size = QtCore.QSize(800, 480)

    def run(self):
        global running
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if running:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                 QtGui.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(self.scaled_size, QtCore.Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
            else:
                #아침=0
                if int(datetime.now().strftime("%H")) >= 5 or int(datetime.now().strftime("%H")) <= 10:
                    inum = day + '0'
                #점심=1
                elif int(datetime.now().strftime("%H")) >= 11 or int(datetime.now().strftime("%H")) <= 16:
                    inum = day + '1'
                #저녁=2
                elif int(datetime.now().strftime("%H")) >= 17 or int(datetime.now().strftime("%H")) <= 4:
                    inum = day + '2'

                num = 0
                #만약 이름이 inum(오늘날짜 + 시간) + num(0부터 몇번 째)인 사진 중 num이 0인 사진이 있을 경우 반복
                while os.path.isfile("default_img/" + inum + str(num) + ".jpg"):
                    num = num + 1

                cv2.imwrite("default_img/" + inum + str(num) + ".jpg", frame)
                cap.release()


class PlayStreaming(QtWidgets.QLabel):
    reSize = QtCore.pyqtSignal(QtCore.QSize)

    def __init__(self):
        super(PlayStreaming, self).__init__()
        self.label = QtWidgets.QLabel(self)
        th = Thread(self)
        th.start()
        th.changePixmap.connect(self.setImage)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
