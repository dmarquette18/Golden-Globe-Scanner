import pandas as pd
import numpy as np 
import pickle

import spacy
import nltk
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
nlp = spacy.load("en_core_web_sm")
from nltk import word_tokenize, pos_tag_sents, pos_tag
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')
nltk.download('stopwords')

with open("official_list.txt", 'rb') as f:
    OFFICIAL_AWARDS_1315, OFFICIAL_AWARDS_1819 = pickle.load(f)


def get_data(year):
    name = 'gg{}.json'.format(year)
    return pd.read_json(name)

def extraction_winner_one_word(tweet: str, criteria: str, forward: bool): 
    candidate_answers = {}
    splits = word_tokenize(tweet)
    splits = [w for w in splits if not w.lower() in gg and w.lower().isalpha()]
    tags = pos_tag(splits)
    try: 
        index = splits.index(criteria)
    except ValueError: 
        index = -1
    if forward: 
        while index > 0:
            index -= 1
            if tags[index][1] == 'NNP' and tags[index-1][1] == 'NNP': 
                name = splits[index-1].lower() + " " + splits[index].lower()
                if name in candidate_answers:
                    candidate_answers[name] += 1
                else: 
                    candidate_answers[name] = 1
    else: 
        while index < len(splits) - 2: 
            index += 1
            if tags[index][1] == 'NNP':  
                curr = curr + " " + splits[index]
                candidate_answers.append(curr) 
    
    #sort the dict and return the highest vote result
    candidate_answers = sorted(candidate_answers.keys(), key = lambda item: item[1], reverse=True)
    if len(candidate_answers) == 0:
        return np.nan
    return candidate_answers
    
    #sort the dict and return the highest vote result
    candidate_answers = sorted(candidate_answers.keys(), key = lambda item: item[1], reverse=True)
    if len(candidate_answers) == 0:
        return None
    return candidate_answers

def extraction_winner_two_words(tweet: str, criteria: str, forward: bool): 
    candidate_answers = {}
    splits = word_tokenize(tweet)
    splits = [w for w in splits if not w.lower() in gg and w.lower().isalpha()]
    tags = pos_tag(splits)
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(criteria)]
    matcher.add(criteria, patterns)
    doc = nlp(tweet)
    matches = matcher(doc)
    persons = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
    for person in persons: 
        valid = True
        for word in person: 
            if word.lower() in gg or not word.lower().isalpha():
                valid = False
        if valid: 
            candidate_answers[person] = 1
    for match_id, start, end in matches:
        if forward: 
            while start > 1: 
                start -= 1
                if tags[start][1] == 'NNP' and tags[start-1][1] == 'NNP': 
                    name = splits[start-1].lower() + " " + splits[start].lower()
                    if name in candidate_answers:
                        candidate_answers[name] += 1
                    else: 
                        candidate_answers[name] = 1
        else: 
            while end < len(splits) - 2: 
                if tags[end][1] == 'NNP' and tags[end+1][1] == 'NNP': 
                    name = splits[end].lower() + " " + splits[end+1].lower()
                    if name in candidate_answers:
                        candidate_answers[name] += 1
                    else: 
                        candidate_answers[name] = 1
                end += 1
        
    #sort the dict and return the highest vote result
    candidate_answers = sorted(candidate_answers.keys(), key = lambda item: item[1], reverse=True)
    if len(candidate_answers) == 0:
        return np.nan
    return candidate_answers

def get_candidates(df, criterias, func, forward):
    df = df.drop(['user','id','timestamp_ms'], axis=1)
    df_answers = pd.DataFrame(np.nan, index=range(0, df.shape[0]), columns = criterias)
    for criteria in criterias: 
        copy = df[df['text'].str.contains(criteria)].copy()
        df_answers[criteria] = copy['text'].apply(func=func, args=(criteria, forward))
    return df_answers.dropna(how='all')

def get_candidates_df(df, before_list, after_list):
    result_before_one_word = get_candidates(df, before_list, extraction_winner_one_word, True)
    result_after_two_words = get_candidates(df, after_list, extraction_winner_two_words, False)
    candidates_df = result_after_two_words.join(result_before_one_word, how='outer')
    return candidates_df

