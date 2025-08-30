import re
from collections import Counter
from nltk.corpus import stopwords

# lista de stopwords en español
STOPWORDS = set(stopwords.words('spanish'))

def limpiar_texto(contenido):
    # convertir a minúsculas
    contenido = contenido.lower()

    # eliminar puntuación (solo letras y números)
    palabras = re.findall(r'\w+', contenido)

    # quitar stopwords
    palabras_limpias = [p for p in palabras if p not in STOPWORDS]

    return palabras_limpias
