import sys
from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from PyQt5 import *
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi

from tkinter.filedialog import askopenfilename, askdirectory
import os
from index_ui import Ui_MainWindow
import ventanaAniadirCategoria_ui
import popUpAniadirCategoria


rutasCategorias = []


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # loadUi("index.ui", self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ventanaPrincipal = self.ui

        ventanaPrincipal.sidebarMin.hide()
        ventanaPrincipal.stackedWidget.setCurrentIndex(0)
        ventanaPrincipal.btnExpandDescargar.setChecked(True)

        ventanaPrincipal.btnDescargar.clicked.connect(self.toogleButton)
        ventanaPrincipal.btnExpandDescargar.clicked.connect(self.toogleButton)

        ventanaPrincipal.btnEntrenamiento.clicked.connect(self.toogleButton)
        ventanaPrincipal.btnExpandEntrenamiento.clicked.connect(self.toogleButton)

        ventanaPrincipal.btnClasificacion.clicked.connect(self.toogleButton)
        ventanaPrincipal.btnExpandClasificacion.clicked.connect(self.toogleButton)

        ventanaPrincipal.btnMapa.clicked.connect(self.toogleButton)
        ventanaPrincipal.btnExpandMapa.clicked.connect(self.toogleButton)

        ventanaPrincipal.categoriabtnAbrir.clicked.connect(self.abrirArchivo)

        ventanaPrincipal.categoriabtnAceptar.clicked.connect(self.aceptarArchivo)

        ventanaPrincipal.categoriabtnAniadir.clicked.connect(self.aniadirCategoria)

    def toogleButton(self):
        if str(self.sender().objectName()).__contains__("Descargar"):
            self.ui.stackedWidget.setCurrentIndex(0)

        if str(self.sender().objectName()).__contains__("Entrenamiento"):
            self.ui.stackedWidget.setCurrentIndex(1)

        if str(self.sender().objectName()).__contains__("Clasificacion"):
            self.ui.stackedWidget.setCurrentIndex(2)
        if str(self.sender().objectName()).__contains__("Mapa"):
            self.ui.stackedWidget.setCurrentIndex(3)

    def abrirArchivo(self):
        selected_folder = askdirectory()

        if not selected_folder:
            self.ui.txt_paths.setText("")
            print("No se ha seleccionado ninguna carpeta")
        else:
            nombreFolder = Path(selected_folder).stem
            self.ui.txt_paths.setText(selected_folder)

    def aceptarArchivo(self):
        if self.ui.txt_paths.text() == "":
            print("Ruta vacia")
        else:
            if not os.path.exists(os.path.dirname(self.ui.txt_paths.text())):
                print("La ruta no existe")
            else:

                for ruta in rutasCategorias:
                    if ruta == self.ui.txt_paths.text():
                        print("La ruta ya existe")
                        return
                    else:
                        rutasCategorias.append(self.ui.txt_paths.text())
                        self.ui.txt_paths.setText("")

                        print("Ruta correcta")




    def aniadirCategoria(self, nuevaCategoria):
        dialog = popUpAniadirCategoria.nuevaCategoria(self)
        dialog.exec()





    def closeEvent(self, event):
        print("Cerrando la aplicacion")
        event.accept()


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
