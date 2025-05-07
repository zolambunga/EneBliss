from django.urls import path
from .import views

urlpatterns = [
    path('historico/listar/', views.lista_historico, name='lista-historico'),
    path('detalhes/<int:historico_id>', views.detalhes, name='detalhes-carregamento'),
]
