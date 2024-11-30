from models.document import Document
from service.buscador import Buscador
from models.indice_invertido import IndiceInvertido

documento = Document("La transformación digital está redefiniendo las dinámicas de las organizaciones modernas, desde la automatización de procesos operativos hasta la implementación de inteligencia artificial para la toma de decisiones. Las empresas que no adopten estas tecnologías corren el riesgo de quedarse obsoletas en un mercado globalizado y altamente competitivo. En este contexto, términos como 'Big Data', 'Machine Learning' y 'Blockchain' se han convertido en elementos imprescindibles para optimizar la eficiencia y la productividad. Sin embargo, la digitalización no solo implica la incorporación de herramientas tecnológicas, sino también un cambio cultural profundo que requiere la capacitación constante del talento humano. Este fenómeno, conocido como 'reskilling', se presenta como el pilar fundamental para garantizar la adaptabilidad y el éxito de las organizaciones en un entorno disruptivo y en constante evolución.")
documento.__str__()
documento2 = Document("Desde los albores de la civilización, el ser humano ha buscado dar respuesta a los misterios del universo a través de la filosofía y la ciencia. Mientras que la filosofía plantea preguntas fundamentales acerca de la existencia, la verdad y el conocimiento, la ciencia busca respuestas a través de la observación, la experimentación y la formulación de leyes. Un claro ejemplo de esta intersección es el debate sobre el determinismo, que cuestiona si los eventos están predestinados por leyes universales o si existe el libre albedrío. En la actualidad, disciplinas como la física cuántica han puesto en jaque las nociones clásicas de causalidad, sugiriendo que el azar puede desempeñar un papel crucial en la estructura del cosmos. Este diálogo entre filosofía y ciencia continúa enriqueciendo nuestra comprensión del mundo, desafiando los límites de lo conocido y abriendo nuevas fronteras para la exploración intelectual.")
documento2.__str__()
indice = IndiceInvertido()

indice.agregar_documento(documento)
indice.agregar_documento(documento2)

buscador = Buscador(indice.indice)

buscador.buscar("determinismo")

print(f"\nIndices: {indice.indice}")