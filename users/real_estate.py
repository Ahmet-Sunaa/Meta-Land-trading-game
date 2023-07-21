from PyQt6 import QtCore, QtGui, QtWidgets, uic
import sys

from PyQt6.QtCore import QSize, QObjectCleanupHandler
from PyQt6.QtWidgets import QPushButton

from database import database

from manager.admin_database import database as d
from manager import real_estate as a_real_estate

class MainWindow(QtWidgets.QMainWindow):
    game_area_info = None
    game_area = None
    uid = None
    emlak_id = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./user_windows/emlak.ui", self)
        self.setWindowTitle("Emlak")

        if str(self.uid[0]) == str(self.game_area_info[2]):
            button = QPushButton('Güncelleme Sayfası', self, objectName=str('update'))
            button.clicked.connect(self.update_page)
            button.resize(150, 30)
            button.move(400, 0)
        name = database.get_area_owner(self.game_area_info[0])
        self.business_owner.setText(name)
        salary = database.get_shop_salary(self.game_area_info[0])
        self.daily_salary.setText(salary[0])
        identity = 1
        place_x = 0
        place_y = 100

        for i in range(int(self.game_area)):
            area = d.get_area(identity)
            if area[4] == str(self.uid[0]):
                if identity == 10:
                    place_x += 150
                    place_y = 100
                identity += 1
                continue
            buton_text = area[0] + " " + area[1] + " id:" + str(area[2]) + " " + area[3]
            button = QPushButton(buton_text, self, objectName=str(identity))
            button.clicked.connect(self.get_areas)
            button.resize(150, 30)
            button.move(place_x, place_y)
            place_y += 30
            identity += 1
            if (identity - 1) % 10 == 0:
                place_x += 150
                place_y = 100
        land_info = database.get_owner_land(self.uid[0])
        self.iskur_label = QtWidgets.QLabel('İş kurulabilecek Arsalarınız:', self)
        self.iskur_label.move(400, 50)
        self.iskur_label.resize(200, 20)
        place_x = 400
        place_y = 70
        for i in land_info:
            buton_text = str(i[0])+" id numaralı arsanız"
            button = QPushButton(buton_text, self, objectName=str(int(i[0])*30))
            button.clicked.connect(self.business_button)
            button.resize(150, 30)
            button.move(place_x, place_y)
            place_y += 30


    def get_areas(self, clicked):
        sender = self.sender()
        emlak_satis_kiralik_window.bid = sender.objectName()
        emlak_satis_kiralik_window.uid = self.uid
        emlak_satis_kiralik_window.emlak_id = self.emlak_id
        self.window = emlak_satis_kiralik_window(self)
        self.window.show()


    def business_button(self):
        sender = self.sender()
        build_business_window.uid = self.uid
        build_business_window.bid = str(int(int(sender.objectName())/30))
        self.window = build_business_window(self)
        self.window.show()

    def update_page(self):
        a_real_estate.MainWindow.user = int(self.uid[0])
        a_real_estate.MainWindow.uid = self.game_area_info
        a_real_estate.MainWindow.game_area = self.game_area
        window_shop = a_real_estate.MainWindow(self)
        window_shop.show()

class emlak_satis_kiralik_window(QtWidgets.QMainWindow):
    bid = None
    type_business = None
    uid = None
    emlak_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(QSize(420, 150))
        buy_button = QPushButton('Satın Al', self, objectName='sold')
        buy_button.clicked.connect(self.buy)
        buy_button.resize(75, 30)
        buy_button.move(0, 50)

        rent_button = QPushButton('Kirala', self, objectName='rent')
        rent_button.clicked.connect(self.rent)
        rent_button.resize(75, 30)
        rent_button.move(75, 50)
        self.rent_days = QtWidgets.QLineEdit(self)
        self.rent_days.setText('0')
        self.rent_days.move(150, 50)

        label1 = QtWidgets.QLabel(self)

        label2 = QtWidgets.QLabel(self)
        label2.move(85, 0)

        label3 = QtWidgets.QLabel(self)
        label3.move(0, 25)

        label4 = QtWidgets.QLabel(self)
        label4.move(85, 25)

        label1.setText('Satış Fiyatı: ')

        label3.setText('Kiralama Fiyatı:')

        price = d.get_emlak_rent_sold_price(self.bid)
        self.type_business = price[2]
        if price[2] != '4':
            label2.setText(str(price[0]))
            label4.setText(str(price[1]))
        else:
            QObjectCleanupHandler().add(label3)
            QObjectCleanupHandler().add(label4)
            QObjectCleanupHandler().add(rent_button)
            label2.setText(str(price[0]))
    def buy(self):
        sender = self.sender()
        database.set_rent_sold(self.bid, sender.objectName(), self.uid[0], emlak_id=self.emlak_id)# satın alma tamamlandıı kiralamayı yapppppp Kulanıcının işletme almasını kontrol etttttttttttttttttt

    def rent(self):
        sender = self.sender()
        day = self.rent_days.text()
        cnx=database.connecter()
        cursor = cnx.cursor()
        cursor.execute(
            "select area_users_id from game_area where idgame_area=%s",
            (self.bid,))
        owner = cursor.fetchall()
        database.set_rent_sold(self.bid, sender.objectName(), self.uid[0], days=day, emlak_id=self.emlak_id, owner=owner[0][0])#kirayı halleeeeeeet


class build_business_window(QtWidgets.QMainWindow):
    bid = None
    uid = None
    emlak_id = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(QSize(420, 150))
        buy_button = QPushButton('Satın Al', self, objectName='sold')
        buy_button.clicked.connect(self.buy)
        buy_button.resize(75, 30)
        buy_button.move(0, 50)

        self.groupbox = QtWidgets.QComboBox(self)
        self.groupbox.addItem('emlak')
        self.groupbox.addItem('market')
        self.groupbox.addItem('magaza')
        self.groupbox.activated.connect(self.change_price)
        self.label4 = QtWidgets.QLabel(self)
        self.label4.move(120, 0)
        self.label4.setText(database.get_build_business_price(self.groupbox.currentText()))


    def buy(self):
        sender = self.sender()
        database.set_build_business(self.uid[0], self.bid, self.emlak_id, self.groupbox.currentText(), self.label4.text()) #iş kurma bitti ancak kullanıcının kendi iş yerine bilgi ayarlama getirrrrrrrrrrrrrrrrrr

    def change_price(self):
        self.label4.setText(database.get_build_business_price(self.groupbox.currentText()))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 200)
    window.show()
    app.exec()
