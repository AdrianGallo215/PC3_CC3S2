from abc import ABC, abstractmethod

class DocumentInterface(ABC):

    @abstractmethod
    def getId(self):
        pass

    @abstractmethod
    def get_content(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

class TextDocument(DocumentInterface):

    documentCount = 0

    def __init__(self, contenido = ''):
        self.id = TextDocument.increaseId()
        self.contenido = contenido

    @classmethod
    def increaseId(cls):
        cls.documentCount += 1
        return cls.documentCount
    
    def __str__(self):
        return(f"Documento {self.id}: {self.contenido[:30]}...")

    def get_content(self):
        return self.contenido
    
    def getId(self):
        return self.id