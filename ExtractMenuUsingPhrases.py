def ExtractMenuItemUsingPrefixPhrases(sentencetokens,phrase):
    len_of_item = 2
    ntokens = len(sentencetokens)
    theitems = []
    for i,token in enumerate(sentencetokens):
            if i+len(phrase)+len_of_item < len(sentencetokens) and phrase == sentencetokens[i:i+len(phrase)]:
                #we found a match for the phrase as a prefix
                theitems.append(sentencetokens[i+len(phrase):i+len(phrase)+len_of_item])
    return theitems

def ExtractMenuItemUsingSuffixPhrases(sentencetokens,phrase):
    len_of_item = 2
    ntokens = len(sentencetokens)
    theitems = []
    for i,token in enumerate(sentencetokens):
            if i-len(phrase) - len_of_item > 0 and phrase == sentencetokens[i-len(phrase):i]:
                #we found a match for the phrase as a suffix
                theitems.append(sentencetokens[i-len(phrase)-len_of_item:i-len(phrase)])
    return theitems
