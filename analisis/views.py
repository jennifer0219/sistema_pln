from django.shortcuts import render, redirect, get_object_or_404
from .models import TextoAnalizado
from .forms import TextoAnalizadoForm
from .utils import limpiar_texto
from collections import Counter

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

    # aplicar limpieza de texto (minúsculas, sin puntuación, sin stopwords)
    palabras = limpiar_texto(contenido)

    # contar frecuencias
    contador = Counter(palabras)

    return render(request, 'analisis/histograma.html', {
        'texto': texto,
        'contador': contador.most_common()  # lista de (palabra, frecuencia)
    })
