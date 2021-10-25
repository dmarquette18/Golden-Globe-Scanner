import pandas as pd
import numpy as np 

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

df2013 = get_data(2013)
before_list = ['won', 'wins', 'winning', 'win', 'got', 'getting', 'gets', 'get', 'took', 'takes', 'taking',
               'take', 'deserves', 'accepts', 'accepted', 'honored', 'nominated', 'receives', 'received']
before_double_list = ['for winning', 'getting nominated','was named' ]

after_list =  ['congratulates', 'announce', 'nominated', 'wtf', 'nominee']
after_double_list = ['goes to', 'awarded to', 'cheer for', 'cheering for', 'cheering on', 'congratulations to']

result_before_one_word = get_candidates(df2013, 'won', extraction_winner_one_word, True)

awards = ['best actress', 'best actor', 'best director', 'best supporting actress ']
sub2013 = getDfCandidateText(df2013)
def getDfCandidateText(df):
    return df.filter(items = result_before_one_word.index, axis = 0).merge(result_before_one_word, left_index=True, right_index=True).drop(['user','id','timestamp_ms'], axis=1)

def countResult(df, criteria): 
    count = {}
    def countName(name):
        for n in name: 
            if n not in count:
                count[n] = 1
            else:
                count[n]+=1
    np.vectorize(countName)(df[criteria])
    return sorted(count.items(), key = lambda item:item[1], reverse=True)

def resultFindAward(df, criteria):
    award_winner = {}
    def find_award(tweet, names): 
        index = -1
        for award in awards:
            if award in tweet:
                award_winner[award] = names[0]
    np.vectorize(find_award)(df['text'], df[criteria])
    return sorted(award_winner.items(), key = lambda item:item[1], reverse=True)  