import pandas as pd
import numpy as np
from textblob import TextBlob
import pickle

drop_list = ['by', 'in', 'a', '-', 'or', 'an', ',', 'for', 'role','made']
with open("official_list.txt", 'rb') as f:
    OFFICIAL_AWARDS_1315, OFFICIAL_AWARDS_1819 = pickle.load(f)

def get_data(year):
    name = 'gg{}.json'.format(year)
    return pd.read_json(name)

def get_list_from_dict(d):
    l = []
    for item in d: 
        if type(d[item]) != list and d[item] not in l: 
            l.append(d[item])
    return l

def convert_official_to_dict(official): 
    official_to_abbr = {}
    for index, row in enumerate(official): 
        abbr = row.split(" ")
        abbr = [word for word in abbr if word not in drop_list]
        for word in row: 
            if word == 'television':
                row.append('tv')
        official_to_abbr[row] = abbr
    return official_to_abbr

def get_tweets_from_list(df, lis): 
    df = df.drop(['user','id','timestamp_ms'], axis=1)
    df.apply(lambda col : col.str.lower())
    winner_df = pd.DataFrame(np.nan, index=range(0, df.shape[0]), columns = lis)
    for i in range(0, len(lis)): 
        winner_df[lis[i]] = df[df['text'].str.contains(lis[i])]['text']
    return winner_df

def get_sentiment(df, lis): 
    result_sentiment = {}
    for winner in lis: 
        tweet_list = df[winner].dropna().tolist()
        total_score = 0 
        size = 0
        for tweet in tweet_list: 
            blob = TextBlob(tweet)
            score = blob.sentiment.polarity
            size += 1
            total_score += score
        if size == 0:
            continue 
        if total_score / size > 0.1: 
            result_sentiment[winner] = 'positive'
        elif total_score / size < -0.1:
            result_sentiment[winner] = 'negative'
        else: 
            result_sentiment[winner]= 'neutral'
    return result_sentiment

def get_sentiments(year, winner_dict, host_list):
    df = get_data(year)
    if year <= 2015:
        awards_dict = convert_official_to_dict(OFFICIAL_AWARDS_1315)
    else:
        awards_dict = convert_official_to_dict(OFFICIAL_AWARDS_1819)
    winner_list = get_list_from_dict(winner_dict)
    winner_df = get_tweets_from_list(df, winner_list).dropna(how='all')
    winner_sentiment = get_sentiment(winner_df, winner_list)
    
    host_df = get_tweets_from_list(df, host_list).dropna(how='all')
    host_sentiment = get_sentiment(host_df, host_list)

    # award_list = get_list_from_dict(awards_dict)
    # award_df = get_tweets_from_list(df, award_list).dropna(how='all')
    # award_sentiment = get_sentiment(award_df, award_list)
    return [winner_sentiment, presenter_sentiment]
            
