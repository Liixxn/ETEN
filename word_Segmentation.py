import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import tkinter
import tkinter.messagebox
import check_lenght_audio


def fragmentar_audio(audio_selected):
    sound_file = AudioSegment.from_wav(audio_selected + '.wav')

    ruta_transcripts = os.getcwd() + '\\transcripciones'
    # Se utiliza el directorio transcripciones para guardar los ficheros .txt
    os.chdir(ruta_transcripts)
    # Si el texto existe se eliminara
    if os.path.exists(ruta_transcripts + "\\" + audio_selected + '.txt'):
        os.remove(ruta_transcripts + "\\" + audio_selected + '.txt')

    # Se obtienen los decibelios del video
    dBFS = sound_file.dBFS

    # Divide el audio en silencios de 300ms y deja un silencio al final del audio
    audio_chunks = split_on_silence(sound_file, min_silence_len=300, silence_thresh=dBFS - 16, keep_silence=1000)

    # Se crean los chunks de audio
    for i, chunk in enumerate(audio_chunks):

        out_file = "chunk{0}.wav".format(i)

        chunk.export(out_file, format="wav")



        fragmento = AudioSegment.from_file(out_file)
        if fragmento.duration_seconds > 15:
            check_lenght_audio.comprobar_largo_audio(out_file, audio_selected)
        else:
            r = sr.Recognizer()
            # r.energy_threshold = 400
            audio = sr.AudioFile(out_file)

            with audio as source:
                audio_file = r.record(source)

                try:
                    # Reconoce el texto del auido
                    text = r.recognize_google(audio_file, language='es')


                    # Crea un arvhivo de texto con el nombre del video
                    with open(audio_selected + '.txt', "a") as receta_txt:
                        # Aniade el texto al final del archivo
                        receta_txt.write(text + " ")

                except Exception as e:
                    print(e)

        # Se elimina el chunk una vez se analiza
        if os.path.exists(out_file):
            os.remove(out_file)
        else:
            tkinter.messagebox.showerror("Error", "El archivo que busca no existe")

