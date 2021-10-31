import numpy as np
import pandas as pd 
import spacy
nlp = spacy.load("en_core_web_sm")

#find tweets with "act"
#find the quoted portion inside the tweet, which captures the act. 

def find_tweets_red_carpet(df): 
    red_carpet_df = pd.DataFrame()
    for index, row in df.iterrows(): 
        if 'dressed' in row['text'].lower().split():
            red_carpet_df = red_carpet_df.append(row) 
    return red_carpet_df

def find_worst(df):
    df = df[df['text'].str.contains('worst')]
    candidate = {} 
    for index, row in df.iterrows(): 
        doc = nlp(row['text'].lower())
        candidates = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
        for c in candidates: 
            if c in candidate: 
                candidate[c] += 1
            else: 
                candidate[c] = 1
    candidate = sorted(candidate.items(), key = lambda item: item[1], reverse=True)
    return candidate

def find_best(df):
    df = df[df['text'].str.contains('best')]
    candidate = {} 
    for index, row in df.iterrows(): 
        doc = nlp(row['text'].lower())
        candidates = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
        for c in candidates: 
            if c in candidate: 
                candidate[c] += 1
            else: 
                candidate[c] = 1
    candidate = sorted(candidate.items(), key = lambda item: item[1], reverse=True)
    return candidate

def find_controversial(df): 
    worst = find_worst(df)
    best = find_best(df)
    count = {}
    for t in worst: 
        for i in best: 
            if t[0] == i[0]: 
                count[t[0]] = t[1] + i[1]
    count = sorted(count.items(), key = lambda item: item[1], reverse=True)
    for i in count: 
        if i[0].find('rt') == -1:
            return i[0]
    return count[0][0]


def red_carpet(df):
    red_carpet_df = find_tweets_red_carpet(df).drop(['id', 'timestamp_ms','user'], axis=1)
    ans = {'worst dressed': "", 
           'best dressed': "",
          'most controversial': ''}
    ans['worst dressed'] = find_worst(red_carpet_df)[0][0]
    ans['best dressed'] = find_best(red_carpet_df)[0][0]
    ans['most controversial'] = find_controversial(red_carpet_df)
    return ans
