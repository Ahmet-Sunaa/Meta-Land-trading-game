from PyQt6 import QtCore, QtGui, QtWidgets, uic
import sys

from PyQt6.QtCore import QObjectCleanupHandler
from PyQt6.QtWidgets import QPushButton

from manager.admin_database import database

class MainWindow(QtWidgets.QMainWindow):
    uid = None
    game_area = None
    user = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./admin_windows/emlak.ui", self)
        self.setWindowTitle("Emlak")
        owner_data = database.get_area_owner(self.uid[2])
        name = owner_data[0][0] + " " + owner_data[0][1]
        self.owner.setText(name)
        owner_data = database.get_cost(self.uid[2], self.uid[0])
        self.salary.setText(str(owner_data[0][0]))
        commission = database.get_emlak_commission(self.uid[0])
        self.sold_commission.setText(commission[0])
        self.rent_commission.setText(commission[1])
        print(owner_data)
        self.sold.setText(owner_data[1][0])
        self.rent.setText(owner_data[1][1])

        self.upgrade.clicked.connect(self.upgrades)
        if int(self.user) == 1:
            identity = 1
            place_x = 0
            place_y = 100

            for i in range(int(self.game_area)):
                area = database.get_area(identity)
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
        else:
            identity = 1
            place_x = 0
            place_y = 100

            for i in range(int(self.game_area)):
                area = database.get_area(identity)
                if str(area[4])==str(self.uid[2]):
                    buton_text = area[0] + " " + area[1] + " id:" + str(area[2]) + " " + area[3]
                    button = QPushButton(buton_text, self, objectName=str(identity))
                    button.clicked.connect(self.get_areas)
                    button.resize(150, 30)
                    button.move(place_x, place_y)
                    place_y += 30
                    if (identity - 1) % 10 == 0:
                        place_x += 150
                        place_y = 100
                identity += 1

    def get_areas(self, clicked):
        sender = self.sender()
        EmlakWindow.bid = sender.objectName()
        self.window = EmlakWindow(self)
        self.window.show()

    def upgrades(self):
        salarys = self.salary.text()
        database.set_cost(self.uid[2], self.uid[0], salarys, 0, self.sold.text(), self.rent.text())
        sold_c = self.sold_commission.text()
        rent_c = self.rent_commission.text()
        database.set_emlak_commission(sold_c, rent_c, self.uid[0], self.uid[2])

class EmlakWindow(QtWidgets.QMainWindow):
    bid = None
    type_business = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./admin_windows/emlak_satis_kiralik.ui", self)
        self.setWindowTitle("Emlak")
        price = database.get_emlak_rent_sold_price(self.bid)
        self.type_business = price[2]
        if price[2] != '4':
            self.sold.setText(str(price[0]))
            self.rent.setText(str(price[1]))
        else:
            QObjectCleanupHandler().add(self.rent)
            QObjectCleanupHandler().add(self.label_2)
            self.sold.setText(str(price[0]))
        self.upgrade.clicked.connect(self.upgrades)

    def upgrades(self):
        if self.type_business != '4':
            sold_price = self.sold.text()
            rent_price = self.rent.text()
            database.set_emlak_rent_sold_price(self.bid, sold_price, rent_price)
        else:
            sold_price = self.sold.text()
            database.set_emlak_rent_sold_price(self.bid, sold_price, 9999)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 200)
    window.show()
    app.exec()
