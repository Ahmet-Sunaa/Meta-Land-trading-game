from PyQt6 import QtCore, QtGui, QtWidgets, uic
import sys
from manager.admin_database import database

class MainWindow(QtWidgets.QMainWindow):
    uid = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./admin_windows/market.ui", self)
        self.setWindowTitle("Market")
        owner_data = database.get_area_owner(self.uid[2])
        name = owner_data[0][0]+" "+owner_data[0][1]
        self.owner.setText(name)
        owner_data = database.get_cost(self.uid[2], self.uid[0])
        self.coast.setText(owner_data[0][0])
        self.salary.setText(owner_data[1][0])
        self.sold_price.setText(owner_data[2][0])
        self.rent_price.setText(owner_data[2][1])
        self.upgrade.clicked.connect(self.upgrades)

    def upgrades(self):
        cost = self.coast.text()
        salarys = self.salary.text()
        sold = self.sold_price.text()
        rent = self.rent_price.text()
        database.set_cost(self.uid[2], self.uid[0], salarys, cost, sold, rent)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 200)
    window.show()
    app.exec()