import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    print(f"ID: {voice.id}\nNome: {voice.name}\nIdioma: {voice.languages}\n")
    engine.setProperty('voice', voice.id)  # Ex: 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MicrosoftHelena'
    engine.say("Texto a ser falado com a voz natural.")
    engine.runAndWait()

# engine.setProperty('voice', voices[2].id)
