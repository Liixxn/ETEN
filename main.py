import sys
import tkinter.messagebox

import joblib
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QGraphicsScene

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import re
import matplotlib.pyplot as plt


from index_ui import Ui_MainWindow
import ventanaAniadirCategoria_ui
import ventanaLoading_ui




import pln
import text_processing
import pandas_table



rutasCategorias = dict()
nombresCategorias = dict()


df_algortimoKnn = pd.DataFrame(columns=['Ficheros', 'Categorias'])
df_algortimoRF = pd.DataFrame(columns=['Ficheros', 'Categorias'])
df_algortimoNB = pd.DataFrame(columns=['Ficheros', 'Categorias'])

final_modeloKnn = KNeighborsClassifier()
final_modeloRF = RandomForestClassifier()
final_modeloNB = MultinomialNB()

modelosFinales = dict()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # loadUi("index.ui", self)

        self.ui = Ui_MainWindow()

        self.Second_MainWindow = QtWidgets.QDialog()
        self.Third_MainWindow = QtWidgets.QWidget()

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

        #############################################################################################

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

                    carpetaValida = True
                    contentFiles = os.listdir(self.ui.txt_paths.text())
                    for i in contentFiles:
                        if carpetaValida == True:
                            if i.endswith(".txt"):
                                carpetaValida = True
                            else:
                                carpetaValida = False

                    if carpetaValida == False:
                        tkinter.messagebox.showerror("Error", "La carpeta seleccionada no es valida")
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
            self.Second_MainWindow.setWindowIcon(QtGui.QIcon(r"ETEN_png.png"))
            self.Second_MainWindow.show()

            self.popUpCategoria.aniadirCategoria_btnAbrir.clicked.connect(self.abirRuta_popup)
            self.popUpCategoria.aniadirCategoria_btnAniadir.clicked.connect(self.aniadirNuevaCategoria)

        # Funcion que abre el explorador de archivos para seleccionar la ruta de la carpeta
        def abirRuta_popup(self):

            nuevaRuta = askdirectory()

            if not nuevaRuta:
                self.popUpCategoria.aniadirCategoria_txtRuta.setText("")
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

        # Algortimo Knn

        # Funcion que recoge la seleccion del algoritmo a utilizar
        def eleccionAlgoritmoKnn(self):

            TotalRecetas = 0
            precisionKnn = 0
            sumaPositivos = 0
            sumaFalsosPositivos = 0
            coloresPie = ['green', 'red']
            labelsPie = ["Correctos", "Incorrectos"]
            df_textos_count = pd.DataFrame(columns=["Carpeta", "Total"])
            df_knn = pd.DataFrame(columns=['Ficheros', 'Categorias'])

            if self.ui.algoritmoKnn.isChecked():

                if len(rutasCategorias) != 1:

                    df_knn["Ficheros"], df_knn["Categorias"], df_textos_count["Carpeta"], df_textos_count[
                        "Total"], TotalRecetas = text_processing.process_text(rutasCategorias)

                    listaNombreCategoriasNumero = []

                    for i, j in df_textos_count.iterrows():
                        texto = self.ui.comboBox_Categorias.itemText(j["Carpeta"])
                        listaNombreCategoriasNumero.append(texto)

                    for i in range(len(listaNombreCategoriasNumero)):
                        df_textos_count["Carpeta"][i] = listaNombreCategoriasNumero[i]

                    model = pandas_table.DataFrameModel(df_textos_count)
                    self.ui.previewEntrenamiento.setModel(model)

                    self.ui.labelNumRecetasTotal.setText(str(TotalRecetas))
                    # df_knn.index = df_knn.index + 1

                    df_knn = text_processing.tratamientoBasico(df_knn)
                    df_knn = text_processing.quit_stopwords(df_knn)
                    df_knn = text_processing.stemming(df_knn)

                    df_algortimoKnn = df_knn

                    try:
                        df_matrix_confusion_knn, precisionKnn, sumaPositivos, sumaFalsosPositivos, modeloKnn = text_processing.calculate_weightKnn(
                            df_algortimoKnn)

                        final_modeloKnn = modeloKnn
                        modelosFinales[1] = final_modeloKnn

                        model = pandas_table.DataFrameModel(df_matrix_confusion_knn)
                        self.ui.matrizConfusionEntrenamiento.setModel(model)
                        self.ui.labelPrecisionAlgoritmo.setText(str(precisionKnn))

                        self.figure = plt.figure(figsize=(5, 5))

                        self.figureCanvas = FigureCanvas(self.figure)

                        self.navigationToolbar = NavigationToolbar(self.figureCanvas, self)

                        layout = QtWidgets.QVBoxLayout()
                        layout.addWidget(self.navigationToolbar)
                        layout.addWidget(self.figureCanvas)
                        self.ui.widget_4.setLayout(layout)

                        # for i, nombre in df_textos_count.iterrows():
                        #     labelsPie.append(nombre["Carpeta"])

                        x = [sumaPositivos, sumaFalsosPositivos]
                        ax = self.figure.add_subplot(111)
                        ax.pie(x, labels=labelsPie, shadow=True, autopct='%1.2f%%', colors=coloresPie)

                        # show canvas
                        self.figureCanvas.show()


                    except Exception as e:
                        print(e)



                else:
                    tkinter.messagebox.showerror("Error", "Debe al menos seleccionar dos categorías")

        #############################################################################################

        # Algoritmo Random Forest

        def eleccionAlgoritmoRF(self):

            TotalRecetas = 0
            precisionRF = 0
            sumaPositivos = 0
            sumaFalsosPositivos = 0
            coloresPie = ['green', 'red']
            labelsPie = ["Correctos", "Incorrectos"]

            df_textos_count = pd.DataFrame(columns=["Carpeta", "Total"])
            df_rf = pd.DataFrame(columns=['Ficheros', 'Categorias'])

            if self.ui.algortimoRandomForest.isChecked():

                if len(rutasCategorias) != 1:

                    df_rf["Ficheros"], df_rf["Categorias"], df_textos_count["Carpeta"], df_textos_count[
                        "Total"], TotalRecetas = text_processing.process_text(rutasCategorias)

                    listaNombreCategoriasNumero = []

                    for i, j in df_textos_count.iterrows():
                        texto = self.ui.comboBox_Categorias.itemText(j["Carpeta"])
                        listaNombreCategoriasNumero.append(texto)

                    for i in range(len(listaNombreCategoriasNumero)):
                        df_textos_count["Carpeta"][i] = listaNombreCategoriasNumero[i]

                    model = pandas_table.DataFrameModel(df_textos_count)
                    self.ui.previewEntrenamiento.setModel(model)

                    self.ui.labelNumRecetasTotal.setText(str(TotalRecetas))

                    df_rf = text_processing.tratamientoBasico(df_rf)
                    df_rf = text_processing.quit_stopwords(df_rf)
                    df_rf = text_processing.stemming(df_rf)

                    df_algortimoRF = df_rf
                    try:

                        df_matrix_confusion_rf, precisionRF, sumaPositivos, sumaFalsosPositivos, modeloRF = text_processing.calculate_weightRF(
                            df_algortimoRF)

                        final_modeloRF = modeloRF
                        modelosFinales[2] = final_modeloRF

                        model = pandas_table.DataFrameModel(df_matrix_confusion_rf)
                        self.ui.matrizConfusionEntrenamiento.setModel(model)
                        self.ui.labelPrecisionAlgoritmo.setText(str(precisionRF))

                        self.figure = plt.figure(figsize=(5, 5))

                        self.figureCanvas = FigureCanvas(self.figure)

                        self.navigationToolbar = NavigationToolbar(self.figureCanvas, self)

                        layout = QtWidgets.QVBoxLayout()
                        layout.addWidget(self.navigationToolbar)
                        layout.addWidget(self.figureCanvas)

                        self.ui.widget_4.setLayout(layout)
                        x = [sumaPositivos, sumaFalsosPositivos]
                        ax = self.figure.add_subplot(111)
                        ax.pie(x, labels=labelsPie, shadow=True, autopct='%1.2f%%', colors=coloresPie)

                        # show canvas
                        self.figureCanvas.show()

                        # for i, nombre in df_textos_count.iterrows():
                        #     labelsPie.append(nombre["Carpeta"])


                    except Exception as e:
                        print(e)


                else:
                    tkinter.messagebox.showerror("Error", "Debe al menos seleccionar dos categorías")

        #############################################################################################

        # Algoritmo Naive Bayes

        def eleccionAlgoritmoNB(self):

            TotalRecetas = 0
            precisionNB = 0
            sumaPositivos = 0
            sumaFalsosPositivos = 0
            coloresPie = ['green', 'red']
            labelsPie = ["Correctos", "Incorrectos"]

            df_textos_count = pd.DataFrame(columns=["Carpeta", "Total"])
            df_nb = pd.DataFrame(columns=['Ficheros', 'Categorias'])

            if self.ui.algortimoNaiveBayes.isChecked():

                if len(rutasCategorias) != 1:

                    df_nb["Ficheros"], df_nb["Categorias"], df_textos_count["Carpeta"], df_textos_count[
                        "Total"], TotalRecetas = text_processing.process_text(rutasCategorias)

                    listaNombreCategoriasNumero = []

                    for i, j in df_textos_count.iterrows():
                        texto = self.ui.comboBox_Categorias.itemText(j["Carpeta"])
                        listaNombreCategoriasNumero.append(texto)

                    for i in range(len(listaNombreCategoriasNumero)):
                        df_textos_count["Carpeta"][i] = listaNombreCategoriasNumero[i]

                    model = pandas_table.DataFrameModel(df_textos_count)
                    self.ui.previewEntrenamiento.setModel(model)

                    self.ui.labelNumRecetasTotal.setText(str(TotalRecetas))

                    df_nb = text_processing.tratamientoBasico(df_nb)
                    df_nb = text_processing.quit_stopwords(df_nb)
                    df_nb = text_processing.stemming(df_nb)

                    df_algortimoNB = df_nb

                    try:
                        df_matrix_confusion_nb, precisionNB, sumaPositivos, sumaFalsosPositivos, modeloNB = text_processing.calculate_weightNB(
                            df_algortimoNB)

                        final_modeloNB = modeloNB
                        modelosFinales[3] = final_modeloNB

                        model = pandas_table.DataFrameModel(df_matrix_confusion_nb)
                        self.ui.matrizConfusionEntrenamiento.setModel(model)
                        self.ui.labelPrecisionAlgoritmo.setText(str(precisionNB))

                        self.figure = plt.figure(figsize=(5, 5))

                        self.figureCanvas = FigureCanvas(self.figure)

                        self.navigationToolbar = NavigationToolbar(self.figureCanvas, self)

                        layout = QtWidgets.QVBoxLayout()
                        layout.addWidget(self.navigationToolbar)
                        layout.addWidget(self.figureCanvas)
                        self.ui.widget_4.setLayout(layout)

                        # for i, nombre in df_textos_count.iterrows():
                        #     labelsPie.append(nombre["Carpeta"])

                        x = [sumaPositivos, sumaFalsosPositivos]
                        ax = self.figure.add_subplot(111)
                        ax.pie(x, labels=labelsPie, shadow=True, autopct='%1.2f%%', colors=coloresPie)

                        # show canvas
                        self.figureCanvas.show()
                    except Exception as e:
                        print(e)

                else:
                    tkinter.messagebox.showerror("Error", "Debe al menos seleccionar dos categorías")

        # los dataframes y algoritmos siempre estan vacios, a pesar de guardarlos en variables "globales"
        # y que se rellenan en las funciones anteriores
        # Funcion que guarda el fichero generado tras el entrenamiento
        def guardarModeloEntrenamiento(self):

            files = [('Model File', '*.pkl')]

            if len(modelosFinales) == 0:
                tkinter.messagebox.showerror("Error", "No se ha realizado ningún entrenamiento")
            else:
                if self.ui.algoritmoKnn.isChecked():
                    model = modelosFinales[1]
                    nombreFicheroGuardar = asksaveasfilename(filetypes=files)
                    joblib.dump(model, nombreFicheroGuardar)
                    self.ui.txt_guardar_path.setText(nombreFicheroGuardar)
                    tkinter.messagebox.showinfo("Información", "Modelo guardado correctamente")

                if self.ui.algortimoNaiveBayes.isChecked():
                    model = modelosFinales[2]
                    nombreFicheroGuardar = asksaveasfilename(filetypes=files)
                    joblib.dump(model, nombreFicheroGuardar)
                    self.ui.txt_guardar_path.setText(nombreFicheroGuardar)
                    tkinter.messagebox.showinfo("Información", "Modelo guardado correctamente")

                if self.ui.algortimoRandomForest.isChecked():
                    model = modelosFinales[3]
                    nombreFicheroGuardar = asksaveasfilename(filetypes=files)
                    joblib.dump(model, nombreFicheroGuardar)
                    self.ui.txt_guardar_path.setText(nombreFicheroGuardar)
                    tkinter.messagebox.showinfo("Información", "Modelo guardado correctamente")

        # Funcion que cierra la aplicacion y las ventanas que esten abiertas
        def closeEvent(self, event):
            try:
                tkinter.messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?")
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
        window.setWindowIcon(QtGui.QIcon(r"ETEN_png.png"))
        window.show()

        sys.exit(app.exec_())
