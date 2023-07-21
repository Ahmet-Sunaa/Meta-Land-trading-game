from PyQt6 import QtCore, QtGui, QtWidgets, uic
import sys

from PyQt6.QtWidgets import QPushButton

from database import database
from manager import item_shop
class MainWindow(QtWidgets.QMainWindow):
    game_area_info = None
    uid = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./user_windows/esya.ui", self)
        self.setWindowTitle("Eşya")
        name = database.get_area_owner(self.game_area_info[0])
        self.business_owner.setText(name)
        item_cost = database.get_shop_price(self.game_area_info[0])
        self.item_coast.setText(item_cost[0])
        salary = database.get_shop_salary(self.game_area_info[0])
        self.daily_salary.setText(salary[0])
        self.buy_button.clicked.connect(self.buy_food)
        if str(self.uid[0]) == str(self.game_area_info[2]):
            button = QPushButton('Güncelleme Sayfası', self, objectName=str('update'))
            button.clicked.connect(self.update_page)
            button.resize(150, 30)
            button.move(10, 120)
    def buy_food(self):
        buy_count = self.item_count.text()
        database.buy_food_item(self.uid[0], buy_count, self.game_area_info)

    def update_page(self):
        item_shop.MainWindow.uid = self.game_area_info
        window_shop = item_shop.MainWindow(self)
        window_shop.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(80, 80)
    window.show()
    app.exec()
