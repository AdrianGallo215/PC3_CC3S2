from collections import defaultdict
from models.document import TextDocument
from utils.normalizer import normalizar_texto
from abc import ABC, abstractmethod

class IndexInterface(ABC):

    @abstractmethod
    def agregar_documento(self, documento):
        pass

class SimpleInvertedIndex(IndexInterface):

    def __init__(self):
        self.indice = defaultdict(list)


    def agregar_documento(self, documento: TextDocument):
        for word in normalizar_texto(documento.contenido.lower()):
            if documento.getId() not in self.indice[word]:
                self.indice[word].append(documento.getId())

class InvertedIndexWithSynonyms(IndexInterface):

    def __init__(self):
        self.indice = defaultdict(list)

    def agregar_documento(self, documento):
        return super().agregar_documento(documento)
            
