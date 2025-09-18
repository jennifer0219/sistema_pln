import re
from collections import Counter
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('spanish'))

def limpiar_texto(contenido):
    """
    Convierte a minúsculas, elimina puntuación y stopwords.
    Retorna lista de tokens limpios.
    """
    from nltk.corpus import stopwords
    STOPWORDS = set(stopwords.words('spanish'))
    
    contenido = contenido.lower()
    palabras = re.findall(r'\w+', contenido)
    return [p for p in palabras if p not in STOPWORDS]

def limpiar_texto_mle(contenido):
    """
    Convierte a minúsculas, mantiene puntuación como tokens separados.
    Retorna lista de tokens limpia para MLE.
    """
    contenido = contenido.lower()
    tokens = re.findall(r'\w+|[.,!?;]', contenido)
    return tokens

def obtener_tokens(contenido, usar_fronteras=False):
    """
    Devuelve la lista de tokens para un texto.
    """
    tokens = limpiar_texto_mle(contenido)
    if usar_fronteras:
        tokens = ["<s>"] + tokens + ["</s>"]
    return tokens

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
from collections import Counter

def calcular_mle(tokens, n=2, usar_fronteras=False):
    if usar_fronteras:
        tokens = ["<s>"] + tokens + ["</s>"]

    ngramas = [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]  

    contador_ngramos = Counter(ngramas)  
    contextos = Counter([ng[:-1] for ng in ngramas])

    resultados = []
    for ngrama, freq in contador_ngramos.items():
        contexto = ngrama[:-1]
        prob = freq / contextos[contexto]
        resultados.append((" ".join(ngrama), freq, prob))

    return resultados


