from typing import final


def canGather(ind, tweet, forward, totalAwards):
    award_word_dict = [
        "award",
        "best",
        "performance",
        "picture",
        "tv",
        "television",
        "series",
        "supporting",
        "honored",
        "honor",
        "actor",
        "actress",
        "song",
        "motion",
        "movie",
        "musical",
        "drama",
        "comedy",
        "mini-series",
        "miniseries",
        "film",
        "screenplay",
        "direct",
        "director",
    ]
    basic_word_dict = ["a", "an", "for", "in", "by", "or", "-", ":", ",", " - "]
    trans = ["in", "an", "or", "a", "motion", "television", "-"]
    stop = ["#", ":"]
    awardcand = totalAwards
    can = []
    if forward:
        totString = tweet[ind:]
        cntr = 0
        for i in range(len(totString)):
            if totString[i] == ":":
                continue
            if totString[i] == "tv":
                totString[i] = "television"
            if totString[i] not in award_word_dict and totString[i] not in basic_word_dict:
                cntr += 1
                can.append(totString[i])
            elif totString[i] in award_word_dict or totString[i] in basic_word_dict:
                can.append(totString[i])
            if cntr > 2:
                break
        while can[-1] in basic_word_dict or can[-1] not in award_word_dict:
                can.pop()
        
                        


        finalAward = " ".join(can)
        finalAward.replace(",", "")
        if len(can) > 3 and can not in totalAwards:
            totalAwards.append(finalAward)

    

    return totalAwards