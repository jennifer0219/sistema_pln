from django.urls import path
from . import views

urlpatterns = [
    path('subir/', views.subir_texto, name='subir_texto'),
    path('', views.lista_textos, name='lista_textos'),
    path('histograma/<int:texto_id>/', views.histograma, name='histograma'),
    path('ngramas/<int:texto_id>/', views.ngramas, name='ngramas'),
    path('mle/<int:texto_id>/<int:n>/<int:usar_fronteras>/', views.mle_view, name='mle'),
]
