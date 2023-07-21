import sys

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QPushButton, QTableWidgetItem

from manager import item_shop, arsa, market, real_estate
from database import database

from manager.admin_database import database as d

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_property = database.get_all_property()
        uic.loadUi("./admin_windows/manager_window.ui", self)
        self.setWindowTitle("Yönetici")
        row = 0
        self.ownered_by_admin.setRowCount(len(self.total_property))
        for i in self.total_property:
            self.ownered_by_admin.setItem(row, 0, QTableWidgetItem(str(i[0])))
            self.ownered_by_admin.setItem(row, 1, QTableWidgetItem(str(i[1])))
            self.ownered_by_admin.setItem(row, 2, QTableWidgetItem(str(i[2])))
            self.ownered_by_admin.setItem(row, 3, QTableWidgetItem(str(i[3])))
            self.ownered_by_admin.setItem(row, 4, QTableWidgetItem(str(i[4])))
            row+=1
        self.upgrade_button.clicked.connect(self.upgrade_starter)
        self.daily_upgrade_button.clicked.connect(self.upgrade_daily)
        self.map_buton.clicked.connect(self.open_map)
        self.Build_upgrade_button.clicked.connect(self.build_upgrade)
        self.level_upgrade_button.clicked.connect(self.level_upgrade)
        button = QtWidgets.QPushButton('Database sıfırlama', self, objectName='delete_database')
        button.resize(120, 30)
        button.clicked.connect(self.database_deleted)
        button.move(10, 550)



    def upgrade_starter(self):
        food = self.food.text()
        money = self.money.text()
        items = self.item.text()
        area_size = self.area_size.text()
        shop_salary = self.shop_salary.text()
        item_salary = self.item_salary.text()
        emlak_salary = self.emlak_salary.text()
        food_price = self.food_price.text()
        item_price = self.item_price.text()
        database.manager_upgrade_starter(items, money, food, area_size, shop_salary, item_salary, emlak_salary,
                                         food_price, item_price)

    def upgrade_daily(self):
        food = self.daily_food.text()
        money = self.daily_money.text()
        item = self.daily_item.text()
        database.manager_upgrade_daily(item, money, food)

    def build_upgrade(self):
        market_price = self.market_text.text()
        emlak_price = self.emlak_text.text()
        supermarket_price = self.supermarket_text.text()
        database.manager_upgrade_build_cost(market_price, supermarket_price, emlak_price)

    def level_upgrade(self):
        first = self.first_text.text()
        second = self.second_text.text()
        third = self.third_text.text()
        database.manager_upgrade_level_cost(first, second, third)

    def database_deleted(self):
        d.deleted_database()

    def open_map(self):
        new_window = map(self)
        new_window.show()

class map(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./admin_windows/map.ui", self)
        self.setWindowTitle("Yönetici Map")
        self.game_area = database.get_game_area()
        identity = 1
        for i in range(int(self.game_area[0])):
            for j in range(int(self.game_area[1])):
                area_data = database.get_area_type(str(identity))
                button = QPushButton('', self, objectName=str(identity))
                button.resize(80, 80)
                button.clicked.connect(self.get_areas)
                button.move(80 * (j + 1), 80 * (i + 1))
                if area_data[0][1] == '1':
                    button.setIcon(QtGui.QIcon('./icons/ev.png'))
                    button.setIconSize(QtCore.QSize(70, 70))
                elif area_data[0][1] == '2':
                    button.setIcon(QtGui.QIcon('./icons/market.png'))
                    button.setIconSize(QtCore.QSize(70, 70))
                elif area_data[0][1] == '3':
                    button.setIcon(QtGui.QIcon('./icons/esya.png'))
                    button.setIconSize(QtCore.QSize(70, 70))
                else:
                    button.setIcon(QtGui.QIcon('./icons/arsa.png'))
                    button.setIconSize(QtCore.QSize(70, 70))
                button.setToolTip(database.get_area_owner(str(identity)))
                identity += 1

    def get_areas(self, clicked):
        sender = self.sender()
        checker = database.get_area_type(str(sender.objectName()))
        if checker[0][1] == '1':
            real_estate.MainWindow.user = 1
            real_estate.MainWindow.game_area = int(self.game_area[0])*int(self.game_area[1])
            real_estate.MainWindow.uid = checker[0]
            window_shop = real_estate.MainWindow(self)
            window_shop.show()
        elif checker[0][1] == '2':
            market.MainWindow.uid = checker[0] ######market bitiiiiiiiiiiiiiiiiiiiiiiiiiii diğerlerini de yapppppppp
            window_shop = market.MainWindow(self)
            window_shop.show()
        elif checker[0][1] == '3':
            item_shop.MainWindow.uid = checker[0]
            window_shop = item_shop.MainWindow(self)
            window_shop.show()
        else:
            arsa.MainWindow.uid = checker[0]
            window_shop = arsa.MainWindow(self)
            window_shop.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(80, 80)
    window.show()
    app.exec()
