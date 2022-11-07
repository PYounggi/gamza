import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from datetime import datetime

class ResultScreen(QDialog):
    def __init__(self):
        super(ResultScreen, self).__init__()
        loadUi("ui/result.ui", self)

        self.img.setPixmap(QPixmap('recognize_img/test02.jpg').scaledToWidth(600).scaledToHeight(390))
        self.end.clicked.connect(self.goBack)

        day = datetime.now().strftime("%Y-%m-%d")
        with open('json_datas/' + day, 'r', encoding="utf-8") as read_file:
            data = json.load(read_file)

        self.num = 0
        if int(datetime.now().strftime("%H")) >= 17 or int(datetime.now().strftime("%H")) <= 4:
            for i in data['dinner']:
                self.num = self.num + 1
            self.name.setText(str(data['dinner'][self.num-1]['menu']))
            self.kcal.setText(str(data['dinner'][self.num-1]['kcal']))
            self.gram.setText(str(data['dinner'][self.num-1]['weight']))

        elif int(datetime.now().strftime("%H")) >= 5 or int(datetime.now().strftime("%H")) <= 10:
            for j in data['breakfast']:
                self.num = self.num + 1
            self.name.setText(str(data['breakfast'][self.num-1]['menu']))
            self.kcal.setText(str(data['breakfast'][self.num-1]['kcal']))
            self.gram.setText(str(data['breakfast'][self.num-1]['weight']))

        elif int(datetime.now().strftime("%H")) >= 11 or int(datetime.now().strftime("%H")) <= 16:
            for k in data['lunch']:
                self.num = self.num + 1
            self.name.setText(str(data['lunch'][self.num-1]['menu']))
            self.kcal.setText(str(data['lunch'][self.num-1]['kcal']))
            self.gram.setText(str(data['lunch'][self.num-1]['weight']))

    def goBack(self):
        self.close()

