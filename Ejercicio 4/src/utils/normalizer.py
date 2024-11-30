import nltk
from nltk.corpus import stopwords
import string
def normalizar_texto(texto):

    stopWords = set(stopwords.words('spanish'))

    tokens = nltk.word_tokenize(texto, 'spanish')
 
    tokens = [token for token in tokens if token.lower() not in stopWords]
    tokens = [token for token in tokens if token not in string.punctuation]
    return tokens