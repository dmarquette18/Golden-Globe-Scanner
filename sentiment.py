import pandas as pd
import numpy as np
from textblob import TextBlob

def get_list_from_dict(d):
    l = []
    for item in d: 
        if type(d[item]) != list and d[item] not in l: 
            l.append(d[item])
    return l

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

def get_sentiments(df, winner_dict): 
    winner_list = get_list_from_dict(winner_dict)
    winner_df = get_tweets_from_list(df, winner_list)
    winner_df = winner_df.dropna(how='all')
    winner_sentiment = get_sentiment(winner_df, winner_list)
    return winner_sentiment
            