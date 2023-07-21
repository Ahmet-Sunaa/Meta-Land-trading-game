import sys

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QPushButton, QTextBrowser

from users import arsa, item, market, real_estate
from database import database
from manager import admin


class find_job_window(QtWidgets.QMainWindow):
    game_area_info = None
    game_area_size = None
    uid = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(QSize(420, 150))

        identity = 1
        place_x = 0
        place_y = 0
        area = database.get_area(self.uid[0])
        for i in range(int(len(area))):
            buton_text = "id: " + str(area[i][0]) + " Türü: " + str(area[i][1]) + " Maaş: " + str(area[i][2])
            buton_tooltip = "id: " + str(area[i][3]) + " Sahibi: " + str(area[i][4]) + " " + str(area[i][5])
            button = QPushButton(buton_text, self, objectName=str(area[i][0]))
            button.clicked.connect(self.job_accept)
            button.setToolTip(buton_tooltip)
            button.resize(200, 30)
            button.move(place_x, place_y)
            place_y += 30
            identity += 1

    def job_accept(self):
        sender = self.sender()
        self.job_details(sender.objectName())

    def job_details(self, bid):
        button = QPushButton('accept job id:'+str(bid), self,objectName=str(bid))
        button.resize(100, 30)
        button.move(200, 0)
        button.clicked.connect(self.job_entry)
        button.show()
    def job_entry(self):
        sender = self.sender()
        database.set_find_job(sender.objectName(),self.uid)

        #text_browser.setText(str(bid))


class UserWindow(QtWidgets.QMainWindow):
    uid = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./user_windows/map.ui", self)
        self.setWindowTitle("Kullanıcı")
        data = database.getIMF(self.uid[0])
        self.food_label.setText(data[0])
        self.item_label.setText(data[1])
        self.money_label.setText(data[2])
        self.job_button.clicked.connect(self.find_job)
        game_area = database.get_game_area()
        self.send_game_area = int(game_area[0]) * int(game_area[1])
        identity = 1
        for i in range(int(game_area[0])):
            for j in range(int(game_area[1])):
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
                button.setToolTip(database.get_area_owner_tooltip(str(identity)))
                identity += 1

    def get_areas(self, clicked):
        sender = self.sender()
        checker = database.get_area_type(str(sender.objectName()))
        if checker[0][1] == '1':
            real_estate.MainWindow.emlak_id = sender.objectName()
            real_estate.MainWindow.uid = self.uid
            real_estate.MainWindow.game_area_info = checker[0]
            real_estate.MainWindow.game_area = self.send_game_area
            window_shop = real_estate.MainWindow(self)
            window_shop.show()
        elif checker[0][1] == '2':
            market.MainWindow.uid = self.uid
            market.MainWindow.game_area_info = checker[0]
            window_shop = market.MainWindow(self)
            window_shop.show()
        elif checker[0][1] == '3':
            item.MainWindow.uid = self.uid
            item.MainWindow.game_area_info = checker[0]
            window_shop = item.MainWindow(self)
            window_shop.show()
        else:
            arsa.MainWindow.bid = sender.objectName()
            arsa.MainWindow.uid = self.uid
            arsa.MainWindow.game_area_info = checker[0]
            window_shop = arsa.MainWindow(self)
            window_shop.show()

        return database.get_area_type(str(sender.objectName()))

    def find_job(self):
        find_job_window.uid = self.uid
        self.window = find_job_window(self)
        self.window.show()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./user_windows/user_entry.ui", self)
        self.setWindowTitle("Login")
        self.user_entry.clicked.connect(self.user_login)
        self.manager_entry.clicked.connect(self.manager_login)
        self.register_button.clicked.connect(self.register_buton)

    def user_login(self):
        tf_checker = database.login(self.name_line.text(), self.surname_line.text(), self.pasword_line.text())
        if tf_checker[1]:
            UserWindow.uid = tf_checker[0]
            user_window = UserWindow(self)
            user_window.show()

    def manager_login(self):
        tf_checker = database.manager_login(self.name_line.text(), self.surname_line.text(), self.pasword_line.text())
        if tf_checker[1]:
            manager_window = admin.MainWindow(self)
            manager_window.show()

    def register_buton(self):
        database.register(self.name_line.text(), self.surname_line.text(), self.pasword_line.text())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 200)
    window.show()
    app.exec()
