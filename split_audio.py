
import speech_recognition as sr
from deep_translator import *
# from deep_translator import GoogleTranslator
from language_detector import detect_language
import moviepy.editor as mp


from pydub import AudioSegment
from pydub.utils import make_chunks

video = "espaguetis"

i = 0

myaudio = AudioSegment.from_file(video+".wav", "wav")
chunk_length_ms = 20000
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec
for i, chunk in enumerate(chunks):
    chunk_name = "{0}.wav".format(i)
    print ("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")


for j in range(i+1):

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
            with open(video+".txt", "a") as receta_txt:
                # Append 'hello' at the end of file
                receta_txt.write(text + " ")



            # print(translated)
        except Exception as e:
            print("Error")
            print(e)




