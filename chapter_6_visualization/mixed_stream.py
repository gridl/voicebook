'''
Audio_stream.py

Give some simple visual feedback when recording an audio stream.
'''
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr_audio
import random, time, librosa, os 
import numpy as np

def transcribe_pocket(filename):
    # transcribe the audio (note this is only done if a voice sample)
    r=sr_audio.Recognizer()
    with sr_audio.AudioFile(filename) as source:
        audio = r.record(source) 
    text=r.recognize_sphinx(audio)
    
    return text

def visualize_data(sample, minimum, maximum):
    difference=maximum-minimum
    delta=difference/10
    bar='==.==.'
    if sample <= minimum:
        # 1 bar
        output=bar
    elif minimum+delta >= sample > minimum:
        # 1 bar
        output=bar
    elif minimum+delta*2 >= sample > minimum+delta:
        # 2 bars
        output=bar*2
    elif minimum+delta*3 >= sample >= minimum+delta*2:
        # 3 bars
        output=bar*3
    elif minimum+delta*4 >= sample > minimum+delta*3:
        # 4 bars
        output=bar*4
    elif minimum+delta*5 >= sample > minimum+delta*4:
        # 5 bars
        output=bar*5
    elif minimum+delta*6 >= sample > minimum+delta*5:
        # 6 bars
        output=bar*6
    elif minimum+delta*7 >= sample > minimum+delta*6:
        # 7 bars
        output=bar*7
    elif minimum+delta*8 >= sample > minimum+delta*7:
        # 8 bards
        output=bar*8
    elif minimum+delta*9 >= sample > minimum+delta*8:
        # 9 bars
        output=bar*9
    elif maximum > sample >= minimum+delta*9:
        # 10 bars
        output=bar*10
    elif sample >= maximum:
        # 10 bars
        output=bar*10
    else:
        print(sample)
        output='error'

    # plot bars based on a min and max 
    return output[0:-1]

def record_data(filename, duration, fs, channels):
    # synchronous recording 
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, fs)
    y, sr = librosa.load(filename)
    rmse=np.mean(librosa.feature.rmse(y)[0])
    
    return rmse*1000

# take a streaming sample and then put that data as it is being recorded
minimum=0
maximum=70
samples=list()
transcripts=list()

for i in range(30):    
    # record 1 second of data 
    sample=record_data('sample.wav',1.0, 44100, 1)
    if sample > maximum:
        maximum=sample 
        print('new max is %s'%(maximum))
    transcript=transcribe_pocket('sample.wav')
    os.remove('sample.wav')
    transcripts.append(transcript)
    samples.append(sample)
    print(visualize_data(sample,minimum,maximum) + ' ' + transcript)

samples=np.array(samples)
minval=np.amin(samples)
maxval=np.amax(samples)
print('minimum val: %s'%(str(minval)))
print('max val: %s'%(str(maxval)))
print('transcripts: ')
print(transcripts)
