import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
from datetime import datetime, date
import pandas
from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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
        self.close()
