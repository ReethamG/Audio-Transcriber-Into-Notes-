import os
import glob
import speech_recognition as sr
from pydub import AudioSegment
import variables
import time
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from aubio import source, onset
import scipy.io.wavfile as wavfile
import wave
import contextlib


def inputOrRecord():
    fileInputOrMicro = int(input(
        "Do you want to input a file OR do you want to use the microphone and record? (1/2)"))

    return fileInputOrMicro


def getAudioUsingMicro():  # Getting audio using the microphone
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


def getVocals():  # Turn on webdriver in variables for this, also might not use this, use lalai.ai for better vocal isolation
    variables.driver.get('https://vocalremover.org/')
    variables.driver.find_element_by_xpath(
        '//*[@id="app"]/main/div[1]/button').click()
    print("You have 30 seconds for you to upload the song you want! \n")
    time.sleep(30)
    variables.driver.find_element_by_xpath(
        '//*[@id="app"]/main/div[6]/div[1]/button')
    variables.driver.find_element_by_xpath(
        '//*[@id="app"]/main/div[6]/div[1]/div/div[1]')
    variables.driver.find_element_by_xpath(
        '//*[@id="app"]/main/div[6]/button').click()
    variables.driver.find_element_by_xpath(
        '//*[@id="app"]/main/div[6]/div[2]/button[2]').click()
    latestFileChangeAndRename()
    print("Downloaded isolated vocals of the song you want! \n")


def whatFileToGetVocals(num):  # User interface for, inputOrRecord option
    print("RECOMMENDED: Type 1 for more accurate results, if you are downloading a song off internet in mp3 format. \n")
    print("If you are using 2, make sure you upload the mp3 format of your microphone recording! NOT WAV FORM! \n")

    if(num == 2):
        getAudioUsingMicro()
        getVocals()
    else:
        getVocals()


def latestFileChangeAndRename():  # Gets the latest file downloaded, and converts and changes the directory, and renames it to the isolatedVocals.mp3
    with open('isolatedVocals.mp3', "r+") as f:
        f.truncate()

    savePath = '/Users/reethamgubba/Desktop/Programming Projects/Audio-Transcriber-Into-Notes-'
    listOfFiles = glob.glob('/Users/reethamgubba/Downloads/*')
    latestFile = max(listOfFiles, key=os.path.getctime)
    os.path.join(savePath, latestFile)
    os.rename(latestFile, 'isolatedVocals.mp3')


def getSecondsOfFile(fileName):

    with contextlib.closing(wave.open(fileName, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def getOnsetTimes(file_path):  # Gets all the start of a new note, and adds it to a list
    window_size = 1024
    hop_size = window_size // 4

    sample_rate = 0
    src_func = source(file_path, sample_rate, hop_size)
    sample_rate = src_func.samplerate
    onset_func = onset('default', window_size, hop_size)

    duration = float(src_func.duration) / src_func.samplerate

    onset_times = []
    while True:
        samples, num_frames_read = src_func()
        if onset_func(samples):
            onset_time = onset_func.get_last_s()
            if onset_time < duration:
                onset_times.append(onset_time)
            else:
                break
        if num_frames_read < hop_size:
            break

    roundedOnsetTimes = []

    for time in onset_times:
        roundedOnsetTimes.append(round(time, 4))

    return roundedOnsetTimes


def getFreq(filename):
    Fs, aud = wavfile.read(filename)
    aud = aud[:, 0]
# trim the first 125 seconds
    first = aud[:int(Fs*(getSecondsOfFile(filename)))]
    powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(
        first, Fs=Fs)
    plt.show()

    print(powerSpectrum)
    print(frequenciesFound)
    print(time)
    print(imageAxis)


def getPitchesOfSong():

    listOfFreq = []

    for time in getOnsetTimes('isolatedVocals.wav'):
        frequency = freq(
            'isolatedVocals.wav', time)
        listOfFreq.append(frequency)

    print(listOfFreq)
    return listOfFreq
