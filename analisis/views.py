from django.shortcuts import render, redirect, get_object_or_404
from .models import TextoAnalizado
from .forms import TextoAnalizadoForm
from .utils import limpiar_texto, frecuencias_palabras, frecuencias_ngramos
from .utils import limpiar_texto_mle, calcular_mle

def limitar_n(n):
    """ Asegura que n esté entre 1 y 3 """
    try:
        n = int(n)
        if n < 1:
            return 1
        elif n > 3:
            return 3
        return n
    except (TypeError, ValueError):
        return 2  

def subir_texto(request):
    if request.method == 'POST':
        form = TextoAnalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_textos')
    else:
        form = TextoAnalizadoForm()
    return render(request, 'analisis/subir.html', {'form': form})

def lista_textos(request):
    textos = TextoAnalizado.objects.all().order_by('-fecha_subida')
    return render(request, 'analisis/lista.html', {'textos': textos})

def histograma(request, texto_id):
    texto = get_object_or_404(TextoAnalizado, id=texto_id)
    with open(texto.archivo.path, "r", encoding="utf-8") as f:
        contenido = f.read()

    tokens = limpiar_texto(contenido)
    contador = frecuencias_palabras(tokens)

    return render(request, 'analisis/histograma.html', {
        'texto': texto,
        'contador': contador.most_common()
    })

def ngramas(request, texto_id):
    texto = get_object_or_404(TextoAnalizado, id=texto_id)
    with open(texto.archivo.path, "r", encoding="utf-8") as f:
        contenido = f.read()

    tokens = limpiar_texto(contenido)

    n = request.GET.get('n')
    try:
        n = int(n)
        if n < 1:
            n = 1
    except (TypeError, ValueError):
        n = 2

    contador = frecuencias_ngramos(tokens, n)

    return render(request, 'analisis/ngramas.html', {
        'texto': texto,
        'contador': contador.most_common(),
        'n': n
    })

def mle_view(request, texto_id, n=2, usar_fronteras=0):
    texto = get_object_or_404(TextoAnalizado, id=texto_id)
    with open(texto.archivo.path, "r", encoding="utf-8") as f:
        contenido = f.read()
    n_get = request.GET.get('n')
    if n_get:
        try:
            n = int(n_get)
            if n < 1:
                n = 1
        except ValueError:
            pass

    uf_get = request.GET.get('usar_fronteras')
    if uf_get is not None:
        try:
            usar_fronteras = int(uf_get)
        except ValueError:
            pass

    tokens = limpiar_texto_mle(contenido)  

    resultados = calcular_mle(tokens, n=n, usar_fronteras=bool(usar_fronteras))

    return render(request, 'analisis/mle.html', {
        'texto': texto,
        'resultados': resultados,
        'tokens': tokens,
        'n': n,
        'usar_fronteras': usar_fronteras,
    })

def autocompletar(request, texto_id, n=2, usar_fronteras=0):
    texto = get_object_or_404(TextoAnalizado, id=texto_id)
    with open(texto.archivo.path, "r", encoding="utf-8") as f:
        contenido = f.read()

    n_get = request.GET.get('n')
    if n_get:
        try:
            n = int(n_get)
            if n < 1:
                n = 1
        except ValueError:
            pass

    uf_get = request.GET.get('usar_fronteras')
    if uf_get is not None:
        try:
            usar_fronteras = int(uf_get)
        except ValueError:
            pass

    from .utils import obtener_tokens
    tokens = obtener_tokens(contenido, usar_fronteras=bool(usar_fronteras))

    ngramas = [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

    if request.method == "POST":
        entrada = request.POST.get("entrada", "").lower().split()
        sugerencias = []

        if entrada:
            contexto = tuple(entrada[-(n-1):]) if n > 1 else tuple()
            candidatos = [ng for ng in ngramas if ng[:-1] == contexto]

            while not candidatos and len(contexto) > 0:
                contexto = contexto[1:] 
                candidatos = [ng for ng in ngramas if ng[:-1] == contexto]

            from collections import Counter
            contador = Counter([c[-1] for c in candidatos])
            total = sum(contador.values())
            if total > 0:
                sugerencias = [(pal, cnt/total) for pal, cnt in contador.items()]
                sugerencias = sorted(sugerencias, key=lambda x: x[1], reverse=True)[:3]

        return render(request, "analisis/autocompletar.html", {
            "texto": texto,
            "entrada": request.POST.get("entrada",""),
            "sugerencias": sugerencias,
            "n": n,
            "usar_fronteras": usar_fronteras,
        })

    return render(request, "analisis/autocompletar.html", {
        "texto": texto,
        "entrada": "",
        "sugerencias": [],
        "n": n,
        "usar_fronteras": usar_fronteras,
    })
