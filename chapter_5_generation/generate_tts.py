'''
generate_tts.py
@Author: Jim Schwoebel

This script takes in a text sample (.json or .txt) and outputs a .wav text-to-speech file from this data.

This text-to-speech defaults to an ouptut female voice, but could be customized to various workers fairly easily in the 
initialization variable section. 

Happy TTXing! 

(C) NeuroLex Laboratories, 2018

'''
import os, shutil, librosa, time, json, random
from subprocess import call 

#assumes ffmpeg and mac computer have default libraries installed via setup.py

##INITIALIZE FUNCTIONS FOR CLEANING
####################################################################################
def createfile(transcript,filename):
    print('making tts file...')
    
    filename=filename+'.aiff'

    #configure output voice here as either - Randomly select here 
    #'Alex',‘Bruce’, ‘Fred, ‘Kathy’, ‘Vicki’ and ‘Victoria’
##    voice=['Alex','Bruce','Fred','Kathy','Vicki','Victoria']
##    randomnum=random.randint(0,len(voice)-1)
##    voicetype=voice[randomnum]
    voicetype='Alex'
    
    #how to create a file
    call(["say","-o",filename,transcript])

    return filename

def convertfile(filename):
    print('converting %s to %s'%(filename,filename[0:-5]+'.wav'))
    filenameold=filename 
    filenamenew=filename[0:-5]+'.wav'
    #convert file
    call(['ffmpeg','-i',filename,filenamenew])

    return filenamenew

##INITIALIZE FUNCTIONS FOR CLEANING
####################################################################################
#host directory in app is likely /usr/app/...
hostdir=os.getcwd()

#now create some folders if they have not already been created 
incoming_dir=hostdir+'/tts-incoming/'
processed_dir=hostdir+'/tts-processed/'

#incoming folder = samples on server that need to be cleaned 
#processed_folder = samples on server that have been cleaned 

try:
    os.chdir(incoming_dir)
except:
    os.mkdir(incoming_dir)

try:
    os.chdir(processed_dir)
except:
    os.mkdir(processed_dir)

#change to incoming directory to look for samples
os.chdir(incoming_dir)

#initialize sleep time for worker (default is 1 second)
sleeptime=1

# now initialize process list with files already in the directory
processlist=[]
ttstype='core mac OS'

#error counts will help us debug later
errorcount=0
processcount=0

#initialize t for infinite loop
t=1

#infinite loop for worker now begins with while loop...

while t>0:
    #go to incoming directory
    os.chdir(incoming_dir)
    listdir=os.listdir()
    print(listdir)

    try:
    
        #look for any files that have not been previously in the directory
        for i in range(len(listdir)):
            start=time.time()
            file=listdir[i]
            if file[-4:]=='.txt' or file[-5:]=='.json' and listdir[i] not in processlist:
                print('%s found, processing...'%(file))
                if file[-4:]=='.txt':
                    transcript=open(file).read()
                    print('transcript found - %s'%(transcript))
                    filename=file[0:-4]
                elif file[-5:]=='.json':
                    transcript=json.load(open(file))['transcript']
                    print('transcript found - %s'%(transcript))
                    filename=file[0:-5]

                #now run functions to convert file
                print(filename)
                filename=createfile(transcript,filename)
                print(filename)
                filename=convertfile(filename)
                print(filename)
                y,samplerate=librosa.core.load(filename)
                duration=librosa.core.get_duration(y,samplerate)

                end=time.time()
                processtime=end-start

                #write data to .json 
                data={
                  'transcript':transcript,
                  'speak file':filename,
                  'processed file':file,
                  'tts type':ttstype,
                  'process time':str(processtime),
                  'file duration':str(duration),
                  }
                
                jsonfilename=filename[0:-4]+'_processed.json'
                jsonfile=open(jsonfilename,'w')
                json.dump(data,jsonfile)
                jsonfile.close()

                #now move all processed file to processed file directory and continue loop
                shutil.move(incoming_dir+jsonfilename,processed_dir+jsonfilename)
                shutil.move(incoming_dir+filename,processed_dir+filename)
                shutil.move(incoming_dir+file,processed_dir+file)

                processlist.append(file)
                
            else:
                #remove the file if it cannot be processed...
                os.remove(file)

        print('sleeping...')
        time.sleep(sleeptime)
              
    except:
        print('error')
        errorcount=errorcount+1
        print('sleeping...')
        time.sleep(sleeptime)
        


