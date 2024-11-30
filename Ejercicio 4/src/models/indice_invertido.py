from collections import defaultdict
from models.document import Document
from utils.normalizer import normalizar_texto

class IndiceInvertido():

    def __init__(self):
        self.indice = defaultdict(list)


    def agregar_documento(self, documento: Document):
        for word in normalizar_texto(documento.contenido.lower()):
            if documento.getId() not in self.indice[word]:
                self.indice[word].append(documento.getId())
            
