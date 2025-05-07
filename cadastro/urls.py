from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
#from .views import ContactoClientes

urlpatterns = [
    path('cadastro/pt/', views.cadastro_pt, name='cadastro-pt'),
    path('cadastro/post/', views.cadastro_post, name='cadastro-post'),
    path('cadastro/cliente/', views.cadastro_usuario, name='cadastro-cliente'),
    path('cadastro/usuario/', views.cadastro_usuario, name='cadastro-usuario'),
    path('cadastro/residencia/<int:user_id>/', views.cadastro_residencia, name='cadastro-residencia'),

    path('editar/pt/<int:pt_id>/', views.editar_pt, name='editar-pt'),
    path('editar/post/<int:post_id>/', views.editar_post, name='editar-post'),
    path('editar/usuario/', views.editar_usuario, name='editar-usuario'),
    #path('editar/perfil/', views.editar_perfis, name='editar-perfis'),
    path('editar/residencia/<int:user_id>/', views.editar_residencia, name='editar-residencia'),

    path('deletar/pt/<int:pt_id>/', views.deletar_pt, name='deletar-pt'),
    path('deletar/post/<int:post_id>/', views.deletar_post, name='deletar-post'),
    path('deletar/usuario/<int:user_id>/', views.deletar_usuario, name='deletar-usuario'),

    path('lista/admin/', views.lista_admin, name='lista-admin'),
    path('lista/operadores/', views.lista_operadores, name='lista-operadores'),
    #path('lista/clientes/', views.lista_clientes, name='lista-clientes'),
    path('lista/clientes/', views.lista_clientes, name='lista-clientes'),
    path('dashboard/', views.lista_usuarios, name='dashboard'),
    path('lista/mensagens/', views.lista_sms, name='lista-sms'),

    path('lista/pt/', views.lista_pt, name='lista-pt'),
    path('lista/post/', views.lista_post, name='lista-post'),
    path('lista/residencia/', views.lista_residencia, name='lista-residencia'),

    path('perfil/consumidor/<int:cliente_id>/', views.operador_ver_perfil_cliente, name='ver-perfil-cliente'),
    #path('Contactos/Clientes', ContactoClientes.as_view(), name='contactos-cliente'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
