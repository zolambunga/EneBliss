from django.urls import path
from .import views

urlpatterns = [
    #path('mensagens/listar/', views.listar_mensagens, name='listar-mensagens'),
    path('operadores/listar/', views.lista_operadores_clientes, name='listar-operadores-clientes'),
    path('mensagens/operador/consumidor/<int:cliente_id>/', views.visualizar_responder_mensagem, name='visualizar-responder'),
    path('mensagens/cliente/operador/<int:operador_id>/', views.enviar_visualizar_mensagem, name='enviar-mensagem'),
    #path('mensagens/admin/operador/<int:operador_id>/', views.enviar_visualizar_mensagem, name='enviar-mensagem'),
    path('mensagens/operador/admin/<int:admin_id>/', views.responder_admin, name='responder-admin'),
    path('messagens/<int:mensagem_id>/apagar/', views.apagar_mensagem, name='apagar-mensagem'),

    #path('mensagens/admin/todas/<int:operador_id>/', views.todas_mensagens, name='todas-mnsagens'),

]