def process_sub_df(df, candidates_df, awards_dict):
    award_winner = {}
    award_nominees = {}
    for award in awards_dict: 
        award_winner[award] = []
    for col in candidates_df: 
        series = candidates_df[col].dropna()
        sub = df.filter(items = series.index, axis = 0).merge(series, left_index=True, right_index=True).drop(['user','id','timestamp_ms'], axis=1)
        sub_result = result_find_official_awards(sub, awards_dict)
        for award in awards_dict:
            for name in sub_result[award]:
                award_winner[award].append(name)
    for award in award_winner:  
        count_dict = {}
        name_list = award_winner[award]
        for t in name_list:
            name, count = t[0], t[1]
            if name in count_dict: 
                count_dict[name] += count
            else: 
                count_dict[name] = 1
        result = sorted(count_dict.items(), key = lambda key: key[1], reverse=True)
        award_winner[award] = result[0][0]
        names = []
        for i in range(1,5): 
            if i > len(result) - 1:
                break
            names.append(result[i][0])
        award_nominees[award] = names
    return [award_winner, award_nominees]


def countResult(name_list): 
    count = {}
    for name in name_list: 
        if name not in count:
            count[name] = 1
        else: 
            count[name] += 1
    return sorted(count.items(), key = lambda item:item[1], reverse=True)

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

def check_award_present(award_dict, tweet, names): 
    max_count = 0
    max_award = []
    for award in award_dict: 
        count = 0
        for word in award_dict[award]:
            if word in tweet: 
                count += 1
        if count == max_count:
            max_award.append(award)
        elif count > max_count:
            max_count = count 
            max_award = [award]
    award_name = {}
    if max_count >= 3: 
        for award in max_award: 
            if 'actor' in award_dict[award] and 'actor' in tweet: 
                award_name[award] = names
            elif 'actress' in award_dict[award] and 'actress' in tweet: 
                award_name[award] = names
            elif 'television' in award_dict[award] and ('television' in tweet or 'tv' in tweet): 
                award_name[award] = names
            elif 'supporting' in award_dict[award] and 'supporting' in tweet: 
                award_name[award] = names
            elif 'actor' not in award_dict[award] and 'actress' not in award_dict[award] and 'supporting' not in award_dict[award] and 'television' not in award_dict[award]:
                award_name[award] = names
    return award_name

def result_find_official_awards(df, awards_dict):
    copy = df.copy(deep=False)
    award_winner = {}
    for award in awards_dict: 
        award_winner[award] = []
    for row in copy.itertuples(index = False): 
        tweet = row.text.lower()
        names = row[1]
        result = check_award_present(awards_dict, tweet, names)
        for award in result: 
            names = result[award]
            for name in names: 
                award_winner[award].append(name)
    for key in award_winner: 
        #name count for each award in the award_winner dict
        #count would be the name of the highest count
        count = countResult(award_winner[key]) 
        if len(count) != 0:
            award_winner[key] = count
    return award_winner 

before_list = ['nominated','won', 'wins','honored']

after_list =  ['goes to']

gg = ['golden', 'globe', 'globes','goldenglobes', 'rt', '@', 'a', 'God', 'thank', "'\'", 'lmao','hi','hey','fuck','wtf','yes']

drop_list = ['by', 'in', 'a', '-', 'or', 'an', ',', 'for', 'role','made']

# df2013 = get_data(2013)

# result_before_one_word = get_candidates(df2013, 'won', extraction_winner_one_word, True)

# sub2013 = getDfCandidateText(df2013)

# awards_dict = convert_official_to_dict(OFFICIAL_AWARDS_1315)

# result_find_official_awards(sub2013, awards_dict)

result = []

def get_result(year): 
    df = get_data(year)
    candidates_df = get_candidates_df(df, before_list, after_list)
    if year <= 2015:
        awards_dict = convert_official_to_dict(OFFICIAL_AWARDS_1315)
    else:
        awards_dict = convert_official_to_dict(OFFICIAL_AWARDS_1819)
    result = process_sub_df(df, candidates_df, awards_dict)
    return result

def get_winners(year): 
    if len(result) == 0:
        return get_result(year)[0]
    else: 
        return result[0]

def get_nominee(year): 
    if len(result) == 0:
        return get_result(year)[1]
    else: 
        return result[1]
