from django.contrib import admin

# adicionar include para importar urls dos apps
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('paginas.urls')),
    path('', include('usuario.urls')),
    path('', include('cadastro.urls')),
    path('', include('notificacao.urls')),
    path('', include('pagamento.urls')),
    path('', include('chat.urls')),
    path('', include('historico.urls')),
    path('', include('medicao.urls')),
]
