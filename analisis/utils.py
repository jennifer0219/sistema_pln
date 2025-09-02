import re
from collections import Counter
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('spanish'))

def limpiar_texto(contenido):
    """
    Convierte a minúsculas, elimina puntuación y stopwords.
    Retorna lista de tokens limpios.
    """
    contenido = contenido.lower()
    palabras = re.findall(r'\w+', contenido)
    return [p for p in palabras if p not in STOPWORDS]

def generar_ngramos(tokens, n=2):
    """
    Genera n-gramas a partir de tokens.
    """
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def frecuencias_palabras(tokens):
    """
    Calcula frecuencia de palabras.
    """
    return Counter(tokens)

def frecuencias_ngramos(tokens, n=2):
    """
    Calcula frecuencia de n-gramas.
    """
    return Counter(generar_ngramos(tokens, n))
