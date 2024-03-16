import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.setWindowTitle('🍵')
        self.show_result()
        self.red = Redactor()
        self.pushButton.clicked.connect(self.open_r)

    def show_result(self):
        cursor = self.connection.cursor()
        result = cursor.execute("SELECT * FROM coffee").fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
             'описание вкуса', 'цена', 'объем упаковки'])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def open_r(self):
        self.hide()
        self.red = Redactor()
        self.red.show()


class Redactor(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.setWindowTitle('🍵')
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton.clicked.connect(self.save_results)
        self.pushButton_2.clicked.connect(self.new_coffee)
        self.modified = {}
        self.show_result()

    def show_result(self):
        cur = self.connection.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            cur.execute("UPDATE coffee SET " + ", ".join(
                [f"{key}='{self.modified.get(key)}'"
                 for key in
                 self.modified.keys()]) + f" WHERE ID = {self.modified['ID']}")
            self.con.commit()
            self.modified.clear()

    def new_coffee(self):
        cur = self.con.cursor()
        cur.execute(
            f"""INSERT INTO coffee VALUES({self.lineEdit_1.text()},
                                            '{self.lineEdit_2.text()}',
                                            '{self.lineEdit_3.text()}',
                                            '{self.lineEdit_4.text()}',
                                            '{self.lineEdit_5.text()}',
                                            '{self.lineEdit_6.text()}',
                                            '{self.lineEdit_7.text()}');""")
        self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
