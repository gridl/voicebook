'''
fingerprint audio models in a streaming folder. 
'''

import librosa, pickle, getpass, time 
from pydub import AudioSegment
import speech_recognition as sr  
import os, nltk, random, json 
from sklearn.preprocessing import PolynomialFeatures
from textblob import TextBlob
import numpy as np 

cur_dir=os.getcwd()+'/load_dir'
model_dir=os.getcwd()+'/models'
load_dir=os.getcwd()+'/load_dir'
    
def featurize2(wavfile):
    #initialize features 
    hop_length = 512
    n_fft=2048
    #load file 
    y, sr = librosa.load(wavfile)
    #extract mfcc coefficients 
    mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
    mfcc_delta = librosa.feature.delta(mfcc) 
    #extract mean, standard deviation, min, and max value in mfcc frame, do this across all mfccs
    mfcc_features=np.array([np.mean(mfcc[0]),np.std(mfcc[0]),np.amin(mfcc[0]),np.amax(mfcc[0]),
                            np.mean(mfcc[1]),np.std(mfcc[1]),np.amin(mfcc[1]),np.amax(mfcc[1]),
                            np.mean(mfcc[2]),np.std(mfcc[2]),np.amin(mfcc[2]),np.amax(mfcc[2]),
                            np.mean(mfcc[3]),np.std(mfcc[3]),np.amin(mfcc[3]),np.amax(mfcc[3]),
                            np.mean(mfcc[4]),np.std(mfcc[4]),np.amin(mfcc[4]),np.amax(mfcc[4]),
                            np.mean(mfcc[5]),np.std(mfcc[5]),np.amin(mfcc[5]),np.amax(mfcc[5]),
                            np.mean(mfcc[6]),np.std(mfcc[6]),np.amin(mfcc[6]),np.amax(mfcc[6]),
                            np.mean(mfcc[7]),np.std(mfcc[7]),np.amin(mfcc[7]),np.amax(mfcc[7]),
                            np.mean(mfcc[8]),np.std(mfcc[8]),np.amin(mfcc[8]),np.amax(mfcc[8]),
                            np.mean(mfcc[9]),np.std(mfcc[9]),np.amin(mfcc[9]),np.amax(mfcc[9]),
                            np.mean(mfcc[10]),np.std(mfcc[10]),np.amin(mfcc[10]),np.amax(mfcc[10]),
                            np.mean(mfcc[11]),np.std(mfcc[11]),np.amin(mfcc[11]),np.amax(mfcc[11]),
                            np.mean(mfcc[12]),np.std(mfcc[12]),np.amin(mfcc[12]),np.amax(mfcc[12]),
                            np.mean(mfcc_delta[0]),np.std(mfcc_delta[0]),np.amin(mfcc_delta[0]),np.amax(mfcc_delta[0]),
                            np.mean(mfcc_delta[1]),np.std(mfcc_delta[1]),np.amin(mfcc_delta[1]),np.amax(mfcc_delta[1]),
                            np.mean(mfcc_delta[2]),np.std(mfcc_delta[2]),np.amin(mfcc_delta[2]),np.amax(mfcc_delta[2]),
                            np.mean(mfcc_delta[3]),np.std(mfcc_delta[3]),np.amin(mfcc_delta[3]),np.amax(mfcc_delta[3]),
                            np.mean(mfcc_delta[4]),np.std(mfcc_delta[4]),np.amin(mfcc_delta[4]),np.amax(mfcc_delta[4]),
                            np.mean(mfcc_delta[5]),np.std(mfcc_delta[5]),np.amin(mfcc_delta[5]),np.amax(mfcc_delta[5]),
                            np.mean(mfcc_delta[6]),np.std(mfcc_delta[6]),np.amin(mfcc_delta[6]),np.amax(mfcc_delta[6]),
                            np.mean(mfcc_delta[7]),np.std(mfcc_delta[7]),np.amin(mfcc_delta[7]),np.amax(mfcc_delta[7]),
                            np.mean(mfcc_delta[8]),np.std(mfcc_delta[8]),np.amin(mfcc_delta[8]),np.amax(mfcc_delta[8]),
                            np.mean(mfcc_delta[9]),np.std(mfcc_delta[9]),np.amin(mfcc_delta[9]),np.amax(mfcc_delta[9]),
                            np.mean(mfcc_delta[10]),np.std(mfcc_delta[10]),np.amin(mfcc_delta[10]),np.amax(mfcc_delta[10]),
                            np.mean(mfcc_delta[11]),np.std(mfcc_delta[11]),np.amin(mfcc_delta[11]),np.amax(mfcc_delta[11]),
                            np.mean(mfcc_delta[12]),np.std(mfcc_delta[12]),np.amin(mfcc_delta[12]),np.amax(mfcc_delta[12])])
    
    return mfcc_features

