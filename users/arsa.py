from PyQt6 import QtCore, QtGui, QtWidgets, uic
import sys

from PyQt6.QtCore import QObjectCleanupHandler, QSize
from PyQt6.QtWidgets import QPushButton

from database import database


class MainWindow(QtWidgets.QMainWindow):
    game_area_info = None
    uid = None
    bid = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./user_windows/arsa.ui", self)
        self.setWindowTitle("Arsa")
        if int(self.uid[0]) == int(self.game_area_info[2]):
            name = database.get_area_owner(self.game_area_info[0])
            self.owner.setText(name)

            business_price = database.get_sold_business(self.game_area_info[0])
            self.textLine = QtWidgets.QLineEdit(self, objectName='sold')
            self.textLine.setText(business_price[0])
            self.textLine.move(100, 30)
            self.textLine.show()

            button = QtWidgets.QPushButton('Güncelle', self)
            button.resize(100, 30)
            button.move(0, 70)
            button.clicked.connect(self.upgrades)


            QObjectCleanupHandler().add(self.price)
            # self.price.setText(business_price[0])
        else:
            name = database.get_area_owner(self.game_area_info[0])
            self.owner.setText(name)
            business_price = database.get_sold_business(self.game_area_info[0])
            self.price.setText(business_price[0])

    def upgrades(self):
        sold_price = self.textLine.text()
        database.set_emlak_rent_sold_price(self.bid, sold_price, 9999)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(80, 80)
    window.show()
    app.exec()
