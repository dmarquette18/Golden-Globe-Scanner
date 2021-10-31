import pandas as pd
from nltk import word_tokenize, pos_tag_sents, pos_tag
import spacy
import re
import collections as col

nlp = spacy.load("en_core_web_sm")

gg = ['golden', 'globe', 'globes', 'Golden', 'Globe', 'Globes', 'goldenglobes', 'GoldenGlobes','RT']
OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
award_weights = {'supporting': 10, 'drama': 10, 'comedy': 10, 'made': 10}

#def findNthMostCommon(dictio, n):


def chooseAwards(year):
    if year > 2015:
        awards = OFFICIAL_AWARDS_1819
    else:
        awards = OFFICIAL_AWARDS_1315
    return awards

def awardWords(year):
    if year > 2015:
        awardNames = OFFICIAL_AWARDS_1819
    else:
        awardNames = OFFICIAL_AWARDS_1315
    awardWords = set()
    for award in awardNames:
        words = word_tokenize(award)
        for word in words:
            if len(word) > 3:
                awardWords.add(word)
    return awardWords

def addTallyToDict(strng, dictio):
    if strng in dictio:
        dictio[strng] += 1
    else:
        dictio[strng] = 1

def data(year):
    file_name = 'gg{}.json'.format(year)
    tweets = pd.read_json(file_name)
    return tweets

def presenterTweets2(tweets):
    allPresentTweets = tweets[tweets['text'].str.contains('(?i)presenting|presenter|presented|presents')]
    relPresentTweets = allPresentTweets[~allPresentTweets['text'].str.contains('(?i)represent')]
    return relPresentTweets

# Using Spacy
def process(pres, award_words):
    """
    inputs:
        df pres of tweets with the word "present" in them
        set award_words of keywords of awards, e.g. 'comedy', 'musical', 'actor'...
    returns:
        dictionary ppl of form {presenter: {award_word1: x, award_word2: y ...}}
    """
    ppl = {} # {presenter: {award_word1: x, award_word2: y ...}}
    for i in pres['text']:
        i = nlp(i)
        peeps = set()
        award_keywords = []

        for token in i:
            if token.text.lower() in award_words:
                award_keywords.append(token.text.lower())
        for ent in i.ents:
            if ent.label_ == 'PERSON' and 2 <= len(ent.text.split()) <= 3 and not any([char in ['&', 'RT', '@', ':', '/'] for char in ent.text]):
                nameParts = ent.text.split()
                for name in nameParts:
                    # check if it's a name and has 's => redundant
                    if "'s" in name:
                        nameParts[nameParts.index(name)] = re.sub("'s", '', name)
                    # check to see if present was part of the name
                    if 'present' in name.lower():
                        nameParts.remove(name)
                if len(nameParts) >= 2:
                    peeps.add(' '.join(nameParts).lower())
        for peep in peeps:
            if peep not in ppl:
                ppl[peep] = {}
            for keyword in award_keywords:
                    addTallyToDict(keyword, ppl[peep])
    return(ppl)
"""
def findPresenters(awardNames, awardWeights, scanDict):
    ###
    #inputs:
    #    awardNames is a list
    #    awardWeights is a dict - {word1: num, word2: num}
    #   scanDict is a dict - {presenter1: {keyword1: count, keyword2: count}
    #                        presenter2: {keyword1: count, keyword2: count}}
    #returns: 
    #    dictionary finalMapping pf form {awardName1: [presenter1, presenter2], awardName2: [presenter1, presenter2]...}
    ###
    # make a result dictionary - {awardName: [presenter1, presenter2]}
    finalMapping = {}
    tempMapping = {}
    presAwardVotes = {}
    for presenter in scanDict:

    for award in awardNames:
        finalMapping[award] = []
    # loop over presenters and find match
    for presenter in scanDict:
        matchNum = {}
        for award in awardNames:
            matchNum[award] = 0
        for award in matchNum:
            for word in scanDict[presenter]:
                if word in award:
                    score = scanDict[presenter][word]
                    if word in awardWeights:
                        score *= awardWeights[word]
                    matchNum[award] += score
    unassigned = []
    for presenter in scanDict:
        unassigned.append(presenter)
    for award in awardNames:
        for presenter in 
        #matched = max(matchNum, key=matchNum.get)
        #tempMapping[matched].append(presenter)
    return finalMapping
"""
def findPresenters(awardNames, awardWeights, scanDict):
    ###
    #inputs:
    #    awardNames is a list
    #    awardWeights is a dict - {word1: num, word2: num}
    #   scanDict is a dict - {presenter1: {keyword1: count, keyword2: count}
    #                        presenter2: {keyword1: count, keyword2: count}}
    #returns: 
    #    dictionary finalMapping pf form {awardName1: [presenter1, presenter2], awardName2: [presenter1, presenter2]...}
    ###
    # make a result dictionary - {awardName: [presenter1, presenter2]}
    finalMapping = {}
    tempMapping = {}
    for award in awardNames:
        finalMapping[award] = []
    # loop over presenters and find match
    for presenter in scanDict:
        matchNum = {}
        for award in awardNames:
            matchNum[award] = 0
        for award in matchNum:
            for word in scanDict[presenter]:
                if word in award:
                    score = scanDict[presenter][word]
                    if word in awardWeights:
                        score *= awardWeights[word]
                    matchNum[award] += score
        matched = max(matchNum, key=matchNum.get)
        tempMapping[matched].append(presenter)
    for award in finalMapping:
        if finalMapping[award] == []:
            finalMapping[award].append('Bob Builder')
    return finalMapping


#print(ppl)
#for person in ppl:
#    print(person)
#    for wrd, count in ppl[person].items():
#        print('\t', wrd, ': ', count)

def presenter(year):
    award_names = chooseAwards(year)
    award_words = awardWords(year)
    df = data(year)
    pres = presenterTweets2(df)
    ppl = process(pres, award_words)
    #for key, val in ppl.items():
    #    print(key, ': ', val)
    final = findPresenters(award_names, award_weights, ppl)
    return final
    #for key, value in final.items():
    #    print(key, ': ', value)

   
#fin = presenter(2013)
#for key, value in fin.items():
#    print(key, ': ', value)
