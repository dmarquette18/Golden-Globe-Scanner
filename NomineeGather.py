from json import decoder
import pickle
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
from NomineeComber import NomGather, quickNomGather
from operator import itemgetter, pos
from collections import Counter
import spacy
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
"Best Motion Picture Drama" : "Best Motion Picture - Drama",
"Best Actress Motion Picture Drama": "Best Performance by an Actress in a Motion Picture - Drama",
"Best Actor Motion Picture Drama" : "Best Performance by an Actor in a Motion Picture - Drama",
"Best Motion Picture Musical or Comedy": "Best Motion Picture - Comedy Or Musical",
"Best Actress Motion Picture Musical or Comedy" :"Best Performance by an Actress in a Motion Picture - Comedy Or Musical",
"Best Actor Motion Picture Musical or Comedy" :"Best Performance by an Actor in a Motion Picture - Comedy Or Musical",
"Best Animated Feature Film": "Best Animated Feature Film",
"Best Foreign Language Film" : "Best Foreign Language Film",
"Best Supporting Actress Motion Picture": "Best Performance by an Actress In A Supporting Role in a Motion Picture",
"Best Supporting Actor Motion Picture" : "Best Performance by an Actor In A Supporting Role in a Motion Picture",
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
    stopWords_tweets = ['http','rt','goldenglobes','golden','globes','rt','golden','globes','globe' 
                        'goldenglobes','goldenglobe']    
    keywords = ['best','winner','wins','award','awards','nominees','nominated','congratulates',
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


def translate(finalDict):
    tempDict = {}
    for item in finalDict:
        real = catToAwards[item]
        real = real.lower()
        tempDict[real] = finalDict[item]
    return tempDict

def add_flatten_lists(the_lists):
    result = []
    for _list in the_lists:
        result += _list
    return result

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

def get_unique_keys(keyDict):
    uniquekeys =  keyDict
    tempKeys = {}
    for key in keyDict:
        for item in keyDict[key]:
            if item in tempKeys:
                tempKeys[item] += 1
            else:
                tempKeys[item] = 1   
    copyKeys = {}
    for key in tempKeys:
        tempKey = key.lower()
        copyKeys[tempKey] = (tempKeys[key] * -0.4) + 10
    
    tempKeys = copyKeys

    
    print(tempKeys)
    return tempKeys


    


    #testVote = voteCounter(nomCand[basicAwards[i]])
    #testVote = sortVote(testVote)
    #nomCand[basicAwards[i]] = testVote
#$nomCand = onlyKnownNames(nomCand)

    


#testVote = nipNames(testVote)
#print(testVote)
def propNouns(allCan):
    print("Starting Prop Nouns")
    nnCand = []
    nlp = spacy.load("en_core_web_sm")
    for can in allCan:
        tweet = nlp(can)
        for i, tagged_token in enumerate(tweet):
            tempText = []
            if tagged_token.pos_ == "PROPN":
                tempText.append(tagged_token.text)
                k=i+1
                while k<len(tweet)-1 and tweet[k].pos_ == "PROPN" and "#" not in tweet.text and "http" not in tweet.text:
                        tempText.append(tweet[k].text)
                        k=k+1
                if len(tempText) >= 2:
                    tempText = " ".join(tempText)
                    nnCand.append(tempText)
                #print("TWEET: " + " ".join(tweet) + " NAME: " +tagged_token[0])
    with open('propNouns.txt', 'wb') as f:
        pickle.dump(nnCand, f)
    print("Finished Prop Nouns")
    return nnCand

def quickPropNouns(allCan):
    print("Starting Prop Nouns")
    nnCand = []
    nlp = spacy.load("en_core_web_sm")
    for tweet in nlp.pipe(allCan):
        for i, tagged_token in enumerate(tweet):
            tempText = []
            if tagged_token.pos_ == "PROPN":
                tempText.append(tagged_token.text)
                k=i+1
                while k<len(tweet)-1 and tweet[k].pos_ == "PROPN" and "#" not in tweet[k].text and "http" not in tweet[k].text:
                        tempText.append(tweet[k].text)
                        k=k+1
                if len(tempText) >= 2:
                    tempText = " ".join(tempText)
                    nnCand.append(tempText)
                #print("TWEET: " + " ".join(tweet) + " NAME: " +tagged_token[0])
    print("Finished Prop Nouns")
    return nnCand



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

def matchNames(names, year, awardKeys, award_dict):
    print("Matching Names...")
    newDict = {}
    file_name = 'gg{}.json'.format(year)
    pand = pandas.read_json(file_name)
    for row in pand.itertuples():
        tweet = row[1]
        tweet = tweet.lower()
        for name in names:
            name = name.lower()
            if name in tweet:
                newAdditions = []
                for word in awardKeys:
                    if word in tweet:
                        newAdditions.append(word)
                if name in newDict and len(newAdditions) > 0:
                    for item in newAdditions:
                        newDict[name].append(item)
                elif len(newAdditions) > 0:
                    newDict[name] = newAdditions
    tempDict = {}
    print("Finished Matching Names!")
    for words in newDict:
        tempDict[words] = sortVote(voteCounter(newDict[words]))
    return tempDict

def quickMatchNames(names, year, awardKeys):
    print("Matching Names...")
    newDict = {}
    counterDict = {}
    file_name = 'gg{}.json'.format(year)
    pand = pandas.read_json(file_name)
    for name in names:
        name = name.lower()
        pand['text'] = pand['text'].str.lower()
        brandy = pand[pand['text'].str.contains(name)]
        for word in awardKeys:
            brandy2 = brandy[brandy['text'].str.contains(word)]
            counterDict[word] = len(brandy2['text'].tolist())
        newDict[name] = counterDict
    tempDict ={}
    print("Finished Matching Names!")
    for words in newDict:
        tempDict[words] = sortVote(newDict[words])
    return tempDict
                

def filterNames(names, awardKeys):
    print("Started Filter Names")
    filtered = names.copy()
    for name in names:
        tempName = name.lower()
        if any(x in tempName for x in awardKeys) or names[name] < 2 or "RT" in name or "golden" in name:
            if name in filtered:
                del(filtered[name])
    print("Finished Filter Names!")
    return filtered

def voteCategories(namesAndKeywords, awards):
    tempDict ={}
    for keys in namesAndKeywords:
        tempkeys = namesAndKeywords[keys]
        if len(tempkeys) >= 5:
            tempkeys = list(tempkeys)
            tempkeys = tempkeys[-5:]
        else:
            tempkeys = tempkeys
        tempDict[keys] = tempkeys
    
    namesAndKeywords = tempDict
    posCat = {}
    for name in namesAndKeywords:
        for award in awards:
            for item in awards[award]:
                item = item.lower()
                if item in namesAndKeywords[name] and item != "best" and item != "award" and item != "picture" and item != "motion":
                    if name in posCat:
                        posCat[name].append(award)
                    else:
                        posCat[name] = [award]

    
    return posCat

        
def finalizeCategories(nameDict, awardDict):
    finalAwards = {}
    for item in awardDict:
        finalAwards[item] = []
    for name in nameDict:
        rev = reversed(list(nameDict[name].keys()))
        posCat = nameDict[name]
        for item in rev:
            if len(finalAwards[item]) >= 4:
                continue
            else:
                finalAwards[item].append(name)
                break
    for item in finalAwards:
        while len(finalAwards[item]) < 4:
            finalAwards[item].append("paul bunyon")
    return finalAwards

          
            

def findAllNominees(year):
    keyDict = get_awardsKeywords(basicAwards)
    scoreDict = get_unique_keys(keyDict)
    nomCand = []
    person_award_criteria = ["actor", "actress", "score", "song", "cecil", "director"]
    award_dict = {a: [nltk.word_tokenize(a)] for a in basicAwards}
    temp = {}
    tempDict = award_dict.copy()
    for award in tempDict:
        temp = award.lower()
        award_dict[temp] = award_dict[award]
        del(award_dict[award])

    for award in award_dict:

        for item in award_dict[award]:
            for miniitem in item:
                miniitem = miniitem.lower()
                if miniitem in person_award_criteria:
                    award_dict[award] = "person"
                    break
    for award in award_dict:
        if award_dict[award] != "person":
            award_dict[award] = "movie"
    flattenedAwardKeys = []
    for keyword in keyDict:
        for item in keyDict[keyword]:
            flattenedAwardKeys.append(item.lower())
    flattenedAwardKeys = set(flattenedAwardKeys)
    nomCand = quickNomGather(award_dict, year)
    #with open("prereadtweets.txt", 'rb') as f:
    #    nomCand = pickle.load(f)
    propN = quickPropNouns(nomCand)
    propN = voteCounter(propN)
    propN = filterNames(propN, flattenedAwardKeys)
    propN = sortVote(propN)
    propN = matchNames(propN, year, flattenedAwardKeys, award_dict)
    propN = voteCategories(propN, keyDict)
    for item in propN:
        propN[item] = voteCounter(propN[item])
        propN[item] = sortVote(propN[item])
    propN = finalizeCategories(propN, keyDict)
    propN = translate(propN)
    return propN
                    



def main():
    nominees = findAllNominees(2013)
    for award in nominees:
        print(award)
        print('\n')
        print(nominees[award])
        print('\n')
    return

if __name__ == '__main__':
    main()

#print(get_nominees_raw(2013, basicAwards))
