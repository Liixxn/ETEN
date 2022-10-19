
from tkinter import *
import os
from pytube import YouTube
import speech_recognition as sr
from deep_translator import *
from deep_translator import GoogleTranslator
from language_detector import detect_language
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.utils import make_chunks

# Titulo del video de Youtube
titulo_video = ""

# Funcion que descarga el video en el directorio en el que te encuentres
def download():
    # Recoge el link y lo localiza en Youtube
    url = YouTube(str(link.get()))
    # Obtiene el titulo del video
    titulo_video = url.title
    # Obtiene el video con la mejor resolucion
    video = url.streams.get_highest_resolution()
    # Obtiene el path en el que te encuentras
    ruta = os.getcwd()
    # Descarga el video
    video.download(ruta)
    # Una vez se ha completado la descarga despliega un mensaje de "descargado"
    Label(root, text="Downloaded", font="arial 15").place(x=100, y=120)


    # Convierte el video descargado con formato .mp4 a audio con formato .wav
    clip = mp.VideoFileClip(titulo_video + '.mp4')
    clip.audio.write_audiofile(titulo_video + '.wav')


    # iterador para recorrer las diferentes particiones
    i = 0

    # audio a utilizar y su respectivo formato
    myaudio = AudioSegment.from_file(titulo_video + ".wav", "wav")
    # longitud de los audios -- 10s
    chunk_length_ms = 10000

    # Se crean los chunks
    chunks = make_chunks(myaudio, chunk_length_ms)
    # Cada chunk se guarda con un numero en formato .wav
    for i, chunk in enumerate(chunks):
        chunk_name = "{0}.wav".format(i)
        print("exporting", chunk_name)
        chunk.export(chunk_name, format="wav")

    # Se recorren esos audios para ser reconozidos
    for j in range(i + 1):

        r = sr.Recognizer()
        # r.energy_threshold = 300 // Establecer un minimo de decibelios
        audio = sr.AudioFile(str(j) + '.wav')

        with audio as source:
            # r.adjust_for_ambient_noise(source, duration=1) //Reajustar para el sonido ambiente
            audio_file = r.record(source)

            # Reconoce el texto y lo guarda en una variable
            try:
                # text = r.recognize_google(audio_file, language='en')
                text = r.recognize_google(audio_file, language='es')
                print(text)
                # to_translate = text
                # translated = GoogleTranslator(source='auto', target='es').translate(to_translate)

                # Crea un fichero en el que se escriben las lineas de texto obtenidas del audio
                with open(titulo_video + ".txt", "a") as receta_txt:
                    receta_txt.write(text + " ")

                # print(translated)
            except Exception as e:
                print("Error")
                print(e)

    # Una vez terminado el .txt elimina cada chunk creado
    for z in range(i+1):
        if os.path.exists(str(z)+".wav"):
            os.remove(str(z)+".wav")
        else:
            print("El archivo que busca no existe")





root = Tk()
root.geometry("500x300")
# Hace que la ventana se pueda ajustar
root.resizable(0, 0)
root.title('youtube downloader')

Label(root, text="Download Youtube videos for free", font='san-serif 14 bold').pack()
link = StringVar() # Specifying the variable type
Label(root, text="Paste your link here", font='san-serif 15 bold').place(x=150, y=55)
link_enter = Entry(root, width=70, textvariable=link).place(x=30, y=85)
# Cuando se pulsa sobre el boton la funcion download se ejecuta
Button(root, text='Download', font='san-serif 16 bold', bg='red', padx=2,command=download).place(x=175, y=150)

root.mainloop()


