import os
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
                f = open(val[0] + '/' + sorted_files[j], "r", encoding="ANSI")

                listaRecetas.append(f.read())
                listaCategoria.append(i)


        except Exception as e:
            print(e)

    return listaRecetas, listaCategoria, listaCuentaCarpeta, listaCuentaFicheros, numeroTotalRecetas


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


# Funcion que aplica el stemming a la lista que se le pasa
def stemming(df_sinStemming):
    listaStemming = []
    lista_stem = []

    # Se establece el idioma
    stemmer = SnowballStemmer('spanish')

    for indiceDF, fila in df_sinStemming.iterrows():
        for word in range(len(fila["Ficheros"])):
            if word == 0:
                lista_stem.append(listaStemming)
                listaStemming = []
            else:
                w = stemmer.stem(fila["Ficheros"][word])
                listaStemming.append(w)

    for i in range(len(lista_stem)):
        df_sinStemming["Ficheros"][i] = lista_stem[i]

    return df_sinStemming












# Funcion que cuenta el numero de apariciones de cada palabra en cada receta y calcula su peso
def calculate_weightKnn(df_entrenamiento):
    listaUnidos = []
    for i in range(len(df_entrenamiento["Ficheros"])):
        unidos = " ".join(df_entrenamiento["Ficheros"][i])

        df_entrenamiento["Ficheros"][i] = str(unidos)

    X = df_entrenamiento['Ficheros']
    y = df_entrenamiento['Categorias']

    # We use a pipeline to vectorize the data, then apply tfidf, and fit a kNN model
    model_knn = Pipeline([('vect', CountVectorizer(lowercase=False, preprocessor=None, tokenizer=None, stop_words=None,
                                                   min_df=1)),
                          ('tfidf', TfidfTransformer()),
                          ('knn', KNeighborsClassifier())])

    # Fitting the model
    model_knn.fit(X, y)



    precisionKnn = round(model_knn.score(X, y), 4) * 100

    y_train_pred = model_knn.predict(X)
    cm_train = confusion_matrix(y, y_train_pred)

    df_matrix_confusion_entrenamiento = pd.DataFrame(cm_train)

    sumaPositivos = 0
    sumaFalsosPositivos = 0

    for i in range(len(df_matrix_confusion_entrenamiento)):
        for j in range(len(df_matrix_confusion_entrenamiento[i])):
            if i == j:
                sumaPositivos += df_matrix_confusion_entrenamiento[i][j]
            else:
                sumaFalsosPositivos += df_matrix_confusion_entrenamiento[i][j]

    return df_matrix_confusion_entrenamiento, precisionKnn, sumaPositivos, sumaFalsosPositivos, model_knn


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
    precisionRF = round(model_rf.score(X, y), 4) * 100

    y_train_pred = model_rf.predict(X)
    cm_train = confusion_matrix(y, y_train_pred)

    df_matrix_confusion_entrenamiento = pd.DataFrame(cm_train)

    sumaPositivos = 0
    sumaFalsosPositivos = 0

    for i in range(len(df_matrix_confusion_entrenamiento)):
        for j in range(len(df_matrix_confusion_entrenamiento[i])):
            if i == j:
                sumaPositivos += df_matrix_confusion_entrenamiento[i][j]
            else:
                sumaFalsosPositivos += df_matrix_confusion_entrenamiento[i][j]

    return df_matrix_confusion_entrenamiento, precisionRF, sumaPositivos, sumaFalsosPositivos, model_rf


def calculate_weightNB(df_entrenamiento):
    listaUnidos = []
    for i in range(len(df_entrenamiento["Ficheros"])):
        unidos = " ".join(df_entrenamiento["Ficheros"][i])

        df_entrenamiento["Ficheros"][i] = str(unidos)

    X = df_entrenamiento['Ficheros']
    y = df_entrenamiento['Categorias']

    # We use a pipeline to vectorize the data, then apply tfidf, and fit a kNN model
    model_nb = Pipeline([('vect', CountVectorizer(lowercase=False, preprocessor=None, tokenizer=None, stop_words=None,
                                                  min_df=1)),
                         ('tfidf', TfidfTransformer()),
                         ('nb', MultinomialNB())])

    # Fitting the model
    model_nb.fit(X, y)

    precisionNB = round(model_nb.score(X, y), 4) * 100

    y_train_pred = model_nb.predict(X)
    cm_train = confusion_matrix(y, y_train_pred)

    df_matrix_confusion_entrenamiento = pd.DataFrame(cm_train)

    sumaPositivos = 0
    sumaFalsosPositivos = 0

    for i in range(len(df_matrix_confusion_entrenamiento)):
        for j in range(len(df_matrix_confusion_entrenamiento[i])):
            if i == j:
                sumaPositivos += df_matrix_confusion_entrenamiento[i][j]
            else:
                sumaFalsosPositivos += df_matrix_confusion_entrenamiento[i][j]

    return df_matrix_confusion_entrenamiento, precisionNB, sumaPositivos, sumaFalsosPositivos, model_nb
