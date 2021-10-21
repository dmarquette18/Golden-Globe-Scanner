from trimmer import CandidateTrimmer, OnlyBest, ThreeWord

def voteCounter(rawCand):
    candidates = dict()
    for curr in rawCand:
        #print(curr)
        if curr in candidates:
            candidates[curr] += 1
        else:
            candidates[curr] = 1
    
    return sortVote(candidates)
    #print(candidates)


def sortVote(candidates):
    sorted_cans = sorted(candidates.items(), key = lambda kv: kv[1])
    sorted_cans = dict(sorted_cans)


    return sorted_cans
    


