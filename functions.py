from os import truncate
from isort import file
import speech_recognition as sr
from pydub import AudioSegment
from tkinter import filedialog as fd


def inputOrRecord():
    fileInputOrMicro = int(input(
        "Do you want to input a file OR do you want to use the microphone and record? (1/2)"))

    return fileInputOrMicro


def getAudioUsingMicro():
    print("Start using your microphone \n")

    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)

        with open('audioResultsInWavForm.wav', 'wb') as f:
            f.truncate()
            f.write(audio.get_wav_data())

    with open('audioResultsInMP3.mp3', "r+") as f:
        f.truncate()

    AudioSegment.from_wav('audioResultsInWavForm.wav').export(
        "audioResultsInMP3.mp3", format="mp3")
    print("Done using microphone, and getting files \n")


def getAudioUsingFilePath():
    filename = fd.askopenfilename()
    str(filename)
    fileNameList = filename.split("/")
    filename = fileNameList[-1]

    return str(filename)


def getSongToGetVocals(num):
    print("RECOMMENDED: Type 1 for more accurate results, if you are downloading a song off internet, and converting to mp3 format. \n")

    if(num == 2):
        getAudioUsingMicro()
        getVocals('audioResultsInMP3.mp3')
    else:
        getVocals(getAudioUsingFilePath)


def getVocals(nameOfFile):
    #Use selenium here
    pass


def wholeProgram():
    getSongToGetVocals(inputOrRecord())
