from VoteSystem import sortVote
def commonality(candidates):
    basic_words = ["was", "an", "or", "a", "the", "more", 'to', "for", "golden", "globe", 's"', "in", "that", "you", "ever", "as", "be", "i", "at", "ben", "with", "and", "but", "&amp;", "is", "of", "those", "he", "she", "rt", "have", "all", "we", "so", "it", "on", "by", "les", "dress", "dressed", "this", "her"]
    wordVote = {}
    for can in candidates:
        can = can.split()
        for word in can:
            if word in basic_words:
                continue
            if word not in wordVote:
                wordVote[word] = 1
            else:
                wordVote[word] += 1
    
    sortWordVote = sortVote(wordVote)

    return sortWordVote



