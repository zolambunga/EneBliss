from django.urls import path
#from .views import UsuarioLoginView
from .views import custom_login_view, perfil_usuario, sair_sistema
from django.contrib.auth import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    #path('', UsuarioLoginView.as_view(), name='index'),
    path('', custom_login_view, name='index'),
    path('logout/', sair_sistema, name='logout'),
    path('Usuario/', perfil_usuario, name='perfil-usuario'),

    path('Recuperar/Senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('Recuperar/Senha/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('Recuperar/Senha/Confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('Recuperar/Senha/Completo/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')


]
