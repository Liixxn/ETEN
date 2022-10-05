from deep_translator import GoogleTranslator
import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Record: ")
    # read the audio data from the default microphone
    audio_data = r.listen(source)
    print("Recognizing...")
    # convert speech to text
    text = r.recognize_google(audio_data, language="es-ES")
    print(text)


to_translate = text
translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
print(translated)



# with sr.Microphone() as source:
#   print('Di cualquier cosa : ')
#   audio = r.listen(source)
#
#   try:
#     text = r.recognize_google(audio, language='en-EN')
#     print('Has dicho: {}'.format(text))
#
#     to_translate = text
#     translated = GoogleTranslator(source='auto', target='es').translate(to_translate)
#     print(translated)
#
#   except:
#     print('Lo siento, no he entendido')


