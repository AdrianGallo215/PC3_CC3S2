import pytest
from utils.normalizer import normalizar_texto

def test_normalizar_texto():
    texto = "Hola, este es un texto de prueba para la normalización."
    resultado_esperado = ['Hola', 'texto', 'prueba', 'normalización']
    assert normalizar_texto(texto) == resultado_esperado

def test_normalizar_texto_con_stopwords():
    texto = "Este es un ejemplo con muchas palabras vacías."
    resultado_esperado = ['ejemplo', 'muchas', 'palabras', 'vacías']
    assert normalizar_texto(texto) == resultado_esperado

def test_normalizar_texto_con_puntuacion():
    texto = "¡Hola! ¿Cómo estás? Esto es una prueba."
    resultado_esperado = ['Hola', 'Cómo', 'prueba']
    assert normalizar_texto(texto) == resultado_esperado

def test_normalizar_texto_vacio():
    texto = ""
    resultado_esperado = []
    assert normalizar_texto(texto) == resultado_esperado

def test_normalizar_texto_solo_stopwords():
    texto = "y de la el en"
    resultado_esperado = []
    assert normalizar_texto(texto) == resultado_esperado