import os
import numpy as np
from pathlib import Path
from nltk import word_tokenize, RegexpTokenizer
import natsort
from nltk.stem import SnowballStemmer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

pd.options.mode.chained_assignment = None

# Funcion que procesa los textos pasados y devuelve un dataframe con los textos leidos ademas de otra informacion
# como el numero de carpetas totales etc
def process_text(rutasCategorias):
    listaRecetas = []
    listaCategoria = []
    listaCuentaCarpeta = []
    listaCuentaFicheros = []
    numeroTotalRecetas = 0

    for i, val in rutasCategorias.items():

        try:
            dirFiles = os.listdir(val[0])

            sorted_files = natsort.natsorted(dirFiles, reverse=False)

            listaCuentaCarpeta.append(i)
            listaCuentaFicheros.append(len(sorted_files))
            numeroTotalRecetas += len(sorted_files)

            for j in range(len(sorted_files)):
                f = open(val[0] + '/' + sorted_files[j], "r", encoding="ISO 8859-1")

                listaRecetas.append(f.read())
                listaCategoria.append(i)


        except Exception as e:
            print(e)

    return listaRecetas, listaCategoria, listaCuentaCarpeta, listaCuentaFicheros, numeroTotalRecetas


# Funcion que pasa a minusculas y elimina los signos de puntuacion
def tratamientoBasico(df_sinTratar):
    listatokens = []

    for indiceDF, fila in df_sinTratar.iterrows():
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(fila["Ficheros"])
        listatokens.append(tokens)

    for i in range(len(listatokens)):
        listatokens[i] = [w.lower() for w in listatokens[i]]
        df_sinTratar["Ficheros"][i] = listatokens[i]

    return df_sinTratar


# Funcion que aplica las stopwords al datafram que se le pasa
def quit_stopwords(df_conStopwords):
    listaStopwords = []
    try:
        # Se carga en fichero de las stopwords
        ruta = os.getcwd()
        data_folder = Path(ruta + "/stopwords/")
        archivoAbir = data_folder / "stop_words_spanish.txt"

        txt_stopwords = open(archivoAbir, "r")
        stop_words = txt_stopwords.read()

        filtered_sentence = []

        for indiceDF, fila in df_conStopwords.iterrows():
            filtered_sentence = [w for w in fila["Ficheros"] if not w in stop_words]
            listaStopwords.append(filtered_sentence)

        for i in range(len(listaStopwords)):
            df_conStopwords["Ficheros"][i] = listaStopwords[i]

    except Exception as e:
        print(e)

    return df_conStopwords


# Funcion que aplica el stemming al dataframe que se le pasa
def stemming(df_sinStemming):
    listaStemming = []
    lista_stem = []

    # Se establece el idioma
    stemmer = SnowballStemmer('spanish')

    for indiceDF, fila in df_sinStemming.iterrows():
        if indiceDF != 0:
            lista_stem.append(listaStemming)
            listaStemming = []

        for word in range(len(fila["Ficheros"])):
            w = stemmer.stem(fila["Ficheros"][word])
            listaStemming.append(w)

    for i in range(len(lista_stem)):
        df_sinStemming["Ficheros"][i] = lista_stem[i]

    return df_sinStemming





# Funcion que cuenta el numero de apariciones de cada palabra en cada receta y calcula su peso con Knn

def calculate_weightKnn(df_entrenamiento):
    listaUnidos = []
    for i in range(len(df_entrenamiento["Ficheros"])):
        unidos = " ".join(df_entrenamiento["Ficheros"][i])

        df_entrenamiento["Ficheros"][i] = str(unidos)

    X = df_entrenamiento['Ficheros']
    y = df_entrenamiento['Categorias']


    model_knn = Pipeline([('vect', CountVectorizer(lowercase=False, preprocessor=None, tokenizer=None, stop_words=None,
                                                   min_df=1)),
                          ('tfidf', TfidfTransformer()),
                          ('knn', KNeighborsClassifier())])


    model_knn.fit(X, y)


    precisionKnn = round(model_knn.score(X, y) * 100, 2)

    y_train_pred = model_knn.predict(X)

    cm_train = confusion_matrix(y, y_train_pred)

    df_matrix_confusion_entrenamiento = pd.DataFrame(cm_train)

    sumaPositivos = 0
    sumaFalsosPositivos = 0

    # Obtener los resultados de la matriz de confusion
    for i in range(len(df_matrix_confusion_entrenamiento)):
        for j in range(len(df_matrix_confusion_entrenamiento[i])):
            if i == j:
                sumaPositivos += df_matrix_confusion_entrenamiento[i][j]
            else:
                sumaFalsosPositivos += df_matrix_confusion_entrenamiento[i][j]

    df_matrix_confusion_precision_recall = df_matrix_confusion_entrenamiento.copy()

    listaPrecision = []
    listaRecall = []

    # suma de diagonal
    true_pos = np.diag(df_matrix_confusion_precision_recall)
    # suma de columnas
    false_pos = np.sum(df_matrix_confusion_precision_recall, axis=0) - true_pos
    # suma de filas
    false_neg = np.sum(df_matrix_confusion_precision_recall, axis=1) - true_pos

    for i in range(len(df_matrix_confusion_precision_recall)):
        recallCategoria = round((true_pos[i] / (true_pos[i] + false_pos[i])) * 100, 2)
        listaRecall.append(recallCategoria)
        precisionlCategoria = round((true_pos[i] / (true_pos[i] + false_neg[i])) * 100, 2)
        listaPrecision.append(precisionlCategoria)


    df_matrix_confusion_precision_recall["Precision"] = listaPrecision
    ultimoIndice = df_matrix_confusion_precision_recall.index[-1]
    df_matrix_confusion_precision_recall["Recall"] = listaRecall




    return df_matrix_confusion_precision_recall, precisionKnn, sumaPositivos, sumaFalsosPositivos, model_knn



