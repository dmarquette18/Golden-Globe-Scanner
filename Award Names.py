import pandas
import itertools
from CanGather import canGather
from VoteSystem import voteCounter, sortVote
from trimmer import scoreCalc

df2013 = pandas.read_json("c:/Users/dmarq/Downloads/GG Scanner/gg2013.json")
awardCand = []
for row in df2013.itertuples():
    tweet = row[1]

    tweet = tweet.lower()
    
    tweet = tweet.replace("the golden globe for", "")
    tweet = tweet.replace("golden globe for", "")

    tweet = tweet.split()

    totAwards = []
    for twt in tweet:
        if twt == "best":
            #if its there, gather all words that come after it individually
            tempAward = awardCand.copy()
            awardCand = canGather(tweet.index(twt), tweet, True, tempAward)
            continue
            

    
    #eliminate the shorter ones that are the same as bigge ones
inter = voteCounter(awardCand)
i=0
for k in inter.keys():
    if inter[k] > 25:
        print(k + ": " + str(inter[k]))
        print("\n")

#print(sortVote(finalAwardCands))

