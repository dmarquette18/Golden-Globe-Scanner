import pandas as pd
import numpy as np 

def get_data(year):
    name = 'gg{}.json'.format(year)
    return pd.read_json(name)

def extraction_winner_one_word(tweet: str, criteria: str, forward: bool): 
    candidate_answers = []
    splits = tweet.lower().split()
    try: 
        index = splits.index(criteria)
    except ValueError: 
        return None
    curr = ""
    if forward: 
        while index > 0:
            index -= 1
            curr = splits[index] + " " + curr 
            candidate_answers.append(curr) 
    else: 
        while index < len(splits) - 1: 
            index += 1
            curr = curr + " " + splits[index]
            candidate_answers.append(curr) 
    return vote_candidate(candidate_answers)

def extraction_winner_two_words(tweet: str, criteria: str, forward: bool): 
    candidate_answers = []
    splits = tweet.lower().split()
    count = 0
    index = None
    for i in range(len(splits) - 1):
        if splits[i] == criteria.split()[0] and splits[i+1] == criteria.split()[1]:
            index = i
    if index == None:
        return None 
    curr = ""
    if forward: 
        while index >= 0:
            index -= 1
            curr = splits[index] + " " + curr
            candidate_answers.append(curr)
    else:  
        index += 2
        while index < len(splits):
            curr = curr + " " + splits[index]
            candidate_answers.append(curr) 
            index += 1
    return vote_candidate(candidate_answers)

def vote_candidate(candidates: list):
    cand = dict()
    for curr in candidates:
        splits = curr.split()
        string = splits[0]
        index = 0
        while index < len(splits) - 1:
            if string in cand:
                cand[string]+=1
            else:
                cand[string]=1
            index += 1
            string = string + " " + splits[index]
    return sorted(cand.items(), key = lambda item: item[1], reverse=True)[:2]

def get_candidates(df, lst, func, forward):
    df_answers = pd.DataFrame(columns=lst) 
    for i in lst: 
        df_answers[i] = pd.Series(map(func, df['text'], [i for _ in range(df.shape[0])], [forward for _ in range(df.shape[0])]))
    return df_answers.dropna(how="all")

df2013 = get_data(2013)
before_list = ['won', 'wins', 'winning', 'win', 'got', 'getting', 'gets', 'get', 'took', 'takes', 'taking',
               'take', 'deserves', 'accepts', 'accepted', 'honored', 'nominated', 'receives', 'received']
before_double_list = ['for winning', 'getting nominated','was named' ]

after_list =  ['congratulates', 'announce', 'nominated', 'wtf', 'nominee']
after_double_list = ['goes to', 'awarded to', 'cheer for', 'cheering for', 'cheering on', 'congratulations to']

get_candidates(df2013, before_list, extraction_winner_one_word, True)
get_candidates(df2013, after_double_list, extraction_winner_two_words, False)
