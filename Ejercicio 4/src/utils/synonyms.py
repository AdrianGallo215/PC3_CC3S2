from nltk.corpus import wordnet

def getSynonyms(phrase):
    synonymsList = wordnet.synonyms(phrase,lang="spa")
    synonyms = [item for sublist in synonymsList for item in sublist]
    return synonyms
