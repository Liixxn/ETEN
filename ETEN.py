# Librerias
import sys
import time
import tkinter.messagebox
from pathlib import Path
import natsort
import joblib
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QGraphicsScene
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Ventanas de diseño de la aplicacion
from index_ui import Ui_MainWindow
import ventanaAniadirCategoria_ui

# .py para el correcto funcionamiento de la aplicacion
import pln
import text_processing
import pandas_table
import descargarVideos

# Variables globales
rutasCategorias = dict()
nombresCategorias = dict()

df_algortimoKnn = pd.DataFrame(columns=['Ficheros', 'Categorias'])
df_algortimoRF = pd.DataFrame(columns=['Ficheros', 'Categorias'])
df_algortimoNB = pd.DataFrame(columns=['Ficheros', 'Categorias'])

final_modeloKnn = KNeighborsClassifier()
final_modeloRF = RandomForestClassifier()
final_modeloNB = MultinomialNB()

modelosFinales = dict()
clasificadorFinal = dict()

diccionarioIngredientes = dict()
rutasUnlabeled = dict()
historialIngredienteSeleccionado = dict()
ingredienteSeleccionado = dict()

sesionAnterior = dict()


# Clase principal de la aplicacion
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Carga de las diferentes ventanas
        self.ui = Ui_MainWindow()

        self.Second_MainWindow = QtWidgets.QDialog()

        self.ui.setupUi(self)

        # Inicializacion de los elementos
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

        ventanaPrincipal.BotonDescargar.clicked.connect(self.descargar)
        ventanaPrincipal.BotonSeleccionar.clicked.connect(self.SelecionarVideoTexto)

        ventanaPrincipal.SelecionarRecetas.clicked.connect(self.abrirRecetasClasificacion)
        ventanaPrincipal.SeleccionarModelo.clicked.connect(self.selecionarModelo)
        ventanaPrincipal.btnConfirmarClasificacion.clicked.connect(self.clasificarTextos)
        ventanaPrincipal.GuardarComo.clicked.connect(self.guardarResultadosClasificacion)
        ventanaPrincipal.categoriabtnEliminar.clicked.connect(self.eliminarseleccion)

        ventanaPrincipal.btnAbrirRecetaAnalizar.clicked.connect(self.abrirRecetaAnalizar)
        ventanaPrincipal.btnCarrefour.clicked.connect(self.abrirCarrefour)
        ventanaPrincipal.btnDia.clicked.connect(self.abrirDia)

        # Rellena el diccionario de las categorias nada mas sacar la ventana
        for numeroCategoria in range(self.ui.comboBoxCategorias.count()):
            nombresCategorias[numeroCategoria] = self.ui.comboBoxCategorias.itemText(numeroCategoria)

    ######################################################################################################
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


    #################################################################################################333333

    # VENTANA DESCARGA

    # Funcion que descarga el video seleccionado o lista de videos
    def descargar(self):
        # lista de reproduccion
        if self.ui.comboBoxElegir.currentIndex() == 0:
            descargarVideos.download_listVideos(self.ui.lineEditURL.text())
        else:
            descargarVideos.downloadVideo(self.ui.lineEditURL.text())

    # Funcion que selecciona el video y procesa el audio generado a texto
    def SelecionarVideoTexto(self):
        descargarVideos.open_file()

    #############################################################################################

    # VENTANA ENTRENAMIENTO

    # Funcion que abre el explorador de archivos para seleccionar la ruta de la carpeta
    def abrirArchivo(self):
        selected_folder = askdirectory()
        if not selected_folder:
            self.ui.txt_paths.setText("")
        else:
            self.ui.txt_paths.setText(selected_folder)


    # Funcion que guarda la ruta seleccionada por el usuario y la almacena en un diccionario
    def aceptarArchivo(self):

        if self.ui.txt_paths.text() == "":
            self.ui.txt_paths.setText("")
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
                    pln.comprobarCategoria(self.ui.txt_paths.text(), self.ui.comboBoxCategorias.currentIndex(),
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
                numElementos = self.ui.comboBoxCategorias.count()
                for i in range(numElementos):
                    if re.search(nombreNuevaCategoria, self.ui.comboBoxCategorias.itemText(i), re.IGNORECASE):
                        nombreExiste = True
                        tkinter.messagebox.showerror("Error", "El nombre de la categoría ya existe")

                if nombreExiste == False:
                    for indice in rutasCategorias.values():
                        if rutaNuevaCategoria in indice:
                            rutaExiste = True
                            tkinter.messagebox.showerror("Error", "La ruta de la categoría ya existe")

                    if rutaExiste == False:
                        rutasCategorias[numElementos] = []
                        rutasCategorias[numElementos].append(rutaNuevaCategoria)
                        self.ui.comboBoxCategorias.addItem(nombreNuevaCategoria)
                        tkinter.messagebox.showinfo("Información", "Categoría añadida correctamente")

                        nombresCategorias[numElementos] = self.ui.comboBoxCategorias.itemText(numElementos)

    def eliminarseleccion(self):
        if not rutasCategorias:
            tkinter.messagebox.showerror("Error", "No hay ninguna ruta de recetas para eliminar")
        else:
            rutasCategorias.clear()
            self.ui.txt_paths.setText("")
            tkinter.messagebox.showerror("Eliminado", "Se han eliminado las recetas seleccionadas anteriormente")

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

            if len(rutasCategorias) == 0:
                tkinter.messagebox.showerror("Error", "No hay categorías añadidas")

            else:
                if len(rutasCategorias) != 1:


                    start = time.time()
                    df_knn["Ficheros"], df_knn["Categorias"], df_textos_count["Carpeta"], df_textos_count[
                        "Total"], TotalRecetas = text_processing.process_text(rutasCategorias)

                    listaNombreCategoriasNumero = []

                    for i, j in df_textos_count.iterrows():
                        texto = self.ui.comboBoxCategorias.itemText(j["Carpeta"])
                        listaNombreCategoriasNumero.append(texto)

                    for i in range(len(listaNombreCategoriasNumero)):
                        df_textos_count["Carpeta"][i] = listaNombreCategoriasNumero[i]

                    model = pandas_table.DataFrameModel(df_textos_count)
                    self.ui.previewEntrenamiento.setModel(model)

                    self.ui.labelNumRecetasTotal.setText(str(TotalRecetas))

                    df_knn = text_processing.tratamientoBasico(df_knn)
                    df_knn = text_processing.quit_stopwords(df_knn)
                    df_knn = text_processing.stemming(df_knn)

                    df_algortimoKnn = df_knn

                    try:
                        df_matrix_confusion_knn, precisionKnn, sumaPositivos, sumaFalsosPositivos, modeloKnn = text_processing.calculate_weightKnn(
                            df_algortimoKnn)
                        end = time.time()

                        tiempoEjecuccion = end - start

                        final_modeloKnn = modeloKnn
                        modelosFinales[1] = final_modeloKnn

                        model = pandas_table.DataFrameModel(df_matrix_confusion_knn)
                        self.ui.matrizConfusionEntrenamiento.setModel(model)
                        self.ui.labelPrecisionAlgoritmo.setText(str(precisionKnn))

                        self.ui.labelTiempoEntrenamiento.setText(str(tiempoEjecuccion) + "s")

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

            if len(rutasCategorias) == 0:
                tkinter.messagebox.showerror("Error", "No hay categorías añadidas")
            else:

                if len(rutasCategorias) != 1:
                    start = time.time()
                    df_rf["Ficheros"], df_rf["Categorias"], df_textos_count["Carpeta"], df_textos_count[
                        "Total"], TotalRecetas = text_processing.process_text(rutasCategorias)

                    listaNombreCategoriasNumero = []

                    for i, j in df_textos_count.iterrows():
                        texto = self.ui.comboBoxCategorias.itemText(j["Carpeta"])
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
                        end = time.time()

                        tiempoEjecuccion = end - start

                        final_modeloRF = modeloRF
                        modelosFinales[2] = final_modeloRF

                        model = pandas_table.DataFrameModel(df_matrix_confusion_rf)
                        self.ui.matrizConfusionEntrenamiento.setModel(model)
                        self.ui.labelPrecisionAlgoritmo.setText(str(precisionRF))

                        self.ui.labelTiempoEntrenamiento.setText(str(tiempoEjecuccion) + "s")

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

                        self.figureCanvas.show()

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

            if len(rutasCategorias) == 0:
                tkinter.messagebox.showerror("Error", "No hay categorías añadidas")
            else:
                if len(rutasCategorias) != 1:
                    start = time.time()
                    df_nb["Ficheros"], df_nb["Categorias"], df_textos_count["Carpeta"], df_textos_count[
                        "Total"], TotalRecetas = text_processing.process_text(rutasCategorias)

                    listaNombreCategoriasNumero = []

                    for i, j in df_textos_count.iterrows():
                        texto = self.ui.comboBoxCategorias.itemText(j["Carpeta"])
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
                        end = time.time()

                        tiempoEjecuccion = end - start

                        final_modeloNB = modeloNB
                        modelosFinales[3] = final_modeloNB

                        model = pandas_table.DataFrameModel(df_matrix_confusion_nb)
                        self.ui.matrizConfusionEntrenamiento.setModel(model)
                        self.ui.labelPrecisionAlgoritmo.setText(str(precisionNB))

                        self.ui.labelTiempoEntrenamiento.setText(str(tiempoEjecuccion) + "s")

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

                        self.figureCanvas.show()
                    except Exception as e:
                        print(e)

                else:
                    tkinter.messagebox.showerror("Error", "Debe al menos seleccionar dos categorías")


    #############################################################################################

    # Funcion que guarda el fichero generado tras el entrenamiento
    def guardarModeloEntrenamiento(self):

        files = [('Model File', '*.pkl')]

        if len(modelosFinales) == 0:
            tkinter.messagebox.showerror("Error", "No se ha realizado ningún entrenamiento")
        else:

            if self.ui.algoritmoKnn.isChecked():

                model = modelosFinales[1]
                nombreFicheroGuardar = asksaveasfilename(filetypes=files)

                if nombreFicheroGuardar == "":
                    self.ui.txt_guardar_path.setText("")
                else:
                    joblib.dump(model, nombreFicheroGuardar + ".pkl")
                    self.ui.txt_guardar_path.setText(nombreFicheroGuardar)
                    tkinter.messagebox.showinfo("Información", "Modelo guardado correctamente")

            if self.ui.algortimoRandomForest.isChecked():

                model = modelosFinales[2]
                nombreFicheroGuardar = asksaveasfilename(filetypes=files)
                if nombreFicheroGuardar == "":
                    self.ui.txt_paths.setText("")
                else:
                    joblib.dump(model, nombreFicheroGuardar + ".pkl")
                    self.ui.txt_guardar_path.setText(nombreFicheroGuardar)
                    tkinter.messagebox.showinfo("Información", "Modelo guardado correctamente")

            if self.ui.algortimoNaiveBayes.isChecked():

                model = modelosFinales[3]
                nombreFicheroGuardar = asksaveasfilename(filetypes=files)
                if nombreFicheroGuardar == "":
                    self.ui.txt_guardar_path.setText("")
                else:
                    joblib.dump(model, nombreFicheroGuardar + ".pkl")
                    self.ui.txt_guardar_path.setText(nombreFicheroGuardar)
                    tkinter.messagebox.showinfo("Información", "Modelo guardado correctamente")

    #########################################################################################

    # VENTANA CLASIFICACION

    # Funcion que carga las categorias a clasificar
    def abrirRecetasClasificacion(self):

        selected_unlabeled = askdirectory()

        if not selected_unlabeled:
            self.ui.lineEdit.setText("")
        else:
            self.ui.lineEdit.setText(selected_unlabeled)

    # Funcion que carga el modelo a utilizar para clasificar
    def selecionarModelo(self):

        selected_model = askopenfilename()

        if not selected_model:
            self.ui.lineEdit_2.setText("")
        else:
            self.ui.lineEdit_2.setText(selected_model)

    # Funcion que clasifica las recetas y las predice
    def clasificarTextos(self):

        if self.ui.lineEdit.text() == "" or self.ui.lineEdit_2.text() == "":
            tkinter.messagebox.showerror("Error", "Rellene los campos necesarios")
        else:
            if not os.path.exists(os.path.dirname(self.ui.lineEdit.text())) or not os.path.exists(
                    self.ui.lineEdit_2.text()):
                tkinter.messagebox.showerror("Error", "Una de las rutas dadas no es válida")
            else:
                if self.ui.lineEdit_2.text().endswith(".pkl"):
                    todoTextos = True

                    contentFiles = os.listdir(self.ui.lineEdit.text())
                    for i in contentFiles:
                        if todoTextos == True:
                            if i.endswith(".txt"):
                                todoTextos = True
                            else:
                                todoTextos = False

                    if todoTextos == False:
                        tkinter.messagebox.showerror("Error", "La carpeta de recetas no contiene ficheros de texto")
                    else:

                        start = time.time()

                        listaRecetasUnlabeled = []
                        listaRecetasUnlabeledCategorias = []
                        listaRecetasUnlabeledContenido = []

                        df_recetasUnlabeled = pd.DataFrame(columns=['Ficheros', 'Categorias'])

                        numeroTotalRecetasUnlabeled = 0

                        categoriasPrediccion = []

                        contenidoRecetasUnlabeled = os.listdir(self.ui.lineEdit.text())

                        sorted_Recetas = natsort.natsorted(contenidoRecetasUnlabeled, reverse=False)
                        numeroTotalRecetasUnlabeled = len(sorted_Recetas)

                        for fichero in range(len(sorted_Recetas)):
                            listaRecetasUnlabeled.append(sorted_Recetas[fichero])
                            rutasUnlabeled[fichero] = self.ui.lineEdit.text() + "/" + sorted_Recetas[fichero]

                        for recetaUnlabeled in range(len(listaRecetasUnlabeled)):
                            contenidoReceta = open(
                                self.ui.lineEdit.text() + "/" + listaRecetasUnlabeled[recetaUnlabeled], "r",
                                encoding="ISO 8859-1")
                            listaRecetasUnlabeledContenido.append(contenidoReceta.read())
                            listaRecetasUnlabeledCategorias.append("Sin clasificar")

                        df_recetasUnlabeled["Ficheros"] = listaRecetasUnlabeledContenido
                        df_recetasUnlabeled["Categorias"] = listaRecetasUnlabeledCategorias

                        df_recetasUnlabeled = text_processing.tratamientoBasico(df_recetasUnlabeled)
                        df_recetasUnlabeled = text_processing.quit_stopwords(df_recetasUnlabeled)
                        df_recetasUnlabeled = text_processing.stemming(df_recetasUnlabeled)

                        cargaModelo = joblib.load(self.ui.lineEdit_2.text())

                        for i in range(len(df_recetasUnlabeled["Ficheros"])):
                            unidos = " ".join(df_recetasUnlabeled["Ficheros"][i])

                            df_recetasUnlabeled["Ficheros"][i] = str(unidos)

                        Y_pred = cargaModelo.predict(df_recetasUnlabeled['Ficheros'])
                        precisionClasificacion = cargaModelo.score(df_recetasUnlabeled['Ficheros'],
                                                                   df_recetasUnlabeled['Categorias'])


                        end = time.time()

                        tiempoEjecuccion = end - start

                        for prediccion in range(len(df_recetasUnlabeled["Categorias"])):
                            df_recetasUnlabeled["Categorias"][prediccion] = Y_pred[prediccion]

                        df_recetasUnlabeled["Ficheros"] = listaRecetasUnlabeled

                        listaNombresCategoriasPrediccion = []

                        for i in Y_pred:
                            nombreCategoria = self.ui.comboBoxCategorias.itemText(i)
                            categoriasPrediccion.append(nombreCategoria)
                            listaNombresCategoriasPrediccion.append(nombreCategoria)

                        for i in range(len(listaNombresCategoriasPrediccion)):
                            df_recetasUnlabeled["Categorias"][i] = listaNombresCategoriasPrediccion[i]

                        listaCategoriasUnicas = []
                        for x in categoriasPrediccion:
                            if x not in listaCategoriasUnicas:
                                listaCategoriasUnicas.append(x)

                        totalResultados = []
                        contadorFicheros = 0
                        for i in range(len(listaCategoriasUnicas)):
                            contadorFicheros = 0

                            for j in range(len(df_recetasUnlabeled["Categorias"])):
                                if listaCategoriasUnicas[i] == df_recetasUnlabeled["Categorias"][j]:
                                    contadorFicheros += 1

                            totalResultados.append(contadorFicheros)

                        cuentaTotal = 0
                        for total in totalResultados:
                            cuentaTotal += total

                        clasificadorFinal[0] = df_recetasUnlabeled
                        model = pandas_table.DataFrameModel(df_recetasUnlabeled)
                        self.ui.tableView.setModel(model)
                        self.ui.tableView.show()

                        self.figure = plt.figure(figsize=(5, 5))

                        self.figureCanvas = FigureCanvas(self.figure)

                        self.navigationToolbar = NavigationToolbar(self.figureCanvas, self)

                        layout = QtWidgets.QVBoxLayout()
                        layout.addWidget(self.navigationToolbar)
                        layout.addWidget(self.figureCanvas)
                        self.ui.graphicsView.setLayout(layout)
                        x = totalResultados
                        total = sum(x)
                        ax = self.figure.add_subplot(111)
                        ax.set_title("Total recetas clasificadas: " + str(cuentaTotal)+'\n' + "Tiempo Ejecucción: " + str(round(tiempoEjecuccion, 4))+'s')
                        ax.pie(x, labels=listaCategoriasUnicas, shadow=True,
                               autopct=lambda p: '{:.0f}'.format(p * total / 100), )

                        self.figureCanvas.draw()
                        self.figureCanvas.show()

                        self.ui.tableView.clicked.connect(self.obtainFileFromExplorer)

                else:
                    tkinter.messagebox.showerror("Error", "El fichero seleccionado no es un modelo con formato .pkl")


    # Funcion que al pulsar sobre una receta muestre su texto
    def obtainFileFromExplorer(self):

        index = self.ui.tableView.selectedIndexes()[0]

        for ruta in rutasUnlabeled:
            if index.row() == ruta:
                path = rutasUnlabeled[ruta]
                path = os.path.realpath(path)
                os.startfile(path)

    # Funcion que guarda los resultados de la clasificacion en varios formatos
    def guardarResultadosClasificacion(self):

        files = [('CSV', '*.csv'),
                 ('Excel', '*.xlsx'),
                 ('Fichero de texto', '*.txt')]

        if len(clasificadorFinal) == 0:
            tkinter.messagebox.showerror("Error", "No hay resultados para guardar")
        else:
            rutaResultadosGuardar = asksaveasfilename(defaultextension=".*", filetypes=files)

            if rutaResultadosGuardar == "":
                self.ui.lineEdit_3.setText("")
            else:
                self.ui.lineEdit_3.setText(rutaResultadosGuardar)
                if rutaResultadosGuardar.endswith(".csv"):
                    df_guardar = clasificadorFinal[0]
                    df_guardar.to_csv(rutaResultadosGuardar, sep=';', encoding='ISO 8859-1', index=False)

                    tkinter.messagebox.showinfo("Información", "Resultados guardados correctamente")
                elif rutaResultadosGuardar.endswith(".xlsx"):
                    df_guardar = clasificadorFinal[0]
                    df_guardar.to_excel(rutaResultadosGuardar)
                    tkinter.messagebox.showinfo("Información", "Resultados guardados correctamente")
                elif rutaResultadosGuardar.endswith(".txt"):
                    df_guardar = clasificadorFinal[0]
                    df_guardar.to_csv(rutaResultadosGuardar, sep=';', index=False)
                    tkinter.messagebox.showinfo("Información", "Resultados guardados correctamente")
                else:
                    tkinter.messagebox.showerror("Error", "El formato seleccionado no es válido")

    ##########################################################################

    # VENTANA MAPA

    # Funcion abre la receta que quiere analizar el usuario para mostrar sus ingredientes
    def abrirRecetaAnalizar(self):

        rutaRecetaAnalizar = askopenfilename()

        if not rutaRecetaAnalizar:
            self.ui.lineAbrirReceta.setText("")
        else:

            self.ui.lineAbrirReceta.setText(rutaRecetaAnalizar)

            if rutaRecetaAnalizar.endswith(".txt"):

                recetaContenido = []
                recetaCategoria = []
                df_recetaAnalizar = pd.DataFrame(columns=['Ficheros', 'Categorias'])

                with open(rutaRecetaAnalizar, "r", encoding="ISO 8859-1") as f:
                    recetaContenido.append(f.read())
                    recetaCategoria.append("Sin clasificar")

                df_recetaAnalizar["Ficheros"] = recetaContenido
                df_recetaAnalizar["Categorias"] = recetaCategoria

                df_recetaAnalizar = text_processing.tratamientoBasico(df_recetaAnalizar)
                df_recetaAnalizar = text_processing.quit_stopwords(df_recetaAnalizar)

                df_ingredientesReceta = pd.DataFrame(columns=['Ingredientes'])
                ruta = os.getcwd()
                data_folder = Path(ruta + "/ingredientes/")
                archivoAbir = data_folder / "listaIngredientes.txt"

                txt_ingredientes = open(archivoAbir, "r")
                ingredientesAComprobar = txt_ingredientes.read()

                listaIngredientesReceta = []

                for indiceDF, fila in df_recetaAnalizar.iterrows():
                    filtered_ingredient = [w for w in fila["Ficheros"] if w in ingredientesAComprobar]
                    listaIngredientesReceta.append(filtered_ingredient)

                listaIngredientesUnicos = []
                contadorFila = 0
                for x in range(len(listaIngredientesReceta)):
                    for y in range(len(listaIngredientesReceta[x])):
                        if listaIngredientesReceta[x][y] not in listaIngredientesUnicos:
                            listaIngredientesUnicos.append(listaIngredientesReceta[x][y])
                            diccionarioIngredientes[contadorFila] = listaIngredientesReceta[x][y]
                            contadorFila += 1


                df_ingredientesReceta["Ingredientes"] = listaIngredientesUnicos

                model = pandas_table.DataFrameModel(df_ingredientesReceta)
                self.ui.tablaIngredientesReceta.setModel(model)

                self.ui.tablaIngredientesReceta.clicked.connect(self.mirarIngrediente)

            else:
                tkinter.messagebox.showerror("Error", "El formato seleccionado no es válido, debe ser .txt")


    # Funcion que detecta que ingrediente ha pulsado el usuario
    def mirarIngrediente(self):

        index = self.ui.tablaIngredientesReceta.selectedIndexes()[0]

        for alimento in diccionarioIngredientes:
            if index.row() == alimento:
                ingredienteSeleccionado[0] = diccionarioIngredientes[alimento]
                historialIngredienteSeleccionado[alimento] = diccionarioIngredientes[alimento]

    # Funcion que abre una pagina web en el carrefour
    def abrirCarrefour(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        browser = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)

        sesionBuscador = ""

        if len(diccionarioIngredientes) == 0:
            try:
                # browser = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)
                browser.get(
                    "https://www.carrefour.es/supermercado?ic_source=portal&ic_medium=menu-links&ic_content=section-home")
            except Exception as e:
                print(e)


        else:

            if len(ingredienteSeleccionado) == 0:
                # browser = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)
                try:
                    browser.get(
                        "https://www.carrefour.es/supermercado?ic_source=portal&ic_medium=menu-links&ic_content=section"
                        "-home")
                except Exception as e:
                    print(e)

            else:
                print(ingredienteSeleccionado[0])
                ingredienteBuscar = ingredienteSeleccionado[0]
                # browser = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)

                try:
                    browser.get(
                        "https://www.carrefour.es/supermercado?ic_source=portal&ic_medium=menu-links&ic_content=section-home")
                    sesionBuscador = browser.session_id
                    time.sleep(4)
                    cookies = browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
                    cookies.click()
                    time.sleep(2)
                    boton_tuto_cerrar = browser.find_element(By.XPATH,
                                                             '//*[@id="app"]/div/nav/div[2]/div[1]/div/div/span')
                    boton_tuto_cerrar.click()
                    time.sleep(2)
                    time.sleep(2)
                    caja_busqueda = browser.find_element(By.XPATH, '//*[@id="search-input"]')
                    caja_busqueda.click()
                    time.sleep(2)
                    caja_busqueda2 = browser.find_element(By.XPATH, '//*[@id="empathy-x"]/header/div/div/input[3]')
                    caja_busqueda2.send_keys(ingredienteBuscar)
                    caja_busqueda2.send_keys(Keys.ENTER)
                    time.sleep(2)
                    sesionAnterior[0] = sesionBuscador

                except Exception as e:
                    print(e)


    # Funcion que abre una pagina web en el dia
    def abrirDia(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        browser = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)

        if len(diccionarioIngredientes) == 0:
            # browser = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)
            browser.get('https://www.dia.es/compra-online/')

        else:

            if len(ingredienteSeleccionado) == 0:
                # browser = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)
                browser.get('https://www.dia.es/compra-online/')
            else:

                browser.get('https://www.dia.es/compra-online/')

                ingredienteBuscar = ingredienteSeleccionado[0]
                time.sleep(5)
                cookies = browser.find_element(By.XPATH, '/html/body/div[10]/div[3]/div/div/div[2]/div[1]/div/button')
                cookies.click()
                time.sleep(2)
                buscador = browser.find_element(By.XPATH, '//*[@id="search"]')
                buscador.click()
                time.sleep(2)
                buscador.send_keys(ingredienteSeleccionado[0])
                buscador.send_keys(Keys.ENTER)
                time.sleep(2)

                sesionAnterior[1] = browser.session_id


    ##############################################################################################3333

    # Funcion que cierra la aplicacion y las ventanas que esten abiertas
    def closeEvent(self, event):
        try:
            self.Second_MainWindow.close()
            event.accept()
        except Exception as e:
            print(e)


##################################################################################33333
# Main de la aplicacion
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Hoja de estilos
    style_file = QFile("index.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())

    window = MainWindow()
    # Establecer un logo a la ventana
    window.setWindowIcon(QtGui.QIcon(r"ETEN_png.png"))
    window.show()

    sys.exit(app.exec_())
