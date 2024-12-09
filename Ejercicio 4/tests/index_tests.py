import pytest
from collections import defaultdict
from models.document import TextDocument
from utils.normalizer import normalizar_texto
from utils.synonyms import getSynonyms
from models.indice_invertido import InvertedIndexWithSynonyms

class MockTextDocument(TextDocument):
    def __init__(self, id, contenido):
        self.id = id
        self.contenido = contenido

    def getId(self):
        return self.id

@pytest.fixture
def inverted_index():
    return InvertedIndexWithSynonyms()

def test_agregar_documento(inverted_index):
    doc1 = MockTextDocument(1, "Hola mundo")
    doc2 = MockTextDocument(2, "Hola a todos")

    inverted_index.agregar_documento(doc1)
    inverted_index.agregar_documento(doc2)

    indice = inverted_index.get_indice()
    assert indice['hola'] == [1, 2]
    assert indice['mundo'] == [1]
    assert indice['a'] == [2]
    assert indice['todos'] == [2]

def test_get_synonyms(inverted_index, mocker):
    mocker.patch('utils.synonyms.getSynonyms', return_value=['saludo', 'saludos'])
    synonyms = inverted_index.get_synonyms('hola')
    assert synonyms == ['saludo', 'saludos']

def test_get_indice(inverted_index):
    doc1 = MockTextDocument(1, "Hola mundo")
    inverted_index.agregar_documento(doc1)
    indice = inverted_index.get_indice()
    assert isinstance(indice, defaultdict)
    assert indice['hola'] == [1]
    assert indice['mundo'] == [1]