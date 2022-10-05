import speech_recognition as sr
from deep_translator import GoogleTranslator
from language_detector import detect_language
import moviepy.editor as mp

video = "garlic"

r = sr.Recognizer()
audio = sr.AudioFile(video+'.wav')

with audio as source:
  audio_file = r.record(source)

  try:
    text = r.recognize_google_cloud(audio_file, language='en')
    print(text)
  except Exception as e:
    print("Error")
    print(e)
