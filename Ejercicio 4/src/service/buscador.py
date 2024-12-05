from utils.normalizer import normalizar_texto
from abc import ABC, abstractmethod

class BuscadorInterface(ABC):

    @abstractmethod
    def buscar(self, contenido):
        pass

class BuscadorSimple(BuscadorInterface):

    def __init__(self, indice):
        self.indice = indice.indice

    def buscar(self, contenido:str):
        documentos = []
        for word in normalizar_texto(contenido.lower()):
            if word in self.indice:
                documentos.extend(self.indice[word])
        print(f"Documentos encontrados: {list(set(documentos))}")

class BuscadorConSinonimo(BuscadorInterface):

    def __init__(self, indice):
        self.indice = indice.get_indice()
        self.get_synonyms = indice.get_synonyms


    def buscar(self, contenido, incluir_sinonimos = True):
        documentos = []
        for word in normalizar_texto(contenido.lower()):
            if word in self.indice:
                documentos.extend(self.indice[word])
            if incluir_sinonimos:
                for syn in self.get_synonyms(word):
                    documentos.extend(self.indice[syn])
        print(f"Documentos encontrados: {list(set(documentos))}")

class BuscadorConOperadores(BuscadorInterface):

    def __init__(self, indice):
        self.indice = indice.get_indice()
