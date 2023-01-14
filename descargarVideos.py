import tkinter
from pathlib import Path
import os
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
from pytube import YouTube
import moviepy.editor as mp
from pytube import Playlist





import word_Segmentation
import check_lenght_audio


# Titulo del video de Youtube
titulo_video = ""
# Titulo del video de Youtube sin caracteres especiales
nuevo_titulo = ""

archivo_selecionado = ""

# Obtiene el directorio en el que te encuentras
current_directory = os.getcwd()


# Crea una carpeta llamada recetas
final_directory = os.path.join(current_directory, r'recetas')

# Si la carpeta no existe la crea, sino no hace nada
if not os.path.exists(final_directory):
    os.makedirs(final_directory)
    # Comprueba que dentro de recetas no exista la carpeta transcripciones, si no existe la crea
    directorio_txt = os.path.join(final_directory, r'transcripciones')
    if not os.path.exists(directorio_txt):
        os.makedirs(directorio_txt)


# Funcion que descarga el video en el directorio en el que te encuentres
def downloadVideo(link_video):

    try:

        # Recoge el link y lo localiza en Youtube
        url = YouTube(str(link_video))
        # Obtiene el titulo del video
        titulo_video = url.title
        # Elimina los caracteres especiales del titulo del video
        nuevo_titulo = titulo_video.replace(',', '').replace('.', '').replace('!', '').replace('¡', '').replace('?',
                                                                                                                '').replace(
            '¿', '').replace('(', '').replace(')', '')
        # Obtiene el video con la mejor resolucion
        video = url.streams.get_highest_resolution()
        # Obtiene el path en el que te encuentras
        ruta = os.getcwd()

        # Descarga el video en el directorio de recetas
        video.download(ruta + "\\recetas")

        tkinter.messagebox.showinfo("Información", "El video se ha descargado correctamente")



    except Exception as e:
        tkinter.messagebox.showerror("Error", "Error a la hora de descargar el vídeo, compruebe que el link es correcto")


def open_file():

    try:
        # Se pide al usuario que seleccione un archivo
        doc_selected = askopenfilename()

        if not doc_selected:
            tkinter.messagebox.showerror("Error", "No ha seleccionado ningún vídeo")
        else:

            if doc_selected.endswith(".mp4"):

                # Se cambia el directorio a la carpeta de recetas
                os.chdir(final_directory)
                recetas = os.getcwd()


                # Se obtiene el nombre del archivo seleccionado
                archivo_selecionado = Path(doc_selected).stem

                # Se extrae del video el audio
                clip = mp.VideoFileClip(doc_selected)
                clip.audio.write_audiofile(recetas + '\\' + archivo_selecionado + '.wav')
                # Se fragmenta el audio y se crea el fichero .txt
                word_Segmentation.fragmentar_audio(archivo_selecionado)

                # Se vuelve al directorio principal
                os.chdir(current_directory)

                os.remove(recetas + '\\' + archivo_selecionado + '.wav')

                tkinter.messagebox.showinfo("Información", "El vídeo se ha procesado correctamente")


            else:
                tkinter.messagebox.showerror("Error", "El archivo seleccionado no es un video")
                os.chdir(current_directory)


    except Exception as e:
        tkinter.messagebox.showerror("Error", "Error a la hora de abrir el archivo")
        print(e)
        os.chdir(current_directory)



def download_listVideos(link_lista_videos):

    try:
        yt_list = Playlist(link_lista_videos)

        for video in yt_list.videos:
            nuevo_titulo = video.title.replace(',', '').replace('.', '').replace('!', '').replace('¡', '').replace('?',
                                                                                                                    '').replace(
                '¿', '').replace('(', '').replace(')', '')
            st = video.streams.get_highest_resolution()
            ruta = os.getcwd()
            st.download(ruta + "\\recetas")

        tkinter.messagebox.showinfo("Información", "Los videos se han descargado correctamente")
    except Exception as e:
        tkinter.messagebox.showerror("Error", "Error al encontrar la lista de reproducción, compruebe que el link es correcto")
