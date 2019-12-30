import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, \
    QPushButton, QWidget, QLabel, QLineEdit, QTextEdit, QMessageBox
from UI.main import Ui_MainWindow
import sqlite3


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.con = sqlite3.connect("data/coffee.db")
        self.cur = self.con.cursor()

        self.addBase = QPushButton("Добавить\nКофе", self)
        self.addBase.setGeometry(525, 500, 100, 40)

        self.updateBase = QPushButton("Изменить", self)
        self.updateBase.setGeometry(50, 500, 100, 40)

        self.pushButton.clicked.connect(self.loadTable)
        self.addBase.clicked.connect(self.window_add)
        self.updateBase.clicked.connect(self.window_update)

    def loadTable(self):

        cmd = """SELECT variety_name, degree_roasting, view, 
        description_taste, price, volume_packagings_grams FROM cofe_informations"""
        resultat = self.cur.execute(cmd).fetchall()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["Имя сорта",
                                                    "Степень обжарки",
                                                    "Молотый/в зернах",
                                                    "Описание вкуса",
                                                    "Цена",
                                                    "Объем упаковки"])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(resultat):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()

    def window_add(self):
        self.add = AddBaseDate()
        self.add.show()

    def window_update(self):
        if len(self.tableWidget.selectedItems()) == 6:
            res = self.cur.execute("SELECT id FROM cofe_informations "
                                   "WHERE variety_name=?",
                                   (self.tableWidget.selectedIndexes()[0].data(),)).fetchall()[0][0]

            self.upd = UpdateBaseDate(self, res)
            self.upd.show()

        elif len(self.tableWidget.selectedItems()) == 0:
            QMessageBox.question(self, "Ошибка", "Вы не выбрали что нужно изменить", QMessageBox.Ok, QMessageBox.Ok)

        else:
            QMessageBox.question(self, "Неправильно Выбран элемент", "Вы должны выбрать номер строчки "
                                                                     "1, 2, 3... чтобы изменить его значения",
                                 QMessageBox.Ok, QMessageBox.Ok)


class AddBaseDate(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 100, 400, 500)
        self.setWindowTitle('Добавить')

        self.add = QPushButton("Добавить", self)
        self.add.setGeometry(150, 400, 100, 50)
        self.add.clicked.connect(self.addBaseDate)

        self.initUI()

    def initUI(self):
        self.label1 = QLabel("Имя Сорта:", self)
        self.label1.setGeometry(20, 20, 100, 20)

        self.label2 = QLabel("Степень Обжарки:", self)
        self.label2.setGeometry(20, 70, 100, 20)

        self.label3 = QLabel("Молотый/В Зернах:", self)
        self.label3.setGeometry(20, 120, 100, 20)

        self.label4 = QLabel("Описания Вкуса:", self)
        self.label4.setGeometry(20, 170, 100, 20)

        self.label5 = QLabel("Цена:", self)
        self.label5.setGeometry(20, 220, 100, 20)

        self.label6 = QLabel("Объем упаковки:", self)
        self.label6.setGeometry(20, 270, 100, 20)

        self.name = QLineEdit(self)
        self.name.setGeometry(140, 20, 100, 20)

        self.degree = QLineEdit(self)
        self.degree.setGeometry(140, 70, 100, 20)

        self.state = QLineEdit(self)
        self.state.setGeometry(140, 120, 100, 20)

        self.descriptions = QTextEdit(self)
        self.descriptions.setGeometry(140, 170, 250, 45)

        self.price = QLineEdit(self)
        self.price.setGeometry(140, 220, 100, 20)

        self.volume = QLineEdit(self)
        self.volume.setGeometry(140, 270, 100, 20)

    def addBaseDate(self):
        name = self.name.text()
        degree = self.degree.text()
        state = self.state.text()
        descriptions = " ".join([i for i in self.descriptions.toPlainText().split()])
        price = self.price.text()
        volum = self.volume.text()

        if len(name) != 0 and len(degree) != 0 and len(state) != 0 \
                and len(descriptions) != 0 and len(price) != 0 and len(volum) != 0:

            con = sqlite3.connect("data/coffee.db")
            cur = con.cursor()
            cmd = """INSERT INTO cofe_informations(variety_name, degree_roasting, 
            view, description_taste, price, volume_packagings_grams) VALUES(?, ?, ?, ?, ?, ?)"""
            cur.execute(cmd, (name, degree, state, descriptions, price, volum))
            con.commit()

            self.hide()

        else:
            QMessageBox.question(self, "Ошибка", "Не все поля введены", QMessageBox.Ok, QMessageBox.Ok)


