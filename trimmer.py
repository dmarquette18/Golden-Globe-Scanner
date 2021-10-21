

def CandidateTrimmer(sortCan):
    cnt = 0
    newSort = sortCan.copy()
    for can in sortCan.keys():
        for count in sortCan.keys():
            if can in count and can != count:
                del(newSort[can])
                break
        
    return newSort


def OnlyBest(sortCan):
    cnt = 0
    newSort = sortCan.copy()
    for can in sortCan.keys():
        if "best" not in can:
            del(newSort[can])

        
    return newSort


def ThreeWord(sortCan):
    cnt = 0
    newSort = sortCan.copy()
    for can in sortCan.keys():
        newCan = can.split()
        if len(newCan) <= 2:
            del(newSort[can])

    return newSort

def scoreCalc(totCands):
    award_word_dict = [
        "award",
        "best",
        "performance",
        "picture",
        "tv",
        "television",
        "series",
        "honored",
        "honor",
        "actor",
        "actress",
        "song",
        "motion",
        "movie",
        "screenplay",
        "direct",
        "director",
    ]
    scrDict = dict()
    for can in totCands.keys():
        scrDict[can] = 0
        splt = can.split()
        for word in splt:
            if word in award_word_dict:
                scrDict[can] += 1
    
    return scrDict





