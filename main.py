import sys

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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
        widget.addWidget(record)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goGraph(self):
        widget.addWidget(grap)
        widget.setCurrentIndex(widget.currentIndex() + 1)

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
        self.w.show()
        widget.removeWidget(cam)

    def goBack(self):
        if preview.running == True:
            preview.running = False
            self.display.close()
        widget.removeWidget(cam)


class GraphScreen(QDialog):
    def __init__(self):
        super(GraphScreen, self).__init__()
        loadUi('ui/graph.ui', self)

        # 현재 날짜와 시간 저장
        my_date = datetime.today()
        # 6일전 날짜와 시간 저장
        lw_date = my_date + relativedelta(days=-9)
        # 오늘날짜만 저장
        today = date.today().isoformat()
        # 오늘부터 ~ 9일 전 날짜 리스트에 저장
        dates = self.date_range(lw_date.date().isoformat(), today)

        #그래프 그리기
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        #위젯 추가
        self.graph_verticalLayout.addWidget(self.canvas)
        #x축 범위
        x = np.arange(10)
        #값(y축)
        kcal = np.random.randint(low=800, high=3000, size=10) #임시 값

        avg_kcal = sum(kcal) / 10
        max_kcal = max(kcal)
        min_kcal = min(kcal)


        axes = self.fig.add_subplot(111)
        axes.bar(x, kcal)
        axes.set_xticks(x, dates)
        axes.set_title("10days kcal")
        self.canvas.draw()

        self.Avg_num.setText(str(int(avg_kcal)) + " (kcal)")
        self.Max_num.setText(str(int(max_kcal)) + " (kcal)")
        self.Min_num.setText(str(int(min_kcal)) + " (kcal)")

        #성공,실패
        styleSheet_suc = """
                        QFrame{
                        	border-radius: 70px;
                        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgb(255, 128, 0), stop:{STOP_2} rgba(204, 204, 204, 100));
                        }
                        """

        styleSheet_fail = """
                QFrame{
                	border-radius: 70px;
                	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(204, 204, 204, 100), stop:{STOP_2} rgb(85, 170, 255));
                }
                """

        progress = 1
        value = 100

        for i in kcal:
            if i <= 2000:
                progress = progress - 0.1
                value = value - 10

        progress = round(progress, 3)

        suc_1 = str(1-progress)
        suc_2 = str(1-progress-0.003)
        fail_1 = str(progress)
        fail_2 = str(progress-0.003)

        newStylesheet_suc = styleSheet_suc.replace("{STOP_1}", suc_1).replace("{STOP_2}", suc_2)
        newStylesheet_fail = styleSheet_fail.replace("{STOP_1}", fail_1).replace("{STOP_2}", fail_2)
        self.circularProgressSuc.setStyleSheet(newStylesheet_suc)
        self.circularProgressFail.setStyleSheet(newStylesheet_fail)

        # 숫자
        htmlText = """<p align="center"><span style=" font-size:24pt;">{VALUE}</span><span style=" font-size:20pt; vertical-align:super;">%</span></p>"""
        self.labelPercentageFail.setText(htmlText.replace("{VALUE}", str(int(value))))
        self.labelPercentageSuc.setText(htmlText.replace("{VALUE}", str(int(100-value))))

        #뒤로가기
        self.back.clicked.connect(self.goBack)

    #최근 일주일 날짜 저장(9일 전부터 오늘까지)
    def date_range(self, start, end):
        start = datetime.strptime(start, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")
        dates = [date.strftime('%d') for date in pandas.date_range(start, periods=(end-start).days+1)]
        return dates

    def goBack(self):
        widget.removeWidget(grap)

class RecordScreen(QDialog):
    def __init__(self):
        super(RecordScreen, self).__init__()
        loadUi("ui/record.ui", self)

        #캘린더
        #자동으로 오늘 날짜 선택
        self.todayDate = QDate.currentDate()
        self.calendar.setCurrentPage(self.todayDate.year(), self.todayDate.month())

        #캘린더 날짜 선택 시 그날 아침 점심 저녁 데이터 가져오기
        #사진, 칼로리, 무게 가져올 예정
        #self.calendar.clicked.connect(self.tday_img)

        #아침(breakfast)
        self.pushButton1_1.clicked.connect(self.page_btn_1)
        self.pushButton1_2.clicked.connect(self.page_btn_2)
        self.pushButton1_3.clicked.connect(self.page_btn_3)
        #점심(lunch)
        self.pushButton2_1.clicked.connect(self.page_btn_1)
        self.pushButton2_2.clicked.connect(self.page_btn_2)
        self.pushButton2_3.clicked.connect(self.page_btn_3)
        #저녁(dinner)
        self.pushButton3_1.clicked.connect(self.page_btn_1)
        self.pushButton3_2.clicked.connect(self.page_btn_2)
        self.pushButton3_3.clicked.connect(self.page_btn_3)

        #기록_이미지
        # self.img = self.img.scaledToWidth(370)
        # self.img = self.img.scaledToHeight(260)
        # self.image.setPixmap(self.img)

        #뒤로가기
        self.back.clicked.connect(self.goBack)

    #아침
    def page_btn_1(self):
        self.stack.setCurrentIndex(0)

    #점심
    def page_btn_2(self):
        self.stack.setCurrentIndex(1)

    #저녁
    def page_btn_3(self):
        self.stack.setCurrentIndex(2)

    #뒤로
    def goBack(self):
        widget.removeWidget(record)


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
    grap = GraphScreen()
    record = RecordScreen()

    widget = QtWidgets.QStackedWidget()
    widget.addWidget(splash)
    widget.setFixedHeight(480)
    widget.setFixedWidth(800)
    widget.move(0, 0)
    #widget.setWindowFlags(Qt.WindowStaysOnTopHint)
    widget.setWindowFlag(Qt.FramelessWindowHint)
    widget.show()
    app.exec_()

