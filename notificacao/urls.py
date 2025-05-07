from django.urls import path

from . import views

urlpatterns = [
    #path('admin/notificacao/', views.enviar_notificacoes_admin, name='notificacao-enviar'),
    path('notificacao/visualizar/<int:notificacao_id>/<str:tipo>/', views.visualizar_notificacoes, name='visualizar-notificacao-cliente'),
    path('notificacao/operador/visualizar/<int:notificacao_id>/<str:tipo>/', views.visualizar_notificacoes_operador, name='visualizar-notificacao-operador'),
    path('notificacao/enviar/clientes/<int:notificacao_id>/', views.enviar_notificacoes_clientes, name='enviar-notificacao-cliente'),
    path('notificacao/enviar/operadores/<int:notificacao_id>', views.enviar_notificacoes_operadores, name='enviar-notificacao-operador'),
    ]

