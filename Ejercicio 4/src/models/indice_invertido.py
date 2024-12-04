from collections import defaultdict
from models.document import TextDocument
from utils.normalizer import normalizar_texto
from utils.synonyms import getSynonyms
from abc import ABC, abstractmethod

class IndexInterface(ABC):

    @abstractmethod
    def agregar_documento(self, documento):
        pass

    @abstractmethod
    def get_indice(self):
        pass

class SimpleInvertedIndex(IndexInterface):

    def __init__(self):
        self.indice = defaultdict(list)


    def agregar_documento(self, documento: TextDocument):
        for word in normalizar_texto(documento.contenido.lower()):
            if documento.getId() not in self.indice[word]:
                self.indice[word].append(documento.getId())

    def get_indice(self):
        return self.indice

class InvertedIndexWithSynonyms(IndexInterface):

    def __init__(self):
        self.indice = defaultdict(list)
        self.synonyms = defaultdict(list)

    def agregar_documento(self, documento):
        for word in normalizar_texto(documento.contenido.lower()):
            if documento.getId() not in self.indice[word]:
                self.indice[word].append(documento.getId())

    def get_synonyms(self, word):
        if word not in self.synonyms:
            self.synonyms[word] = getSynonyms(word)
        return self.synonyms[word]
    
    def get_indice(self):
        return self.indice