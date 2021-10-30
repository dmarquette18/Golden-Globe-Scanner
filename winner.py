import pandas as pd
import numpy as np 
import nltk
import pickle

# import spacy
# from spacy.matcher import Matcher
# nlp = spacy.load("en_core_web_sm")
from nltk import word_tokenize, pos_tag_sents, pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')

with open("official_list.txt", 'rb') as f:
    OFFICIAL_AWARDS_1315, OFFICIAL_AWARDS_1819 = pickle.load(f)


def get_data(year):
    name = 'gg{}.json'.format(year)
    return pd.read_json(name)

def extraction_winner_one_word(tweet: str, criteria: str, forward: bool): 
    candidate_answers = {}
    splits = word_tokenize(tweet)
    tags = pos_tag(splits)
    try: 
        index = splits.index(criteria)
    except ValueError: 
        return None
    if forward: 
        while index > 0:
            index -= 1
            if tags[index][1] == 'NNP' and tags[index-1][1] == 'NNP': 
                if splits[index] not in gg and splits[index-1] not in gg: 
                    name = splits[index-1] + " " + splits[index]
                    if name in candidate_answers:
                        candidate_answers[name] += 1
                    else: 
                        candidate_answers[name] = 1
    else: 
        while index < len(splits) - 1: 
            index += 1
            if tags[index][1] == 'NNP':  
                curr = curr + " " + splits[index]
                candidate_answers.append(curr) 
    
    #sort the dict and return the highest vote result
    candidate_answers = sorted(candidate_answers.keys(), key = lambda item: item[1], reverse=True)
    if len(candidate_answers) == 0:
        return None
    return candidate_answers

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

def get_candidates(df, criteria, func, forward):
    df_answers = pd.DataFrame(columns=[criteria]) 
    df_answers[criteria] = pd.Series(np.vectorize(func)(df['text'], [criteria for _ in range(df.shape[0])], [forward for _ in range(df.shape[0])]))
    #df_answers[criteria] = pd.Series(map(func, df['text'], [criteria for _ in range(df.shape[0])], [forward for _ in range(df.shape[0])]))
    return df_answers.dropna(how="all")

def getDfCandidateText(df):
    return df.filter(items = result_before_one_word.index, axis = 0).merge(result_before_one_word, left_index=True, right_index=True).drop(['user','id','timestamp_ms'], axis=1)

def countResult(name_list): 
    count = {}
    for name in name_list: 
        if name not in count:
            count[name] = 1
        else: 
            count[name] += 1
    return sorted(count.items(), key = lambda item:item[1], reverse=True)

def resultFindAward(df, criteria, awards):
    award_winner = {}
    def find_award(tweet, names): 
        index = -1
        for award in awards:
            if award in tweet:
                award_winner[award] = names[0]
    np.vectorize(find_award)(df['text'], df[criteria])
    return sorted(award_winner.items(), key = lambda item:item[1], reverse=True)  

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

def check_award_present(award_dict, award, tweet, names): 
    count = 0
    for word in award_dict[award]:
        if word in tweet: 
            count += 1
    if (len(award_dict[award]) > 4 and count >= 4) or (len(award_dict[award]) <= 4 and count >= 3): 
        return names
    return []

def result_find_official_awards(df, awards_dict):
    copy = df.copy(deep=False)
    award_winner = {}
    for award in awards_dict: 
        award_winner[award] = []
    for row in copy.itertuples(index = False): 
        tweet = row.text.lower()
        names = row[1]
        for award in awards_dict:
            result = check_award_present(awards_dict, award, tweet, names)
            if len(result) > 0: 
                for name in result: 
                    award_winner[award].append(name)
    for key in award_winner: 
        #name count for each award in the award_winner dict
        #count would be the name of the highest count
        count = countResult(award_winner[key]) 
        if len(count) != 0:
            award_winner[key] = count[0][0]
    return award_winner 

before_list = ['won', 'wins', 'winning', 'win', 'got', 'getting', 'gets', 'get', 'took', 'takes', 'taking',
               'take', 'deserves', 'accepts', 'accepted', 'honored', 'nominated', 'receives', 'received']
before_double_list = ['for winning', 'getting nominated','was named' ]

after_list =  ['congratulates', 'announce', 'nominated', 'wtf', 'nominee']
after_double_list = ['goes to', 'awarded to', 'cheer for', 'cheering for', 'cheering on', 'congratulations to']

gg = ['golden', 'globe', 'globes', 'Golden', 'Globe', 'Globes', 'goldenglobes', 'GoldenGlobes','RT', '@', 'a', 'A', 'God', 'god', 'thank', 'Thank',"'\'"]

drop_list = ['by', 'in', 'a', '-', 'or', 'an', ',', 'for', 'role','made']

# df2013 = get_data(2013)

# result_before_one_word = get_candidates(df2013, 'won', extraction_winner_one_word, True)

# sub2013 = getDfCandidateText(df2013)

# awards_dict = convert_official_to_dict(OFFICIAL_AWARDS_1315)

# result_find_official_awards(sub2013, awards_dict)

def winner(year): 
    df = get_data(year)
    result_before_one_word = get_candidates(df, 'won', extraction_winner_one_word, True)
    sub = getDfCandidateText(df)
    awards_dict = convert_official_to_dict(OFFICIAL_AWARDS_1315)
    result = result_find_official_awards(sub, awards_dict)
    return result
