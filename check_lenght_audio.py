import os
import tkinter.messagebox
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import tkinter


def comprobar_largo_audio(fragmento, nombre_audio):


    sound = AudioSegment.from_file(fragmento)

    dBFS = sound.dBFS


    # Divide el audio en silencios de 300ms y deja un silencio al final del audio
    audio_chunks = split_on_silence(sound, min_silence_len=300, silence_thresh=dBFS-8, keep_silence=2000)

    # Se crean los chunks de audio
    for i, chunk in enumerate(audio_chunks):

        out_file = "sub_chunk{0}.wav".format(i)

        chunk.export(out_file, format="wav")

        r = sr.Recognizer()

        audio = sr.AudioFile(out_file)

        with audio as source:
            audio_file = r.record(source)

            try:
                # Reconoce el texto del auido
                text = r.recognize_google(audio_file, language='es')

                # Crea un arvhivo de texto con el nombre del video
                with open(nombre_audio + '.txt', "a") as receta_txt:
                    # Aniade el texto al final del archivo
                    receta_txt.write(text + " ")

            except Exception as e:
                print(e)

        # Se elimina el chunk una vez se analiza
        if os.path.exists(out_file):
            os.remove(out_file)
        else:
            tkinter.messagebox.showerror("Error", "El archivo que busca no existe")

    receta_txt.close()


