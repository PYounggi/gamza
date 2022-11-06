from PyQt5 import QtCore, QtGui, QtWidgets
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
            if running:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QtGui.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(self.scaled_size, QtCore.Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
            else:
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

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
