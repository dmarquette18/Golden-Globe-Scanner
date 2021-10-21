import pandas as pd
from nltk import word_tokenize, pos_tag_sents

gg = ['golden', 'globe', 'globes', 'Golden', 'Globe', 'Globes', 'goldenglobes', 'GoldenGlobes','RT']

def data(year):
    file_name = 'gg{}.json'.format(year)
    tweets = pd.read_json(file_name)
    return tweets

def hostTweets(tweets):
    allHostTweets = tweets[tweets['text'].str.contains('(?i)host')]
    relHostTweets = allHostTweets[~allHostTweets['text'].str.contains('(?i)should|next year')]
    taggedTweets = pos_tag_sents(relHostTweets['text'].apply(word_tokenize).tolist())
    return taggedTweets

def findHosts(taggedTweets):
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
    host1 = sortedVotes[0][0]
    host2 = ''
    if sortedVotes[1][1] >= 0.6*votes[host1]:
        host2 = sortedVotes[1][0]
    if host2 == '':
        return [host1]
    else:
        return[host1, host2]

tweets = data(2015)
taggedTweets = hostTweets(tweets)
hosts = findHosts(taggedTweets)
print(hosts)


#def sortDict(dictio):
#    return dict(sorted(dictio.items(), key=lambda x: x[1], reverse=True))

#for key, value in sortDict(votes).items():
#    print(key, ': ', value)

