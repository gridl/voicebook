'''
generate_remix.py

Given a list of .wav files (20 seconds), remix them to 4 seconds of each
(20/5=4) and normalize the remixed file.

Useful for putting together audio playbacks to summarize audio recordings.
'''

from pydub import AudioSegment
import os, getpass, random

folder=input('what folder (in ./data directory) would you like to remix? \n')
os.chdir(os.getcwd()+'/data/'+folder)

listdir=os.listdir()
random.shuffle(listdir)
t=0
for i in range(len(listdir)):
    if listdir[i][-4:]=='.wav':
        if t==0:
            soundt=AudioSegment.from_wav(os.getcwd()+'/'+listdir[i])
            sound=soundt[0:(len(soundt))]
            t=t+1
        else:
            soundt=AudioSegment.from_wav(os.getcwd()+'/'+listdir[i])
            sound=sound+soundt[0:(len(soundt))]
        
sound.export('remix.wav', format="wav")
os.system('ffmpeg-normalize remix.wav -o remix-normalized.wav')
