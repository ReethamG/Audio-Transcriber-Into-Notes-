import speech_recognition as sr


def getAudio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)

        with open('audioResults.wav', 'wb') as f:
            f.write(audio.get_wav_data())
