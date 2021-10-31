import pandas as pd
from nltk import word_tokenize, pos_tag_sents, pos_tag
import spacy
#import en_core_web_sm
import re


#nlp = en_core_web_sm.load()
nlp = spacy.load("en_core_web_sm")

gg = ['golden', 'globe', 'globes', 'Golden', 'Globe', 'Globes', 'goldenglobes', 'GoldenGlobes','RT']
OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
awardWeights = {'supporting': 10, 'drama': 10, 'comedy': 10, 'made': 10}

def findPresenters(awardNames, awardWeights, scanDict):
    """
    awardNames is a list
    awardWeights is a dict - {word1: num, word2: num}
    scanDict is a dict - {presenter1: {keyword1: count, keyword2: count}
                          presenter2: {keyword1: count, keyword2: count}}
    """
    # make a result dictionary - {awardName: [presenter1, presenter2]}
    finalMapping = {}
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
        finalMapping[matched].append(presenter)
    return finalMapping


def addTallyToDict(strng, dictio):
    if strng in dictio:
        dictio[strng] += 1
    else:
        dictio[strng] = 1

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

def data(year):
    file_name = 'gg{}.json'.format(year)
    tweets = pd.read_json(file_name)
    return tweets

def presenterTweets(tweets):
    allPresentTweets = tweets[tweets['text'].str.contains('(?i)presenting|presenter|presented|presents')]
    relPresentTweets = allPresentTweets[~allPresentTweets['text'].str.contains('(?i)represent')]
    taggedTweets = pos_tag_sents(relPresentTweets['text'].apply(word_tokenize).tolist())
    return taggedTweets

def presenterTweets2(tweets):
    allPresentTweets = tweets[tweets['text'].str.contains('(?i)presenting|presenter|presented|presents')]
    relPresentTweets = allPresentTweets[~allPresentTweets['text'].str.contains('(?i)represent')]
    return relPresentTweets

def Di(taggedTweets):
    votes = {}
    for tweet in taggedTweets:
        for i in range(len(tweet[:-1])):
            if tweet[i][1] == 'NNP' and tweet[i+1][1] == 'NNP' and tweet[i][0].isalpha() and tweet[i+1][0].isalpha():
                if tweet[i][0] in gg or tweet[i+1][0] in gg:# or not tweet[i][0].isalpha() or not tweet[i+1][0].isalpha():
                    pass
                else:
                    fname_lname = ' '.join([tweet[i][0].lower(), tweet[i+1][0].lower()])
                    #if fname_lname.lower() in list(map(lambda x: x.lower(), list(votes.keys()))):
                    if fname_lname in votes.keys():
                        votes[fname_lname] += 1
                    else:
                        votes[fname_lname] = 1
    sortedVotes = sorted(votes.items(), key=lambda x: x[1], reverse=True)
    return sortedVotes

award_words = awardWords(2013)
#print(award_words)

df = data(2013)
"""
pres = presenterTweets(df)
di = Di(pres)
for key in di:
    split = pos_tag(key[0].split())
    print(split)
"""
#for key, value in Di(pres).items():
#    print(key, ': ', value)

# tried to use spacy
def process(pres):
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

#print(ppl)
#for person in ppl:
#    print(person)
#    for wrd, count in ppl[person].items():
#        print('\t', wrd, ': ', count)

award_words = awardWords(2013)
df = data(2013)
pres = presenterTweets2(df)
ppl = process(pres)
final = findPresenters(OFFICIAL_AWARDS_1315, awardWeights, ppl)
for key, value in final.items():
    print(key, ': ', value)




#for pp in ppl:
#    print(pp)

#try:
#    print(pres.head())
#except:
#    print(pres)



#di2 = [tup[0] for tup in di]
#for i in di2:
#    print(i)

"""
# Uses txt file of presenters and awards and sees if the names I got are in the txt file
file1 = open('preswiki.txt', 'r')
Lines = file1.readlines()
#print(Lines)
for line in Lines:
    split = line.split()
    if ' '.join(split[:2]).lower() in ppl:
        print(' '.join(split[:2]).lower(), 'yes')
    else:
        print(' '.join(split[:2]).lower(), 'no')
"""
"""
# look at the Aziz Tweets
allPresentTweets = df[df['text'].str.contains('(?i)presenting|presenter|presented|presents')]
pres1 = allPresentTweets[~allPresentTweets['text'].str.contains('(?i)represent')]
aziz = pres1[pres1['text'].str.contains('(?i)christian bale')]
for i in aziz['text']:
    print(pos_tag(word_tokenize(i)))
    print(aziz.shape[0])
"""
"""
df = data(2013)
pres = presenterTweets(df)
for i in range(100):
    print(pres['text'].iloc[i])
    print(pres['timestamp_ms'].iloc[i], '\n')
print(pres.shape[0])
x=3
print(pres.info())
"""
