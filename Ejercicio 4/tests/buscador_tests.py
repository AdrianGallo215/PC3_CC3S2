import pytest
from service.buscador import BuscadorConOperadores
from utils.normalizer import normalizar_texto

class MockIndice:
    def __init__(self, indice):
        self._indice = indice

    def get_indice(self):
        return self._indice

@pytest.fixture
def mock_indice():
    indice = {
        'word1': [1, 2, 3],
        'word2': [2, 3, 4],
        'word3': [3, 4, 5],
        'word4': [4, 5, 6]
    }
    return MockIndice(indice)

def test_buscar_and_operator(mock_indice, capsys):
    buscador = BuscadorConOperadores(mock_indice)
    buscador.buscar("word1 and word2")
    captured = capsys.readouterr()
    assert "Documentos encontrados: [2, 3]" in captured.out

def test_buscar_or_operator(mock_indice, capsys):
    buscador = BuscadorConOperadores(mock_indice)
    buscador.buscar("word1 or word2")
    captured = capsys.readouterr()
    assert "Documentos encontrados: [1, 2, 3, 4]" in captured.out

def test_buscar_not_operator(mock_indice, capsys):
    buscador = BuscadorConOperadores(mock_indice)
    buscador.buscar("word1 not word2")
    captured = capsys.readouterr()
    assert "Documentos encontrados: [1]" in captured.out

def test_buscar_xor_operator(mock_indice, capsys):
    buscador = BuscadorConOperadores(mock_indice)
    buscador.buscar("word1 xor word2")
    captured = capsys.readouterr()
    assert "Documentos encontrados: [1, 4]" in captured.out

def test_buscar_no_operator(mock_indice, capsys):
    buscador = BuscadorConOperadores(mock_indice)
    buscador.buscar("word1")
    captured = capsys.readouterr()
    assert "Documentos encontrados: [1, 2, 3]" in captured.out