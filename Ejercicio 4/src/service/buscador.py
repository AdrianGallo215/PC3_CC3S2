from utils.normalizer import normalizar_texto
from abc import ABC, abstractmethod

class BuscadorInterface(ABC):

    @abstractmethod
    def buscar(self, contenido):
        pass

class Buscador(BuscadorInterface):

    def __init__(self, indice):
        self.indice = indice

    def buscar(self, contenido:str):
        documentos = []
        for word in normalizar_texto(contenido.lower()):
            if word in self.indice:
                documentos.extend(self.indice[word])
        print(f"Documentos encontrados: {list(set(documentos))}")