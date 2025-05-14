from django.urls import path, include
from . import views
from .views import SucessoPagina, ErroPagina

urlpatterns = [
    path('painel_admin/', views.admin_dashboard, name='painel-admin'),
    path('painel_operador/', views.operador_dashboard, name='painel-operador'),
    path('painel_cliente/', views.cliente_dashboard, name='painel-cliente'),
    path('sucesso/', SucessoPagina.as_view(), name='sucesso-pagina'),
    path('erro/', ErroPagina.as_view(), name='erro-pagina'),
    path('api/', include('api.urls')),
]

