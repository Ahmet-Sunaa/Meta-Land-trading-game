from PyQt6 import QtCore, QtGui, QtWidgets, uic
import sys
from manager.admin_database import database


class MainWindow(QtWidgets.QMainWindow):
    uid = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./admin_windows/arsa.ui", self)
        self.setWindowTitle("Arsa")
        owner_data = database.get_area_owner(self.uid[2])
        name = owner_data[0][0] + " " + owner_data[0][1]
        self.owner.setText(name)
        owner_data = database.get_emlak_rent_sold_price(self.uid[0])
        self.price.setText(owner_data[0])
        self.upgrade.clicked.connect(self.upgrades)

    def upgrades(self):
        sold_price = self.price.text()
        database.set_emlak_rent_sold_price(self.uid[0], sold_price, 9999)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 200)
    window.show()
    app.exec()