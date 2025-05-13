from django.urls import path
from . import views

urlpatterns = [
    path('pagamento/meu/', views.pagamento_view, name='pagamento'),
    #path('pagamento/realizar/meu pagamento/<str:valor_energia_kzs>/', views.realizar_pagamento_para_mim, name='realizar-pagamento-para-mim'),
    #path('pagamento/confirmar_para_mim/<str:valor_energia_kzs>/', views.confirmar_pagamento_para_mim, name='confirmar-pagamento-para_mim'),
    #path('pagamento/outro/', views.iniciar_outro_pagamento, name='iniciar-outro-pagamento'),
    #path('pagamento/outro/realizar/<int:destinatario_id>/<str:valor_energia_kzs>/', views.realizar_pagamento_para_outro, name='realizar-outro-pagamento'),
    #path('pagamento/outro/confirmar/<int:destinatario_id>/<str:valor_energia_kzs>/', views.confirmar_pagamento_outros, name='confirmar-outro-pagamento'),
    #path('pagamento/transferencia/iniciar/', views.transferir_energia, name='transferir-energia'),
    #path('pagamento/transferencia/realizar/<int:destinatario_id>/<str:valor_energia_kzs>/', views.realizar_transferencia, name='realizar-transferencia'),
    path('pagamento/concluido/', views.pagamento_concluido, name='pagamento-concluido')
]
