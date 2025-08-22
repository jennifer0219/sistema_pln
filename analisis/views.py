from django.shortcuts import render, redirect, get_object_or_404
from .forms import TextoAnalizadoForm
from .models import TextoAnalizado
from collections import Counter
import re

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
        contenido = f.read().lower()

    # separar palabras con regex
    palabras = re.findall(r'\w+', contenido)
    contador = Counter(palabras)

    return render(request, 'analisis/histograma.html', {
        'texto': texto,
        'contador': contador.most_common()  # lista de (palabra, frecuencia)
    })