def exportfile(newAudio,time1,time2,filename,i):
    #Exports to a wav file in the current path.
    newAudio2 = newAudio[time1:time2]
    g=os.listdir()
    if filename[0:-4]+'_'+str(i)+'.wav' in g:
        filename2=str(i)+'_segment'+'.wav'
        print('making %s'%(filename2))
        newAudio2.export(filename2,format="wav")
    else:
        filename2=str(i)+'.wav'
        print('making %s'%(filename2))
        newAudio2.export(filename2, format="wav")

    return filename2 

def audio_time_features(filename):
    #recommend >0.50 seconds for timesplit 
    timesplit=0.50
    hop_length = 512
    n_fft=2048
    
    y, sr = librosa.load(filename)
    duration=float(librosa.core.get_duration(y))
    
    #Now splice an audio signal into individual elements of 100 ms and extract
    #all these features per 100 ms
    segnum=round(duration/timesplit)
    deltat=duration/segnum
    timesegment=list()
    time=0

    for i in range(segnum):
        #milliseconds
        timesegment.append(time)
        time=time+deltat*1000

    newAudio = AudioSegment.from_wav(filename)
    filelist=list()
    
    for i in range(len(timesegment)-1):
        filename=exportfile(newAudio,timesegment[i],timesegment[i+1],filename,i)
        filelist.append(filename)

        featureslist=np.array([0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0,
                               0,0,0,0])
    
    #save 100 ms segments in current folder (delete them after)
    for j in range(len(filelist)):
        try:
            features=featurize2(filelist[i])
            featureslist=featureslist+features 
            os.remove(filelist[j])
        except:
            print('error splicing')
            os.remove(filelist[j])

    #now scale the featureslist array by the length to get mean in each category
    featureslist=featureslist/segnum
    
    return featureslist

def featurize(wavfile):
    features=np.append(featurize2(wavfile),audio_time_features(wavfile))
    return features 

def convert(file):
    
    if file[-4:] != '.wav':
        filename=file[0:-4]+'.wav'
        os.system('ffmpeg -i %s -an %s'%(file,filename))
        os.remove(file)
    elif file[-4:] == '.wav':
        filename=file
    else:
        filename=file 
        os.remove(file)

    return filename

model_list=list()
os.chdir(model_dir)
listdir=os.listdir()

for i in range(len(listdir)):
    if listdir[i][-18:]=='_regression.pickle':
        model_list.append(listdir[i])

count=0
errorcount=0

try:
    os.chdir(load_dir)
except:
    os.mkdir(load_dir)
    os.chdir(load_dir)
    
listdir=os.listdir()
print(os.getcwd())
for i in range(len(listdir)):
    try:
        if listdir[i][-5:] not in ['Store','.json']:
            if listdir[i][-4:] != '.wav':
                if listdir[i][-5:] != '.json':
                    filename=convert(listdir[i])
            else:
                filename=listdir[i]

            print(filename)

            if filename[0:-4]+'_regression.json' not in listdir:
                
                features=featurize(filename)
                features=features.reshape(1,-1)

                os.chdir(model_dir)

                class_list=list()
                model_stats=list()
                modeltypes=list()
                
                for j in range(len(model_list)):
                    modelname=model_list[j]
                    i1=modelname.find('_')
                    name1=modelname[0:i1]
                    i2=modelname[i1:]
                    i3=i2.find('_')
                    name2=i2[0:i3]

                    g=json.load(open(modelname[0:-7]+'.json'))
                    modeltype=g['model type']
                    classes=g['classes']
                    model_stats.append(g['stats'])
                    modeltypes.append(modeltype)

                    loadmodel=open(modelname, 'rb')
                    model = pickle.load(loadmodel)
                    loadmodel.close()
                    
                    if modeltype not in ['stochastic gradient descent (SGD)', 'polynomial (perceptron)']:
                        output=str(model.predict(features)[0])
                        print(output)
                        classname=output
                    # slightly different for polynomial perceptrons and SGD
                    elif modeltype=='stochastic gradient descent (SGD)':
                        scaler = StandardScaler()
                        scaler.fit(features)
                        features2 = scaler.transform(features)
                        output=str(model.predict(features2))
                        print(output)
                        classname=output
                    elif modeltype=='polynomial (perceptron)':
                        output=str(model.predict(features2)[0])
                        print(output)
                        classname=output

                    if float(classname) < 0.5: 
                        classname=classes[0]
                    else:
                        classname=classes[1]
                    print(classname)
                    class_list.append(classname)

                os.chdir(load_dir)

                jsonfilename=filename[0:-4]+'_regression.json'
                jsonfile=open(jsonfilename,'w')
                data={
                    'filename':filename,
                    'filetype':'audio file',
                    'class':class_list,
                    'model':model_list,
                    'model types':modeltypes,
                    'stats':model_stats,
                    'features':features.tolist(),
                    'count':count,
                    'errorcount':errorcount,
                    }
                json.dump(data,jsonfile)
                jsonfile.close()
                
            count=count+1
    except:
        errorcount=errorcount+1
        count=count+1 
