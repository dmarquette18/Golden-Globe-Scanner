from pickle import STRING
import re
from typing import final
from nltk.tag import perceptron
import pandas
import json
import nltk
import string
import spacy
import re
import pickle
from nltk import word_tokenize, pos_tag
def quickNomGather(personOrMovie, year):
    print("started quick search")
    file_name = 'gg{}.json'.format(year)
    pand = pandas.read_json(file_name)
    criteria = ["nominated for", "nominee for", "congrats to", "should have won", "wins", "nominee"]
    tempTotal = []
    for item in criteria:
        brandy = pand[pand['text'].str.contains(item)]
        tempList = brandy['text'].tolist()
        tempTotal += tempList
    
    finCand = tempTotal
    print("starting findNN")
    nomCand = quickFindNN(finCand, "person")
    print("finished findNN")
    print("Finished Quick Search")
    return nomCand
    
    print("finished quick search")
    
def NomGather(personOrMovie, scoreDict, year):
    print("Started loading tweets")
    basic_words = ["was", "an", "or", "a", "the", "more", 'to', "for", "golden", "globe", 's"', "in", "that", "you", "ever", "as", "be", "i", "at", "ben", "with", "and", "but", "&amp;", "is", "of", "those", "he", "she", "rt", "have", "all", "we", "so", "it", "on", "by", "les", "dress", "dressed", "this", "her"]
    punctuation = ["'", "*", ",", '"', ".", ":"]
    file_name = 'gg{}.json'.format(year)
    pand = pandas.read_json(file_name)

    
    nomCand = []
    finCand = []
    
    for row in pand.itertuples():
        
        dontCare = False
        tweet = row[1]
        tweet = tweet.lower()
        #tweet = tweet.translate(str.maketrans('', '', string.punctuation))
        #for i in range(len(punctuation)):
        #    tweet.replace(punctuation[i], "")
        cnt = 0
        if "rt" in tweet:
            continue
        #if "nomination" in tweet or "nominated" in tweet or "nominee"  in tweet or "congrats" in tweet or "wins" in tweet:
        #    nomCand.append(tweet)
        if "nominated for" in tweet or "nominee for" in tweet or "congrats to" in tweet or "should have won" in tweet:
            nomCand.append(tweet)
        elif "wins" in tweet or "nominee" in tweet:
            nomCand.append(tweet)
        
        
    #if len(awardName) < 4:
    #    for can in nomCand:
    #        count = 0
    #        count2 = 0
    #        if awardName in can:
    #            finCand.append(can)
    #else:
    #    for can in nomCand:
    #        count = 0
    #        count2 = 0
    #        if awardName in can:
    #            for item in can:
    #                if item in awardKeys:
    #                    count += scoreDict[item]
    #                    count2 += 1
    #        if count >= 12 and count2 > 4:
    #            finCand.append(" ".join(can))
    
    

        
    finCand = nomCand    
    #nomCand = findNN(finCand, personOrMovie)
    nomCand = quickFindNN(finCand, "person")
    #with open('prereadtweets.txt', 'wb') as f:
    #    pickle.dump(nomCand, f)
    print("Finished Loading Tweets")
    return nomCand

def findNN(nomCand, person):
    nnCand = []
    nlp = spacy.load("en_core_web_sm")
    if person == "person":
        posType = "PROPN"
    else:
        posType = "NOUN"

    for can in nomCand:
        tweet = nlp(can)
        for i, tagged_token in enumerate(tweet):
            tempText = ""
            if tagged_token.pos_ == posType:
                tempText = tagged_token.text
                k=i+1
                while k<(len(tweet)-1) and "#" not in tweet.text and "http" not in tweet.text:
                        tempText = tempText + " " + tweet[k].text
                        k=k+1
                break
                #print("TWEET: " + " ".join(tweet) + " NAME: " +tagged_token[0])
        nnCand.append(tempText)
    return nnCand

def quickFindNN(nomCand, person):
    nnCand = []
    nlp = spacy.load("en_core_web_sm")
    if person == "person":
        posType = "PROPN"
    else:
        posType = "NOUN"
    
    for doc in nlp.pipe(nomCand):
    # Do something with the doc here
        for i, ent in enumerate(doc):
            if ent.pos_ == posType:
                tempText = ent.text
                k=i+1
                while k<(len(doc)-1) and "#" not in doc[k].text and "http" not in doc[k].text:
                        tempText = tempText + " " + doc[k].text
                        k=k+1
                break
        nnCand.append(tempText)
    
    return nnCand
    


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def add_flatten_lists(the_lists):
    result = []
    for _list in the_lists:
        result += _list
    return result
        




    