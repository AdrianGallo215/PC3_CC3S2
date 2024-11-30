from utils.normalizer import normalizar_texto

class Buscador():

    def __init__(self, indice):
        self.indice = indice

    def buscar(self, texto:str):
        documentos = []
        for word in normalizar_texto(texto.lower()):
            if word in self.indice:
                documentos.extend(self.indice[word])
        print(f"Documentos encontrados: {list(set(documentos))}")