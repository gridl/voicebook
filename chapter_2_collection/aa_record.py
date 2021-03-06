'''
aa_record.py

quick example illustrating active-asynchronous mode (AS mode).

Get a query from a user about whether they want the weather.

If they want the weather, fetch the weather over the internet with
BeautifulSoup.

It's a non-blocking example, meaning the weather is catched simultaneously
as the sample is being recorded.
'''
import sounddevice as sd
import soundfile as sf 
from bs4 import BeautifulSoup
import speech_recognition as sr_audio
import os, pyttsx3, pdfkit, pygame

def sync_record(filename, duration, fs, channels):
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    try:
        fetch_weather()
    except:
        pass
    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done recording')
    
def sync_playback(filename):
    # takes in a file and plays it back 
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def speak_text(text):
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def transcribe_audio_sphinx(filename):
    # transcribe the audio (note this is only done if a voice sample)
    r=sr_audio.Recognizer()
    with sr_audio.AudioFile(filename) as source:
        audio = r.record(source) 
    text=r.recognize_sphinx(audio)
    print('transcript: '+text)
    return text
    
def fetch_weather():
    link='https://www.yahoo.com/news/weather'
    pdfkit.from_url(link, 'out.pdf')

speak_text('would you like to get the weather?')
sync_playback('beep.mp3')
time.sleep(1.2)
sync_record('response.wav',5,16000,1)
transcript=transcribe_audio_sphinx('response.wav')
if transcript.lower().find('yes') >= 0 or transcript.lower().find('yeah')>=0:
    speak_text('ok, great here it is.')
    os.system('open out.pdf')
    
    
