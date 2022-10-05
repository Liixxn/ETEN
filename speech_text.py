
# #import library
# import speech_recognition as sr
# #Initiаlize  reсоgnizer  сlаss  (fоr  reсоgnizing  the  sрeeсh)
# r = sr.Recognizer()
# # Reading Audio file as source
# #  listening  the  аudiо  file  аnd  stоre  in  аudiо_text  vаriаble
# with sr.AudioFile('Juego.mp4') as source:
#     audio_text = r.listen(source)
# # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
#     try:
#         # using google speech recognition
#         text = r.recognize_google(audio_text)
#         print('Converting audio transcripts into text ...')
#         print(text)
#     except:
#          print('Sorry.. run again...')




import speech_recognition as sr
from deep_translator import *
# from deep_translator import GoogleTranslator
from language_detector import detect_language
import moviepy.editor as mp

video = "pasta2"

clip = mp.VideoFileClip(video+'.mp4')
clip.audio.write_audiofile(video+'.wav')

r = sr.Recognizer()
# r.energy_threshold = 400
audio = sr.AudioFile(video+'.wav')

with audio as source:
  r.adjust_for_ambient_noise(source, duration=1)
  audio_file = r.record(source)


  try:
    text = r.recognize_google(audio_file, language='en')
    print(text)
    to_translate = text
    translated = GoogleTranslator(source='auto', target='es').translate(to_translate)
    print(translated)
  except Exception as e:
    print("Error")
    print(e)




