
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

titulo_video = ""


def download():
    url = YouTube(str(link.get())) #This captures the link(url) and locates it from YouTube.
    titulo_video = url.title
    print(titulo_video)
    video = url.streams.get_highest_resolution()
    ruta = os.getcwd()
    video.download(ruta) # This is the method with the instruction to download the video.
    Label(root, text="Downloaded", font="arial 15").place(x=100, y=120) #Once the video is downloaded, this label `downloaded` is displayed to show dowload completion.

    clip = mp.VideoFileClip(titulo_video + '.mp4')
    clip.audio.write_audiofile(titulo_video + '.wav')

    i = 0

    myaudio = AudioSegment.from_file(titulo_video + ".wav", "wav")
    chunk_length_ms = 15000
    chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of one sec
    for i, chunk in enumerate(chunks):
        chunk_name = "{0}.wav".format(i)
        print("exporting", chunk_name)
        chunk.export(chunk_name, format="wav")

    for j in range(i + 1):

        r = sr.Recognizer()
        # r.energy_threshold = 300
        audio = sr.AudioFile(str(j) + '.wav')

        with audio as source:
            # r.adjust_for_ambient_noise(source, duration=1)
            audio_file = r.record(source)

            try:
                # text = r.recognize_google(audio_file, language='en')
                text = r.recognize_google(audio_file, language='es')
                print(text)
                # to_translate = text
                # translated = GoogleTranslator(source='auto', target='es').translate(to_translate)

                # Open a file with access mode 'a'
                with open(titulo_video + ".txt", "a") as receta_txt:
                    # Append 'hello' at the end of file
                    receta_txt.write(text + " ")

                # print(translated)
            except Exception as e:
                print("Error")
                print(e)

    for z in range(i+1):
        if os.path.exists(str(z)+".wav"):
            os.remove(str(z)+".wav")
        else:
            print("The file does not exist")





root = Tk()
root.geometry("500x300")
root.resizable(0, 0) # makes the window adjustable with its features
root.title('youtube downloader')

Label(root, text="Download Youtube videos for free", font='san-serif 14 bold').pack()
link = StringVar() # Specifying the variable type
Label(root, text="Paste your link here", font='san-serif 15 bold').place(x=150, y=55)
link_enter = Entry(root, width=70, textvariable=link).place(x=30, y=85)

Button(root, text='Download', font='san-serif 16 bold', bg='red', padx=2,command=download).place(x=175, y=150)


root.mainloop()


