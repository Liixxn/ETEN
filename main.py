import sys
import tkinter.messagebox
from pathlib import Path

from tkinter import *

import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from PyQt5 import *
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi

from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
import os
from index_ui import Ui_MainWindow
import ventanaAniadirCategoria_ui
import re






import pln
import text_processing




rutasCategorias = dict()
nombresCategorias = dict()

df_algortimoKnn = pd.DataFrame(columns=['Ficheros', 'Categorias'])
df_algortimoRF = pd.DataFrame(columns=['Ficheros', 'Categorias'])
df_algortimoNB = pd.DataFrame(columns=['Ficheros', 'Categorias'])

df_textos_count = pd.DataFrame(columns=["Carpeta Categorias", "Total"])

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # loadUi("index.ui", self)

        self.ui = Ui_MainWindow()

        self.Second_MainWindow = QtWidgets.QDialog()


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

        ventanaPrincipal.btnGuardarModelo.clicked.connect(self.guardarModeloEntrenamiento)


        ventanaPrincipal.algoritmoKnn.clicked.connect(self.eleccionAlgoritmoKnn)
        ventanaPrincipal.algortimoRandomForest.clicked.connect(self.eleccionAlgoritmoRF)
        ventanaPrincipal.algortimoNaiveBayes.clicked.connect(self.eleccionAlgoritmoNB)

        # Rellena el diccionario de las categorias nada mas sacar la ventana
        for numeroCategoria in range(self.ui.comboBox_Categorias.count()):
            nombresCategorias[numeroCategoria] = self.ui.comboBox_Categorias.itemText(numeroCategoria)

    # Funcion que despliega las paginas del menu lateral
    def toogleButton(self):
        if str(self.sender().objectName()).__contains__("Descargar"):
            self.ui.stackedWidget.setCurrentIndex(0)

        if str(self.sender().objectName()).__contains__("Entrenamiento"):
            self.ui.stackedWidget.setCurrentIndex(1)

        if str(self.sender().objectName()).__contains__("Clasificacion"):
            self.ui.stackedWidget.setCurrentIndex(2)
        if str(self.sender().objectName()).__contains__("Mapa"):
            self.ui.stackedWidget.setCurrentIndex(3)

    #############################################################################################33

    # VENTANA ENTRENAMIENTO

    # Funcion que abre el explorador de archivos para seleccionar la ruta de la carpeta
    def abrirArchivo(self):
        selected_folder = askdirectory()

        if not selected_folder:
            self.ui.txt_paths.setText("")
            print("No se ha seleccionado ninguna carpeta")
        else:
            # nombreFolder = Path(selected_folder).stem
            self.ui.txt_paths.setText(selected_folder)

    # Funcion que guarda la ruta seleccionada por el usuario y la almacena en un diccionario
    def aceptarArchivo(self):

        # rutasCategorias = list(range(self.ui.comboBox_Categorias.count()+1))

        if self.ui.txt_paths.text() == "":
            tkinter.messagebox.showerror("Error", "No se ha seleccionado ninguna carpeta")
        else:
            if not os.path.exists(os.path.dirname(self.ui.txt_paths.text())):
                tkinter.messagebox.showerror("Error", "La carpeta seleccionada no existe")
            else:
                # Se comprueba que la ruta no este ya en el diccionario
                pln.comprobarCategoria(self.ui.txt_paths.text(), self.ui.comboBox_Categorias.currentIndex(),
                                       rutasCategorias)


    ##############################################################################################

    # POPUP ANIADIR CATEGORIA

    # Funcion que abre la ventana para aniadir una nueva categoria
    def aniadirCategoria(self, nuevaCategoria):


        self.popUpCategoria = ventanaAniadirCategoria_ui.Ui_Dialog()
        self.popUpCategoria.setupUi(self.Second_MainWindow)
        self.Second_MainWindow.show()

        self.popUpCategoria.aniadirCategoria_btnAbrir.clicked.connect(self.abirRuta_popup)
        self.popUpCategoria.aniadirCategoria_btnAniadir.clicked.connect(self.aniadirNuevaCategoria)

        # dialog = popUpAniadirCategoria.nuevaCategoria(self)
        # dialog.show()
        # dialog.aniadirNuevaCategoria(nuevaCategoria, self.ui.comboBox_Categorias)

    # Funcion que abre el explorador de archivos para seleccionar la ruta de la carpeta
    def abirRuta_popup(self):

        nuevaRuta = askdirectory()

        if not nuevaRuta:
            self.popUpCategoria.aniadirCategoria_txtRuta.setText("")
            print("No se ha seleccionado ninguna carpeta")
        else:
            self.popUpCategoria.aniadirCategoria_txtRuta.setText(nuevaRuta)

    # Funcion que guarda la ruta seleccionada por el usuario y la almacena en un diccionario
    def aniadirNuevaCategoria(self):

        nombreNuevaCategoria = self.popUpCategoria.aniadirCategoria_nombreCategoria.text()
        rutaNuevaCategoria = self.popUpCategoria.aniadirCategoria_txtRuta.text()

        nombreExiste = False
        rutaExiste = False

        if nombreNuevaCategoria == "" or rutaNuevaCategoria == "":
            tkinter.messagebox.showerror("Error",
                                         "No se ha seleccionado ninguna carpeta o no se ha introducido un nombre de categoría")
        else:
            if not os.path.exists(os.path.dirname(rutaNuevaCategoria)):
                tkinter.messagebox.showerror("Error", "La carpeta seleccionada no existe")
            else:
                numElementos = self.ui.comboBox_Categorias.count()
                for i in range(numElementos):
                    if re.search(nombreNuevaCategoria, self.ui.comboBox_Categorias.itemText(i), re.IGNORECASE):
                        nombreExiste = True
                        tkinter.messagebox.showerror("Error", "El nombre de la categoría ya existe")

                if nombreExiste == False:
                    for indice in rutasCategorias.values():
                        if rutaNuevaCategoria in indice:
                            rutaExiste = True
                            print("La categoria no existe pero la ruta si")

                    if rutaExiste == False:
                        rutasCategorias[numElementos] = []
                        rutasCategorias[numElementos].append(rutaNuevaCategoria)
                        self.ui.comboBox_Categorias.addItem(nombreNuevaCategoria)
                        tkinter.messagebox.showinfo("Información", "Categoría añadida correctamente")
                        print("Se añade la nueva categoria")
                        nombresCategorias[numElementos] = self.ui.comboBox_Categorias.itemText(numElementos)

    #############################################################################################

    # Funcion que recoge la seleccion del algoritmo a utilizar
    def eleccionAlgoritmoKnn(self):

        df_knn = pd.DataFrame(columns=['Ficheros', 'Categorias'])

        if self.ui.algoritmoKnn.isChecked():
            print("KNN")

            if len(rutasCategorias) !=1:

                df_knn["Ficheros"], df_knn["Categorias"], df_textos_count = text_processing.process_text(rutasCategorias)

                # df_knn.index = df_knn.index + 1

                df_knn = text_processing.tratamientoBasico(df_knn)
                df_knn = text_processing.quit_stopwords(df_knn)
                df_knn = text_processing.stemming(df_knn)

                df_algortimoKnn = df_knn
                print(df_algortimoKnn)

            else:
                tkinter.messagebox.showerror("Error", "Debe al menos seleccionar dos categorías")

    def eleccionAlgoritmoRF(self):

        df_rf = pd.DataFrame(columns=['Ficheros', 'Categorias'])

        if self.ui.algortimoRandomForest.isChecked():
            print("Random Forest")

            if len(rutasCategorias) != 1:

                df_rf["Ficheros"], df_rf["Categorias"] = text_processing.process_text(rutasCategorias)

                # df_knn.index = df_knn.index + 1

                df_rf = text_processing.tratamientoBasico(df_rf)
                df_rf = text_processing.quit_stopwords(df_rf)
                df_rf = text_processing.stemming(df_rf)

                df_algortimoRF = df_rf


            else:
                tkinter.messagebox.showerror("Error", "Debe al menos seleccionar dos categorías")


    def eleccionAlgoritmoNB(self):

        df_nb = pd.DataFrame(columns=['Ficheros', 'Categorias'])

        if self.ui.algortimoNaiveBayes.isChecked():
            print("Naive Bayes")

            if len(rutasCategorias) != 1:

                df_nb["Ficheros"], df_nb["Categorias"] = text_processing.process_text(rutasCategorias)

                # df_knn.index = df_knn.index + 1

                df_nb = text_processing.tratamientoBasico(df_nb)
                df_nb = text_processing.quit_stopwords(df_nb)
                df_nb = text_processing.stemming(df_nb)

                df_algortimoNB = df_nb

            else:
                tkinter.messagebox.showerror("Error", "Debe al menos seleccionar dos categorías")











    # Funcion que guarda el fichero generado tras el entrenamiento
    def guardarModeloEntrenamiento(self):

        files = [('All Files', '*.*'),
                 ('Python Files', '*.py'),
                 ('Text Document', '*.txt')]

        nombreFicheroGuardar = asksaveasfilename(filetypes=files)

    # Funcion que cierra la aplicacion y las ventanas que esten abiertas
    def closeEvent(self, event):
        try:
            print("Cerrando la aplicacion")

            self.Second_MainWindow.close()
            event.accept()
        except Exception as e:
            print(e)


# Main de la aplicacion
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # with open("index.qss", "r") as style_file:
    #     app.setStyleSheet(style_file.read())

    # Hoja de estilos
    style_file = QFile("index.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
