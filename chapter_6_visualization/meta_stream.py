'''
Author: Jim Schwoebel 
Github: 

meta_stream.py

Stream in an audio file from the microphone and output
meta features - like gender and age detection.

'''
#########################################################
##.                  IMPORT STATEMENTS                 ##
#########################################################

import sounddevice as sd
import soundfile as sf
import random, time, librosa, os 
import numpy as np
import matplotlib.pyplot as plt
from drawnow import drawnow
import shutil, os, json

#########################################################
##.                  HELPER FUNCTIONS.                 ##
#########################################################

def make_fig():
    plt.scatter(x, y) 

def record_data(filename, duration, fs, channels):
    # synchronous recording 
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done')
    
    return filename 

def meta_featurize(filename, datadir, metadir):

	# from a wav file in the current directory featurize it with meta features
	# derived from machine learning models 
	# can be used in a streaming or non-streaming way 
	# note: models were trained on 20 second periods so this is probably the best windows for files 

	curdir=os.getcwd()
	os.chdir(metadir)
	if 'load_dir' not in os.listdir():
		# make load directory folder 
		os.system('python3 meta_features.py')
            
	shutil.move(curdir+'/'+filename, metadir+'/load_dir/'+filename)
	# now featurize the file 
	os.system('python3 meta_features.py')
	# now load the .json result
	os.chdir('load_dir')
	g=json.load(open(filename[0:-4]+'.json'))
	# get classes
	classes=g['class']
	# remove file 
	os.remove(filename[0:-4]+'.json')
	os.remove(filename)
	# go back to current directory 
	os.chdir(curdir)

	return classes

#########################################################
##.                  MAIN SCRIPT                       ##
#########################################################

# plot out meta features on the screen in streaming way
curdir=os.getcwd()
datadir=os.getcwd()+'/data/'
metadir=curdir.replace('/chapter_6_visualization','/chapter_3_featurization')

# wavfile
#file=input('what file in the ./data directory would you like to meta featurize? \n')
x=list()
y=list()
for i in range(30):    
    # record 20ms of data 
    filename=record_data('sample.wav', 1, 44100, 1)
    classes=meta_featurize(filename, datadir, metadir)
    sample=classes[27]

    # make a simple method for finding whether or not class is control
    if sample.find('male') > 0:
    	sample=0
    else:
        sample=1

    x.append(i)
    y.append(sample)
    drawnow(make_fig)

plt.xlabel('time (seconds)')
plt.ylabel('gender')
plt.savefig('meta_stream.png')
os.system('open meta_stream.png')
