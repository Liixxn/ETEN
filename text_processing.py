import os
import natsort
import numpy as np
from tkinter.filedialog import askopenfilename, askdirectory
from pathlib import Path
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
import re
from nltk import word_tokenize, RegexpTokenizer
from nltk.stem import PorterStemmer
import natsort
from nltk.stem import SnowballStemmer
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd
from sklearn.model_selection import train_test_split

pd.options.mode.chained_assignment = None

listaRecetas = []
listaCategoria = []


df_counts = pd.DataFrame(columns=["Carpeta Categorias", "Total"])

def process_text(rutasCategorias):
    for i, val in rutasCategorias.items():

        try:
            dirFiles = os.listdir(val[0])

            sorted_files = natsort.natsorted(dirFiles, reverse=False)

            print("Numero de carpetas: ", len(rutasCategorias))
            print("Para la carpeta ", rutasCategorias[i])
            print("Numero de recetas: ", len(sorted_files))

            df_counts.append(rutasCategorias[i], len(sorted_files))


            for j in range(len(sorted_files)):
                f = open(val[0] + '/' + sorted_files[j], "r", encoding="ANSI")

                listaRecetas.append(f.read())
                listaCategoria.append(i)



        except Exception as e:
            print(e)

    return listaRecetas, listaCategoria, df_counts


def tratamientoBasico(df_sinTratar):
    listatokens = []
    print("Aqui")
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
        txt_stopwords = open("stop_words_spanish.txt", "r")
        stop_words = txt_stopwords.read()

        filtered_sentence = []

        for indiceDF, fila in df_conStopwords.iterrows():
            filtered_sentence = [w for w in fila["Ficheros"] if not w in stop_words]
            listaStopwords.append(filtered_sentence)

        for i in range(len(listaStopwords)):
            df_conStopwords["Ficheros"][i] = listaStopwords[i]

    except Exception as e:
        print("Error al abrir el el fichero de stopwords")
        print(e)

    return df_conStopwords


# Funcion que aplica el stemming a la lista que se le pasa
def stemming(df_sinStemming):
    listaStemming = []
    lista_stem = []

    print("llega stemming")
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
def calculate_weight(df_category):
    # Lista que guardara las palabras unidas de cada receta
    list_joined = []

    lista_count = []

    # Se crea el objeto que cuenta el numero de apariciones
    vec_weight = CountVectorizer(analyzer='word', lowercase=False, preprocessor=None, tokenizer=None, stop_words=None,
                                 min_df=1)

    X_train, X_test, Y_train, Y_test = train_test_split(df_category["Ficheros"], df_category["Categorias"],
                                                        test_size=0.2)
    Y_train = list(Y_train)
    print(X_train)
    # Ahora vecrtorizamos X_train y X_cv para poder meterlo en el modelo de clasificación
    # Set de entrenamiento
    arrayTemp = []
    for i, j in enumerate(X_train):
        arrayTemp.append(" ".join(j))
        print(arrayTemp)
    X_train = vec_weight.fit_transform(arrayTemp)
    X_train = X_train.toarray()

    print(X_train)

    # # Se recorre la lista y se unen las palabras de cada receta con un espacio entre medias
    # for i in range(len(list_category)):
    #
    #     print(list_category[i])
    #     joined = " ".join(list_category[i])
    #
    #
    #     list_joined.append(joined)
    #
    # print(list_joined)
    # # Se ejecuta el countVectorizer
    # matrix_count = vec_weight.fit_transform(list_joined)
    # print(matrix_count.shape)
    # # Se pasa a array
    # array_matrix_count = matrix_count.toarray()
    #
    # # Se pasan los datos a una tabla para su visualizacion
    # df_weight = pd.DataFrame(data=array_matrix_count, columns=vec_weight.get_feature_names_out())
    # #print(df_weight)
    #
    #
    #
    # tfi = TfidfTransformer()
    # matrix_tfi = tfi.fit_transform(array_matrix_count)
    # print(matrix_tfi.shape)
    # array_matrix_tfi = matrix_tfi.toarray()
    #
    # df_tfi = pd.DataFrame(data=array_matrix_tfi, columns=vec_weight.get_feature_names_out())
    # print(df_tfi)
    # print(array_matrix_tfi)
    #
    # # La matriz tiene que ser de 3 dimensiones en este caso, tiene que tener el mismo tamanio que las opciones
    # # En este caso es 7, por lo que tendria que haber 7 recetas en la 2nd dimension del array de rutas
    # # es decir [1º dimension, las categorias (seran 7) [ 2ºnd dimension los txt de cada categoria (numero que sea
    # # [ 3º dimension, las palabras de cada receta (numero que sea)]   2ºnd dimesnion  ]    3º dimension ]
    # clf = MultinomialNB().fit(array_matrix_tfi, options)
