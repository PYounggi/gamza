# -*- coding: utf-8 -*-
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from datetime import datetime

class RecordScreen(QDialog):
    def __init__(self):
        super(RecordScreen, self).__init__()
        loadUi("ui/record.ui", self)

        #칼로리, 무게
        day = datetime.now().strftime("%Y-%m-%d")
        if os.path.isfile('json_datas/' + day):
            with open('json_datas/' + day, 'r', encoding='utf-8') as read_file:
                json_data = json.load(read_file)
                #아침
                self.bl_kcal.setText(str(json_data['breakfast'][0]['kcal']) + '(kcal)')
                self.bl_gram.setText(str(json_data['breakfast'][0]['weight']) + '(g)')
                if os.path.isfile('recognize_img/' + day + '0' + '0' + '.jpg'):
                    self.image.setPixmap(QPixmap('recognize_img/' + day + '0' + '0' + '.jpg').scaledToWidth(370).
                                         scaledToHeight(260))
                #점심
                self.lu_kcal.setText(str(json_data['lunch'][0]['kcal']) + '(kcal)')
                self.lu_gram.setText(str(json_data['lunch'][0]['weight']) + '(g)')
                if os.path.isfile('recognize_img/' + day + '1' + '0' + '.jpg'):
                    self.image_2.setPixmap(QPixmap('recognize_img/' + day + '1' + '0' + '.jpg').scaledToWidth(370).
                                           scaledToHeight(260))
                #저녁
                self.di_kcal.setText(str(json_data['dinner'][0]['kcal']) + '(kcal)')
                self.di_gram.setText(str(json_data['dinner'][0]['weight']) + '(g)')
                if os.path.isfile('recognize_img/' + day + '2' + '0' + '.jpg'):
                    self.image_3.setPixmap(QPixmap('recognize_img/' + day + '2' + '0' + '.jpg').scaledToWidth(370).
                                           scaledToHeight(260))

        #캘린더
        #자동으로 오늘 날짜 선택
        self.todayDate = QDate.currentDate()
        self.calendar_widget.setCurrentPage(self.todayDate.year(), self.todayDate.month())

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

        #캘린더 날짜 선택 시 그날 아침 점심 저녁 데이터 가져오기
        #사진, 칼로리, 무게 가져올 예정
        self.calendar_widget.selectionChanged.connect(self.day_data)

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

    #캘린더 클릭 시
    def day_data(self):
        self.day = self.calendar_widget.selectedDate()
        # "년-월-일" 형태의 문자열
        date_str = self.day.toString(Qt.ISODate)

        if os.path.isfile('json_datas/' + date_str):
            with open('json_datas/' + date_str, 'r', encoding='utf-8') as read_file:
                json_data = json.load(read_file)
                self.bl_kcal.setText(str(json_data['breakfast'][0]['kcal']) + '(kcal)')
                self.bl_gram.setText(str(json_data['breakfast'][0]['weight']) + '(g)')

                self.lu_kcal.setText(str(json_data['lunch'][0]['kcal']) + '(kcal)')
                self.lu_gram.setText(str(json_data['lunch'][0]['weight']) + '(g)')

                self.di_kcal.setText(str(json_data['dinner'][0]['kcal']) + '(kcal)')
                self.di_gram.setText(str(json_data['dinner'][0]['weight']) + '(g)')
        else:
            self.bl_kcal.setText("없음")
            self.bl_gram.setText("없음")

            self.lu_kcal.setText("없음")
            self.lu_gram.setText("없음")

            self.di_kcal.setText("없음")
            self.di_gram.setText("없음")

    #뒤로
    def goBack(self):
        self.close()
