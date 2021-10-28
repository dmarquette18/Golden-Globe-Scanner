from pickle import STRING
import re
from typing import final
from nltk.tag import perceptron
import pandas
import json
import nltk
import string
import spacy

from nltk import word_tokenize, pos_tag
def NomGather(awardName, awardKeys):
    basic_words = ["was", "an", "or", "a", "the", "more", 'to', "for", "golden", "globe", 's"', "in", "that", "you", "ever", "as", "be", "i", "at", "ben", "with", "and", "but", "&amp;", "is", "of", "those", "he", "she", "rt", "have", "all", "we", "so", "it", "on", "by", "les", "dress", "dressed", "this", "her"]
    punctuation = ["'", "*", ",", '"', ".", ":"]
    
    df2013 = pandas.read_json("c:/Users/dmarq/Downloads/GG Scanner/gg2013.json")
    nomCand = []
    finCand = []
    awardName = awardName.lower()
    for i in range(len(awardKeys)):
        awardKeys[i] = awardKeys[i].lower()
    for row in df2013.itertuples():
        
        dontCare = False
        tweet = row[1]
        tweet = tweet.lower()
        #tweet = tweet.translate(str.maketrans('', '', string.punctuation))
        #for i in range(len(punctuation)):
        #    tweet.replace(punctuation[i], "")
        cnt = 0
        if "rt" in tweet:
            continue
        if "nomination" in tweet or "nominated" in tweet or "nominee"  in tweet or "congrats" in tweet or "wins" in tweet or "should" in tweet:
            nomCand.append(tweet)
    
    for can in nomCand:
        count = 0
        can = can.split()
        for item in can:
            if item in awardKeys:
                count+=1
        if count >= len(awardKeys)-2:
            finCand.append(" ".join(can))
    

        
        
    nomCand = findNN(finCand)
    return nomCand

def findNN(nomCand):
    nnCand = []
    nlp = spacy.load("en_core_web_sm")
    
    for can in nomCand:
        tweet = nlp(can)
        for i, tagged_token in enumerate(tweet):
            tempText = ""
            if tagged_token.pos_ == 'PROPN':
                tempText = tagged_token.text
                k=i
                while k<(len(tweet)-1) and tweet[k+1].pos_ == 'PROPN':
                        tempText = tagged_token.text + " " + tweet[k+1].text
                        k=k+1
                #print("TWEET: " + " ".join(tweet) + " NAME: " +tagged_token[0])
                nnCand.append(tempText)
    return nnCand
        




    