# Funcion que cuenta el numero de apariciones de cada palabra en cada receta y calcula su peso con Random Forest

def calculate_weightRF(df_entrenamiento):
    listaUnidos = []
    for i in range(len(df_entrenamiento["Ficheros"])):
        unidos = " ".join(df_entrenamiento["Ficheros"][i])

        df_entrenamiento["Ficheros"][i] = str(unidos)

    X = df_entrenamiento['Ficheros']
    y = df_entrenamiento['Categorias']

    model_rf = Pipeline([('vect', CountVectorizer(lowercase=False, preprocessor=None, tokenizer=None, stop_words=None,
                                                  min_df=1)),
                         ('tfidf', TfidfTransformer()),
                         ('rf', RandomForestClassifier())])

    model_rf.fit(X, y)
    precisionRF = round(model_rf.score(X, y) * 100, 2)

    y_train_pred = model_rf.predict(X)
    cm_train = confusion_matrix(y, y_train_pred)

    df_matrix_confusion_entrenamiento = pd.DataFrame(cm_train)

    sumaPositivos = 0
    sumaFalsosPositivos = 0



    # Obtener los resultados de la matriz de confusion
    for i in range(len(df_matrix_confusion_entrenamiento)):
        for j in range(len(df_matrix_confusion_entrenamiento[i])):
            if i == j:
                sumaPositivos += df_matrix_confusion_entrenamiento[i][j]
            else:
                sumaFalsosPositivos += df_matrix_confusion_entrenamiento[i][j]

    df_matrix_confusion_precision_recall = df_matrix_confusion_entrenamiento.copy()

    listaPrecision = []
    listaRecall = []

    # suma de diagonal
    true_pos = np.diag(df_matrix_confusion_precision_recall)
    # suma de columnas
    false_pos = np.sum(df_matrix_confusion_precision_recall, axis=0) - true_pos
    # suma de filas
    false_neg = np.sum(df_matrix_confusion_precision_recall, axis=1) - true_pos



    for i in range(len(df_matrix_confusion_precision_recall)):
        recallCategoria = round((true_pos[i] / (true_pos[i] + false_pos[i]))*100, 2)
        listaRecall.append(recallCategoria)
        precisionlCategoria = round((true_pos[i] / (true_pos[i] + false_neg[i]))*100, 2)
        listaPrecision.append(precisionlCategoria)



    df_matrix_confusion_precision_recall["Precision"] = listaPrecision
    ultimoIndice = df_matrix_confusion_precision_recall.index[-1]
    df_matrix_confusion_precision_recall["Recall"] = listaRecall





    return df_matrix_confusion_precision_recall, precisionRF, sumaPositivos, sumaFalsosPositivos, model_rf



# Funcion que cuenta el numero de apariciones de cada palabra en cada receta y calcula su peso con Naive Bayes

def calculate_weightNB(df_entrenamiento):
    listaUnidos = []
    for i in range(len(df_entrenamiento["Ficheros"])):
        unidos = " ".join(df_entrenamiento["Ficheros"][i])

        df_entrenamiento["Ficheros"][i] = str(unidos)

    X = df_entrenamiento['Ficheros']
    y = df_entrenamiento['Categorias']

    model_nb = Pipeline([('vect', CountVectorizer(lowercase=False, preprocessor=None, tokenizer=None, stop_words=None,
                                                  min_df=1)),
                         ('tfidf', TfidfTransformer()),
                         ('nb', MultinomialNB())])

    model_nb.fit(X, y)

    precisionNB = round(model_nb.score(X, y) * 100, 2)

    y_train_pred = model_nb.predict(X)
    cm_train = confusion_matrix(y, y_train_pred)

    df_matrix_confusion_entrenamiento = pd.DataFrame(cm_train)

    sumaPositivos = 0
    sumaFalsosPositivos = 0

    # Obtener los resultados de la matriz de confusion
    for i in range(len(df_matrix_confusion_entrenamiento)):
        for j in range(len(df_matrix_confusion_entrenamiento[i])):
            if i == j:
                sumaPositivos += df_matrix_confusion_entrenamiento[i][j]
            else:
                sumaFalsosPositivos += df_matrix_confusion_entrenamiento[i][j]

    df_matrix_confusion_precision_recall = df_matrix_confusion_entrenamiento.copy()

    listaPrecision = []
    listaRecall = []

    # suma de diagonal
    true_pos = np.diag(df_matrix_confusion_precision_recall)
    # suma de columnas
    false_pos = np.sum(df_matrix_confusion_precision_recall, axis=0) - true_pos
    # suma de filas
    false_neg = np.sum(df_matrix_confusion_precision_recall, axis=1) - true_pos

    for i in range(len(df_matrix_confusion_precision_recall)):
        recallCategoria = round((true_pos[i] / (true_pos[i] + false_pos[i])) * 100, 2)
        listaRecall.append(recallCategoria)
        precisionlCategoria = round((true_pos[i] / (true_pos[i] + false_neg[i])) * 100, 2)
        listaPrecision.append(precisionlCategoria)


    df_matrix_confusion_precision_recall["Precision"] = listaPrecision
    ultimoIndice = df_matrix_confusion_precision_recall.index[-1]
    df_matrix_confusion_precision_recall["Recall"] = listaRecall



    return df_matrix_confusion_precision_recall, precisionNB, sumaPositivos, sumaFalsosPositivos, model_nb