class UpdateBaseDate(QWidget):
    def __init__(self, *args):
        self.num = args[1]
        super().__init__()
        self.setGeometry(200, 100, 400, 500)
        self.setWindowTitle('Изменить')

        self.label1 = QLabel("Имя Сорта:", self)
        self.label1.setGeometry(20, 20, 100, 20)

        self.label2 = QLabel("Степень Обжарки:", self)
        self.label2.setGeometry(20, 70, 100, 20)

        self.label3 = QLabel("Молотый/В Зернах:", self)
        self.label3.setGeometry(20, 120, 100, 20)

        self.label4 = QLabel("Описания Вкуса:", self)
        self.label4.setGeometry(20, 170, 100, 20)

        self.label5 = QLabel("Цена:", self)
        self.label5.setGeometry(20, 220, 100, 20)

        self.label6 = QLabel("Объем упаковки:", self)
        self.label6.setGeometry(20, 270, 100, 20)

        self.update_btn = QPushButton("Обновить", self)
        self.update_btn.setGeometry(150, 400, 100, 50)
        self.update_btn.clicked.connect(self.updateBaseDate)

        self.initUI()

    def initUI(self):
        self.con = sqlite3.connect("data/coffee.db")
        self.cur = self.con.cursor()
        cmd = """SELECT variety_name, degree_roasting, view, description_taste, 
        price, volume_packagings_grams FROM cofe_informations WHERE id = ?"""
        result = self.cur.execute(cmd, (self.num,)).fetchall()[0]

        self.name = QLineEdit(self)
        self.name.setGeometry(140, 20, 150, 20)
        self.name.setText(result[0])

        self.degree = QLineEdit(self)
        self.degree.setGeometry(140, 70, 150, 20)
        self.degree.setText(result[1])

        self.state = QLineEdit(self)
        self.state.setGeometry(140, 120, 150, 20)
        self.state.setText(result[2])

        self.descriptions = QTextEdit(self)
        self.descriptions.setGeometry(140, 170, 250, 45)
        self.descriptions.setText(result[3])

        self.price = QLineEdit(self)
        self.price.setGeometry(140, 220, 150, 20)
        self.price.setText(result[4])

        self.volume = QLineEdit(self)
        self.volume.setGeometry(140, 270, 150, 20)
        self.volume.setText(result[5])

    def updateBaseDate(self):
        name = self.name.text()
        degree = self.degree.text()
        state = self.state.text()
        descriptions = " ".join([i for i in self.descriptions.toPlainText().split()])
        price = self.price.text()
        volum = self.volume.text()

        if len(name) != 0 and len(degree) != 0 and len(state) != 0 \
                and len(descriptions) != 0 and len(price) != 0 and len(volum) != 0:

            cmd = """UPDATE cofe_informations
            SET variety_name=?, degree_roasting=?, view=?, description_taste=?, price=?, volume_packagings_grams=?
            WHERE id=?"""

            self.cur.execute(cmd, (name, degree, state, descriptions, price, volum, self.num))
            self.con.commit()

            self.hide()

        else:
            QMessageBox.question(self, "Ошибка", "Не все поля заполнены", QMessageBox.Ok, QMessageBox.Ok)

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())