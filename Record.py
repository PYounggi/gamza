import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class RecordScreen(QDialog):
    def __init__(self):
        super(RecordScreen, self).__init__()
        loadUi("ui/record.ui", self)

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

        #기록_이미지
        self.image.setPixmap(QPixmap('default_img/test.jpg').scaledToWidth(370).scaledToHeight(260))
        self.image_2.setPixmap(QPixmap('default_img/test02.jpg').scaledToWidth(370).scaledToHeight(260))
        self.image_3.setPixmap(QPixmap('default_img/test03.jpg').scaledToWidth(370).scaledToHeight(260))

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
        self.image.setPixmap(QPixmap('recognize_img/test.jpg').scaledToWidth(370).scaledToHeight(260))
        self.image_2.setPixmap(QPixmap('recognize_img/test02.jpg').scaledToWidth(370).scaledToHeight(260))
        self.image_3.setPixmap(QPixmap('recognize_img/test03.jpg').scaledToWidth(370).scaledToHeight(260))

    #뒤로
    def goBack(self):
        self.deleteLater()
