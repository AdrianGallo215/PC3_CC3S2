class Document():

    documentCount = 0

    def __init__(self, contenido = ''):
        self.id = Document.increaseId()
        self.contenido = contenido

    @classmethod
    def increaseId(cls):
        cls.documentCount += 1
        return cls.documentCount
    
    def __str__(self):
        return(f"Documento {self.id}: {self.contenido[:30]}...")

    def read(self):
        print(self.contenido)
    
    def getId(self):
        return self.id