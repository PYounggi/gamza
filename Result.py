# -*- coding: utf-8 -*-
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import os
from PyQt5.QtGui import *
import json
from datetime import datetime

class ResultScreen(QDialog):
    def __init__(self):
        super(ResultScreen, self).__init__()
        loadUi("ui/result.ui", self)
        day = datetime.now().strftime("%Y-%m-%d")

        if int(datetime.now().strftime("%H")) >= 5 and int(datetime.now().strftime("%H")) <= 10:
            inum = day + "0"
        # 점심=1
        elif int(datetime.now().strftime("%H")) >= 11 and int(datetime.now().strftime("%H")) <= 16:
            inum = day + "1"
        # 저녁=2
        elif int(datetime.now().strftime("%H")) >= 17 or int(datetime.now().strftime("%H")) <= 4:
            inum = day + "2"

        num = 0
        #2022-11-08일에 아침 시간때 첫번째 사진 찍을 시 2022-11-0800
        while os.path.isfile('default_img/' + inum + str(num) + '.jpg'):
            if os.path.isfile("recognize_img/" + inum + str(num) + ".jpg"):
                self.img.setPixmap(QPixmap('recognize_img/' + inum + str(num) + '.jpg').scaledToWidth(600)
                                   .scaledToHeight(390))
            else:
                self.img.setPixmap(QPixmap('default_img/' + inum + str(num) + '.jpg').scaledToWidth(600)
                                   .scaledToHeight(390))
                num = num + 1

        self.end.clicked.connect(self.goBack)

        with open('json_datas/' + day, 'r', encoding="utf-8") as read_file:
            data = json.load(read_file)

        self.num = 0

        if int(datetime.now().strftime("%H")) >= 5 and int(datetime.now().strftime("%H")) <= 10:
            for j in data['breakfast']:
                self.num = self.num + 1
            if data['breakfast'] != []:
                self.name.setText(str(data['breakfast'][self.num-1]['menu']))
                self.kcal.setText(str(data['breakfast'][self.num-1]['kcal']))
                self.gram.setText(str(data['breakfast'][self.num-1]['weight']))

        elif int(datetime.now().strftime("%H")) >= 11 and int(datetime.now().strftime("%H")) <= 16:
            for k in data['lunch']:
                self.num = self.num + 1
            if data['lunch'] != []:
                self.name.setText(str(data['lunch'][self.num-1]['menu']))
                self.kcal.setText(str(data['lunch'][self.num-1]['kcal']))
                self.gram.setText(str(data['lunch'][self.num-1]['weight']))

        elif int(datetime.now().strftime("%H")) >= 17 or int(datetime.now().strftime("%H")) <= 4:
            for i in data['dinner']:
                self.num = self.num + 1
            if data['dinner'] != []:
                self.name.setText(str(data['dinner'][self.num - 1]['menu']))
                self.kcal.setText(str(data['dinner'][self.num - 1]['kcal']))
                self.gram.setText(str(data['dinner'][self.num - 1]['weight']))


    def goBack(self):
        self.close()

