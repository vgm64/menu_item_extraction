from nltk.tokenize import RegexpTokenizer

def GenerateTokenizedRevs(onebizdata):
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
    alltokens = []
    if 'review' in onebizdata:
        for review in onebizdata['review']:
            reviewtxt = review['comment'].replace("\\n"," ")
            tokens = tokenizer.tokenize(reviewtxt)
            alltokens += tokens
    return alltokens
