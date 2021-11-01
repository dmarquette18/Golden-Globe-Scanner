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


def findAwardNames(year):
    basic_words = ["was", "an", "or", "a", "the", "more", 'to', "for", "golden", "globe", 's"', "in", "that", "you", "ever", "as", "be", "i", "at", "ben", "with", "and", "but", "&amp;", "is", "of", "those", "he", "she", "rt", "have", "all", "we", "so", "it", "on", "by", "les", "dress", "dressed", "this", "her"]

    file_name = 'gg{}.json'.format(year)
    df2013 = pandas.read_json(file_name)
    awardCand = []
    for row in df2013.itertuples():
        tweet = row[1]

        tweet = tweet.lower()

        tweet = tweet.replace("the golden globe for", "")
        tweet = tweet.replace("golden globe for", "")
        tweet = tweet.replace("the golden globe", "")
        tweet = tweet.replace("the golden globes", "")
        tweet = tweet.replace("#goldenglobe", "")

        tweet = tweet.split()

        for i, twt in enumerate(tweet):
            if twt == "best":
                #if its there, gather all words that come after it individually
                temp = canGather(tweet.index(twt), tweet, "best")
                awardCand.append(temp)
                continue
            if twt == "wins":
                temp = canGather(tweet.index(twt), tweet, "forward")
                awardCand.append(temp)
                continue
            if twt == "goes":
                temp = canGather(tweet.index(twt), tweet, "goes")
                awardCand.append(temp)
                continue

    flat_list = [item for sublist in awardCand for item in sublist]


    inter = voteCounter(flat_list)
    inter = sortVote(inter)
    inter = unifySpaces(inter)
    above20 = dict()
    for can in inter:
        if inter[can] > 30:
            above20[can] = inter[can]

    inter = above20

    wordVote = commonality(inter)




    sum = 0
    for word in wordVote.keys():
        sum += wordVote[word]

    mean = sum/len(wordVote)

    #print(wordVote)

    #gather the top 15 most common words in all tweets
    topWords = []
    for l in list(reversed(list(wordVote)))[0:10]:
        #print(l + ": " + str(wordVote[l]))
        topWords.append(l)


    sum=0
    scoreDict = dict()
    for word in topWords:
        val = wordVote[word]/(mean*2)
        #a = 0.1
        #b = 1.1
        #val = (wordVote[word]/(mean*3))
        #val = a*(b ** val)
        val = (0.2 * val) + 1
        scoreDict[word] = val

    scoreDict = sortVote(scoreDict)
    scoreDict[list(scoreDict.keys())[-1]] = scoreDict[list(scoreDict.keys())[-2]]



    #add to the score if one of those top 15 words is present
    garbage = []
    newSumCand = {}
    for keyT in inter.keys():
        seenWords = []
        newSumCand[keyT] = 0
        test = keyT.split()
        for word in test:
            if word in wordVote:
                if word in topWords and word not in seenWords: 
                    newSumCand[keyT] = newSumCand[keyT] + scoreDict[word]
                    seenWords.append(word)
                elif word in topWords and word in seenWords:
                    newSumCand[keyT] = -1000
                elif word not in basic_words:
                    newSumCand[keyT] = newSumCand[keyT] - 3
                    garbage.append(word)


    sortgarbage = voteCounter(garbage)
    sortgarbage = sortVote(sortgarbage)


    sorted = sortVote(newSumCand)
    sorted = endRemove(sorted)
    sorted = unifySpaces(sorted)
    sorted = trimToBest(sorted)
    sorted = sortVote(sorted)
    #print(sortgarbage)

    aboveGround = dict()
    for item in sorted:
        if sorted[item] > 0:
            aboveGround[item] = sorted[item]

    wordVote = commonality(aboveGround)

    sum = 0
    for word in wordVote.keys():
        sum += wordVote[word]

    mean = sum/len(wordVote)

    #print(wordVote)

    #gather the top 15 most common words in all tweets
    topWords = []
    for l in list(reversed(list(wordVote)))[0:10]:
        #print(l + ": " + str(wordVote[l]))
        topWords.append(l)


    sum=0
    scoreDict = dict()
    for word in topWords:
        val = wordVote[word]/(mean*2)
        #a = 0.1
        #b = 1.1
        #val = (wordVote[word]/(mean*3))
        #val = a*(b ** val)
        val = (0.9 * val) + 1
        scoreDict[word] = val

    scoreDict = sortVote(scoreDict)
    scoreDict[list(scoreDict.keys())[-1]] = scoreDict[list(scoreDict.keys())[-2]]

    garbage = []
    newSumCand = {}
    for keyT in aboveGround.keys():
        seenWords = []
        newSumCand[keyT] = 0
        test = keyT.split()
        for word in test:
            if word in wordVote:
                if word in topWords and word not in seenWords: 
                    newSumCand[keyT] = newSumCand[keyT] + scoreDict[word]
                    seenWords.append(word)
                elif word in topWords and word in seenWords:
                    newSumCand[keyT] = -1000
                elif word not in basic_words:
                    newSumCand[keyT] = newSumCand[keyT] - 4
                    garbage.append(word)

    sorted = sortVote(newSumCand)
    sorted = endRemove(sorted)
    sorted = unifySpaces(sorted)
    sorted = trimToBest(sorted)
    sorted = purgeSame(sorted)
    sorted = nipNames(sorted)
    sorted = sortVote(sorted)
    newSorted = []
    for l in list(reversed(list(sorted)))[0:20]:
        newSorted.append(l)
    return newSorted

