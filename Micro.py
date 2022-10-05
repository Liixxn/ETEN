import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Record: ")
    # read the audio data from the default microphone
    audio_data = r.listen(source)
    print("Recognizing...")
    # convert speech to text
    text = r.recognize_google(audio_data, language="en")
    print(text)



