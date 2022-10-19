
import speech_recognition as sr
from deep_translator import *
# from deep_translator import GoogleTranslator
from language_detector import detect_language
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.utils import make_chunks
import os


# nombre del audio el cual se va a analizar
video = "Tortilla de patatas - Receta de cocina española"

# Convierte el video descargado con formato .mp4 a audio con formato .wav
clip = mp.VideoFileClip(video + '.mp4')
clip.audio.write_audiofile(video + '.wav')

# iterador para recorrer las diferentes particiones
i = 0

# audio a utilizar y su respectivo formato
myaudio = AudioSegment.from_file(video+".wav", "wav")
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
for j in range(i+1):

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
            with open(video+".txt", "a") as receta_txt:
                receta_txt.write(text + " ")



            # print(translated)
        except Exception as e:
            print("Error")
            print(e)

# # Una vez terminado el .txt elimina cada chunk creado
# for z in range(i + 1):
#     if os.path.exists(str(z) + ".wav"):
#         os.remove(str(z) + ".wav")
#     else:
#         print("El archivo que busca no existe")
