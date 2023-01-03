import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from index_ui import Ui_MainWindow

boton = ""


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # loadUi("index.ui", self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.sidebarMin.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btnExpandDescargar.setChecked(True)

        self.ui.btnDescargar.clicked.connect(self.toogleButton)
        self.ui.btnExpandDescargar.clicked.connect(self.toogleButton)

        self.ui.btnEntrenamiento.clicked.connect(self.toogleButton)
        self.ui.btnExpandEntrenamiento.clicked.connect(self.toogleButton)

        self.ui.btnClasificacion.clicked.connect(self.toogleButton)
        self.ui.btnExpandClasificacion.clicked.connect(self.toogleButton)

        self.ui.btnMapa.clicked.connect(self.toogleButton)
        self.ui.btnExpandMapa.clicked.connect(self.toogleButton)


    def toogleButton(self):
        if str(self.sender().objectName()).__contains__("Descargar"):
            self.ui.stackedWidget.setCurrentIndex(0)

        if str(self.sender().objectName()).__contains__("Entrenamiento"):
            self.ui.stackedWidget.setCurrentIndex(1)

        if str(self.sender().objectName()).__contains__("Clasificacion"):
            self.ui.stackedWidget.setCurrentIndex(2)
        if str(self.sender().objectName()).__contains__("Mapa"):
            self.ui.stackedWidget.setCurrentIndex(3)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # with open("index.qss", "r") as style_file:
    #     app.setStyleSheet(style_file.read())

    style_file = QFile("index.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
