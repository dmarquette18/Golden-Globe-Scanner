
from typing import ItemsView
from VoteSystem import sortVote
from fuzzywuzzy import fuzz



def FiveWord(sortCan):
    cnt = 0
    newSort = sortCan.copy()
    for can in sortCan.keys():
        newCan = can.split()
        if len(newCan) >= 5:
            del(newSort[can])

    return newSort

def endRemove(sortCan):
    removables = ["an", "the", "at", "for", "or", "is", "and", "s", "golden", "globe", "to"]
    newSort = sortCan.copy()
    for can in sortCan.keys():
        word = can.split()
        for w in word:
            if w in removables and can in newSort:
                del(newSort[can])
                continue
    return newSort

def unifySpaces(sortCan):
    newSort = {}
    for can in sortCan.keys():
        tempCan = can
        can = " ".join(can.split())
        newSort[can] = sortCan[tempCan]
    
    return newSort

def trimToBest(sortCan):
    newSort = dict()
    for can in sortCan:
        temp = can.split()
        if "best" in temp:
        
            ind = temp.index("best")
            temp = temp[ind:]
            temp = " ".join(temp)
            newSort[temp] = sortCan[can]

        elif len(temp) > 0 and temp[len(temp)-1] == "television":
            temp.append("series")
            temp = " ".join(temp)
            newSort[temp] = sortCan[can]
        
        else:
            temp = " ".join(temp)
            newSort[temp] = sortCan[can]

    return newSort

def fatTrimmer(sortCan):
    newSort = dict()
    for can in sortCan:
        trueWord = can
        temp = can.split()
        for i, word in enumerate(temp):
            if "http" in word or "#" in word or "for" in word or "is" in word or '"' in word or "with" in word:
                trueWord = " ".join(temp[:i])
                break
        newSort[trueWord] = sortCan[can]

    return newSort

def removePunct(sortCan):
    punct = ['"', ".", ",", "-"]
    newSort = dict()
    for can in sortCan:
        trueWord = can
        temp = can.split()
        for i, word in enumerate(temp):
            for punctation in punct:
                if punctation in word:
                    word.replace(punctation, "")
                trueWord = word
                break
        newSort[trueWord] = sortCan[can]

    return newSort



def unifySimilar(sortCan):
    newSort = sortCan.copy()
    for can in sortCan.keys():
        if "in a" not in can and " in " in can:
            ind = can.index("in")
            part1 = can[:ind+1]
            part2 = can[ind+1:]
            newpart = part1 + " a" + part2
            " ".join(newpart.split())
            newSort[newpart] = newSort[can]
            del(newSort[can])

    return newSort

def purgeSame(sortedKeys):
    filtered = dict()
    finalDict = dict()
    sortList = reversed(sortedKeys)
    found = False
    for item in sortList:
        found = False
        store = item
        item = item.split()
        newItem =[]
        for i in item:
            if i == "in" or i == "a" or i == "series":
                continue
            else:
                newItem.append(i)
        newItem = sorted(newItem)
        item = " ".join(newItem)
        for curr in filtered.keys():
            if item == curr:
                found = True
                break
        if not found:
            filtered[item] = store
        
    
    for newKeys in filtered.keys():
        call = filtered[newKeys]
        finalDict[call] = sortedKeys[call]
    return finalDict

def nipNames(sortedDict):
    filtered = dict()
    finalDict = dict()
    sortList = sortedDict
    for item in sortList:
        found = False
        store = item
        for curr in filtered.keys():
            if curr in item or item in curr:
                found = True
        if not found:
            filtered[item] = sortedDict[item]
    return filtered



    

def purgeSimilar(sortedKeys):
    filtered = dict()
    finalDict = dict()
    sortList = reversed(sortedKeys)
    for item in sortList:
        store = item
        item = item.split()
        newItem =[]
        for i in item:
            i.replace(" ", "")
            if i == "in" or i == "a" or i == "series":
                continue
            else:
                newItem.append(i)
        newItem = sorted(newItem)
        max = 0
        temp = False
        for i, curr in enumerate(filtered.keys()):
            curr = curr.split()
            diff = []
            for i in curr:
                if i not in newItem:
                    diff.append(i)
            if len(diff) >= 1 and len(diff) <=3:
                del()


                
            #if fuzz.ratio(item, curr) >= 95:
            #    temp = True             
            #    if len(curr) < len(item):
            #        #print("New Word: " + str(item) +" Word it's Replacing: " + str(curr) + " RATIO: " + str(fuzz.ratio(item, curr)))
            #        del(filtered[curr])
            #        filtered[item] = store
            #        temp = True
            #        break

            
        if not temp:
            filtered[item] = store
        temp = False


    for newKeys in filtered.keys():
        call = filtered[newKeys]
        finalDict[call] = sortedKeys[call]
    return finalDict    

        
        






