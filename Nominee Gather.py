from nltk.grammar import is_nonterminal
import pandas
import itertools
from CanGather import canGather
from VoteSystem import voteCounter, sortVote
from trimmer import FiveWord, endRemove, fatTrimmer, nipNames, purgeSame, removePunct, unifySimilar, unifySpaces, purgeSimilar, trimToBest, purgeSame
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from wordVote import commonality
from NomineeComber import NomGather
from operator import itemgetter
from collections import Counter
import json
nominees = dict()
mAwards = ['Best Motion Picture - Drama','Best Motion Picture - Musical or Comedy','Best Director','Best Actor - Motion Picture Drama','Best Actor - Motion Picture Musical or Comedy',
'Best Actress - Motion Picture Drama','Best Actress - Motion Picture Musical or Comedy','Best Supporting Actor - Motion Picture','Best Supporting Actress - Motion Picture',
'Best Screenplay','Best Original Score','Best Foreign Language Film','Best Animated Feature Film','Cecil B. DeMille Lifetime Achievement Award', 'Best Original Song']

# Television Awards
tAwards = ['Best Drama Series','Best Comedy Series','Best Actor in a Television Drama Series','Best Actor in a Television Comedy Series','Best Actress in a Television Drama Series',
'Best Actress in a Television Comedy Series','Best Limited Series or Motion Picture made for Television','Best Actor in a Limited Series made for Television',
'Best Actress in a Limited Series made for Television','Best Supporting Actor in a Limited Series made for Television',
'Best Supporting Actress in a Limited Series made for Television']

catToAwards = {"Cecil B. DeMille Award" : "Cecil B. DeMille Award",
"Best Motion Picture - Drama" : "Best Motion Picture - Drama",
"Best Actress - Motion Picture Drama": "Best Performance by an Actress in a Motion Picture - Drama",
"Best Actor - Motion Picture Drama" : "Best Performance by an Actor in a Motion Picture - Drama",
"Best Motion Picture - Musical or Comedy": "Best Motion Picture - Comedy Or Musical",
"Best Actress - Motion Picture Musical or Comedy" :"Best Performance by an Actress in a Motion Picture - Comedy Or Musical",
"Best Actor - Motion Picture Musical or Comedy" :"Best Performance by an Actor in a Motion Picture - Comedy Or Musical",
"Best Animated Feature Film": "Best Animated Feature Film",
"Best Foreign Language Film" : "Best Foreign Language Film",
"Best Supporting Actress - Motion Picture": "Best Performance by an Actress In A Supporting Role in a Motion Picture",
"Best Supporting Actor - Motion Picture" : "Best Performance by an Actor In A Supporting Role in a Motion Picture",
"Best Director": "Best Director - Motion Picture",
"Best Screenplay": "Best Screenplay - Motion Picture",
"Best Original Score": "Best Original Score - Motion Picture",
"Best Original Song" : "Best Original Song - Motion Picture",
"Best Drama Series" :"Best Television Series - Drama",
"Best Actress in a Television Drama Series": "Best Performance by an Actress In A Television Series - Drama",
"Best Actor in a Television Drama Series" : "Best Performance by an Actor In A Television Series - Drama",
"Best Comedy Series" : "Best Television Series - Comedy Or Musical",
"Best Actress in a Television Comedy Series" :"Best Performance by an Actress In A Television Series - Comedy Or Musical",
"Best Mini-Series or Motion Picture made for Television" : "Best Mini-Series Or Motion Picture Made for Television",
"Best Actor in a Television Comedy Series" : "Best Performance by an Actor In A Television Series - Comedy Or Musical",
"Best Actress in a Mini-Series or Motion Picture made for Television" : "Best Performance by an Actress In A Mini-series or Motion Picture Made for Television",
"Best Actor in a Mini-Series or Motion Picture made for Television" : "Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television",
"Best Supporting Actress in a Series, Mini-Series or Motion Picture made for Television": "Best Performance by an Actress in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television",
"Best Supporting Actor in a Series, Mini-Series or Motion Picture made for Television" : "Best Performance by an Actor in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television"}

basicAwards = list(catToAwards.keys())
awardsAndNomCands = dict()


def get_tweets(year):
    
    # get tweets
    with open('gg%s.json' % year) as json_data:
        data = json.load(json_data)
    json_data.close()
    
    #stopWords = set(stopwords.words('english'))
    stopWords_tweets = ['http','rt','goldenglobes','golden','globes','rt','golden','globes','globe' \
                        'goldenglobes','goldenglobe']    
    keywords = ['best','winner','wins','award','awards','nominees','nominated','congratulates',\
                'congratulations','congrats','announce','announcing','present']
    
    # tokenize tweets and select matching tweets
    start = 0
    end = len(data)
    word_list = []  
    for q in range(start, end):
        words = word_tokenize(data[q]['text'])
        
        # convert to lower case
        text = [words[i].lower() for i in range(len(words))]
        
        words_meaningful = [token for token in text if token not in stopWords_tweets and token.isalpha()]
        if len(list(set(words_meaningful) & set(keywords)))>0:
            word_list.append(words_meaningful)
    
    return word_list



def get_awardsKeywords(awards):
    awards_keys = awards
    awards_keywords = []
    keyDict = {}
    for i in range(len(awards_keys)):
        # tokenize awards words
        awards_token = word_tokenize(awards_keys[i])
        # find awards keywords
        awards_temp = []
        stopWords_awards = ['by', 'an', 'in', 'a', 'for', 'or', '-', ',']
        j = 0
        while len(awards_temp) < 5 and j < len(awards_token):
            if awards_token[j] not in stopWords_awards:
                awards_temp.append(awards_token[j])
                j = j + 1
            else:
                j = j + 1
        awards_keywords.append(awards_temp)
        keyDict[awards_keys[i]] = awards_temp


    

    return keyDict

keyDict = get_awardsKeywords(basicAwards)
nomCand = {}
nomCand[basicAwards[2]] = NomGather(basicAwards[2], keyDict[basicAwards[2]])
testVote = voteCounter(nomCand[basicAwards[2]])
testVote = sortVote(testVote)
#testVote = nipNames(testVote)
print(testVote)



def get_nominees_raw(year, awards):
    
    word_list = get_tweets(year)
    awards_keys = list(awards)   
    awards_keywords = get_awardsKeywords(awards)
    tweets_stopwords = ['best','better','winner','wins','won','winning','presents','at','for',
                        'in','to','award','awards','nominees','nominated','congratulates','congratulations',
                        'congrats','Congrats','was','a','an','i','announced','announce', 'announcing','present',
                       'by','with','the', 'todayshow','of','latest','movie','film','is','awarded','and',
                       'actor','globe','or','picture','animated','animation','motion','from']
    
    # get tweets with possible nominees
    nominees_raw = {}
    for i in range(len(awards_keywords)):
        nom_values = []
        # get the matching tweets
        for j in range(len(word_list)):
            k = set(awards_keywords[i])
            b = set(word_list[j])
            if set(awards_keywords[i]) <= set(word_list[j]):
                print("IN HERE")
                wordList_copy = word_list[j].copy()
                
                # exclude awards_keywords
                for ak in awards_keywords[i]:
                    wordList_copy.remove(ak)
                # exculde tweets_stopwords
                wordList = [item for item in wordList_copy if item not in tweets_stopwords]
                nom_values.append(wordList)
            else:
                continue

        nominees_raw[awards_keys[i]] = nom_values
      
    return nominees_raw
   

#print(get_nominees_raw(2013, basicAwards))
