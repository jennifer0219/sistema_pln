from django.shortcuts import render, redirect, get_object_or_404
from .models import TextoAnalizado
from .forms import TextoAnalizadoForm
from .utils import limpiar_texto, frecuencias_palabras, frecuencias_ngramos
from .utils import limpiar_texto_mle, calcular_mle
from .utils import obtener_tokens

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
            n = 2
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

    tokens = obtener_tokens(contenido, usar_fronteras=bool(usar_fronteras))
    resultados = calcular_mle(tokens, n=n, usar_fronteras=bool(usar_fronteras))

    return render(request, 'analisis/mle.html', {
        'texto': texto,
        'resultados': resultados,
        'tokens': tokens,  
        'n': n,
        'usar_fronteras': usar_fronteras,
    })
