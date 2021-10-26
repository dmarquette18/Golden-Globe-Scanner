from typing import final


def canGather(ind, tweet, type):
    basic_word_dict = ["-", ":", ",", " - "]
    trans = ["in", "an", "or", "a", "motion", "television", "-"]
    stop = ["#", ":", "@", ]
    can = []

    if type == "forward":

        totString = tweet[(ind+1):]
        cntr = 0
        daStr = ""
        for i in range(len(totString)):
            if totString[i] == "goes":
                break
            if totString[i] == "tv":
                totString[i] = "television"
            daStr = daStr + " " + str(totString[i])
            while daStr[-1] in basic_word_dict:
                daStr = daStr[:-1]
            can.append(daStr)
    elif type == "best":
        can.append(str(tweet[ind:]))
        totString = tweet[ind:]
        cntr = 0
        daStr = ""
        for i in range(len(totString)):
            if totString[i] == "goes":
                break
            if totString[i] == "tv":
                totString[i] = "television"
            daStr = daStr + " " + str(totString[i])
            while daStr[-1] in basic_word_dict:
                daStr = daStr[:-1]
            can.append(daStr)
    elif type == "goes":
        can = []
        totString = tweet[:ind]
        daStr = ""
        for i in range(len(totString)):
            if totString[i] == "tv":
                totString[i] = "television"
            daStr = daStr + " " + str(totString[i])
            while daStr[-1] in basic_word_dict:
                daStr = daStr[:-1]
            can.append(daStr)
    

    

    return can