'''
text_tsne_many.py

Plot many tsne plots from a folder full of .txt files 


'''
import os 
import numpy as np
import re, nltk, gensim
from sklearn.manifold import TSNE
import speech_recognition as sr_audio
import matplotlib.pyplot as plt
import spacy 

# helper funcitons 
def transcribe_pocket(filename):
    # transcribe the audio (note this is only done if a voice sample)
    try:
        r=sr_audio.Recognizer()
        with sr_audio.AudioFile(filename) as source:
            audio = r.record(source) 
        text=r.recognize_sphinx(audio)
    except:
        text=''
    print(text)
    # now print out text to a .txt file 
    txtfile=open(filename[0:-4]+'.txt','w')
    txtfile.write(text)
    txtfile.close()

    return text

def tsne_vals(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)
    
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
        
    return x, y 


# initialization
curdir=os.getcwd()
folder=input('what folder in ./data directory would you like to make tSNE text plots for?\n')
os.chdir('./data/'+folder)
files = sorted(os.listdir())
wavfiles=list()
# get text files 
for i in range(len(files)):
    if files[i][-4:]=='.wav':
        wavfiles.append(files[i])

# initialize plotting parameters 
columns=5
nlp=spacy.load('en')
STOP_WORDS = nltk.corpus.stopwords.words()
fig, ax = plt.subplots(int(np.ceil(len(files)/columns)),columns,figsize=(15,30))

# now loop through each txtfile and put in proper subplot 
for idx, file in enumerate(wavfiles):
    # set plot parameteres 
    r,c = idx//columns, idx%columns
    ax[r,c].set_title(file)

    # get  transcript if it does not exist 
    if file[0:-4]+'.txt' not in os.listdir():
        transcript=transcribe_pocket(file)
    else:
        transcript=open(file[0:-4]+'.txt').read()

    # manipulate transcript to get sentences and words 
    # (spacy is more accurate at sentence parsing!! )
    sents=list()
    doc=nlp(transcript)
    for span in doc.sents:
        sents.append(str(span))
    vocabs=list()
    for i in range(len(sents)):
        vocabs.append(str(sents[i]).split())

    # make word2vec model 
    model = gensim.models.Word2Vec(vocabs, min_count=1)

    # now plot word2vec model 
    x,y = tsne_vals(model)

    for i in range(len(x)):
        ax[r,c].scatter(x[i],y[i])

plt.subplots_adjust(wspace=0.05, hspace=0.1)
plt.savefig('plotmany_tsne.png')
os.system('open plotmany_tsne.png')
