from models.document import TextDocument
from models.indice_invertido import SimpleInvertedIndex, InvertedIndexWithSynonyms
from service.buscador import BuscadorSimple, BuscadorConSinonimo

# Crear documentos
documento1 = TextDocument("La inteligencia artificial está revolucionando muchas industrias.")
documento2 = TextDocument("El aprendizaje automático, un subcampo de la inteligencia artificial, se utiliza en el análisis de datos.")
documento3 = TextDocument("El sinónimo de revolucionando podría ser transformando, dependiendo del contexto.")

# Crear índices
indice_simple = SimpleInvertedIndex()
indice_con_sinonimos = InvertedIndexWithSynonyms()

# Agregar documentos a los índices
indice_simple.agregar_documento(documento1)
indice_simple.agregar_documento(documento2)
indice_simple.agregar_documento(documento3)

indice_con_sinonimos.agregar_documento(documento1)
indice_con_sinonimos.agregar_documento(documento2)
indice_con_sinonimos.agregar_documento(documento3)

# Crear buscadores
buscador_simple = BuscadorSimple(indice_simple)
buscador_con_sinonimos = BuscadorConSinonimo(indice_con_sinonimos)

# Pruebas de búsqueda
print("=== Buscador Simple ===")
buscador_simple.buscar("inteligencia")
buscador_simple.buscar("revolucionando")
buscador_simple.buscar("subcampo")

print("\n=== Buscador con Sinónimos ===")
buscador_con_sinonimos.buscar("inteligencia", incluir_sinonimos=True)
buscador_con_sinonimos.buscar("transformando", incluir_sinonimos=True)
buscador_con_sinonimos.buscar("subcampo", incluir_sinonimos=True)

print("\n=== Índices ===")
print("Índice Simple:", dict(indice_simple.indice))
print("Índice con Sinónimos:", dict(indice_con_sinonimos.indice))
