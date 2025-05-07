from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


'''
request (requisição) quando uma solicitaçao é enviado do cliente ao servidor,
o servidor recebe a requisição, processa os dados conforme as regras da API e
geralmente reliza uma ação(como consultar ou alterar dados no banco de dados)
Após processar a solicitação, a API envia uma resposta de volta para o cliente
que fez a requisição (no formato JSON ou XML)
'''

'''
Sobrescrevendo o método LoginView.as_view usado na urls para tratar do login, ou seja,
Estamos criando uma subclassificação da LoginView para personalisar o comportamento
'''
'''
class UsuarioLoginView(LoginView):
    #O template onde o formulario de login está renderizado
    template_name = 'usuario/login.html'
'''
'''
    Esse método é chamado quando o login é bem sucedido. Nele verificamos uma
    em qual grupo o usuario está e redirecionamos para a URL apropriada de acordo
    com o grupo

    def get_success_url(self):
        user = self.request.user

        #Verificar os grupos do usuário para redireciona-lo para o painel correto
        if user.groups.filter(name='Admin').exists():
            # Redireciona para o Painel Admin
            return reverse('painel-admin')
        elif user.groups.filter(name='Operador').exists():
            # Redireciona para o Painel Operador
            return reverse('painel-operador')
        elif user.groups.filter(name='Cliente').exists():
            # Redireciona para o Painel Cliente
            return reverse('painel-cliente')
            # é usada para gerar a URL de uma vista a partir do nome da URL e os parametros
            #que vista precisa. Usa-se quando se precisa gerar uma URL dentro do codigo
        else:
            #Caso não tenha acesso redireciona para atela de login
            return reverse('login')
'''

def custom_login_view(request):
    if request.method == 'POST':
        #Obtem os dados do formulario

        username = request.POST.get('username')
        password = request.POST.get('password')

        #Tenta autenticar o usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #Se a autenticação for bem sucedida, faz o login do usuario
            login(request, user)

            # Verifica o grupo do usuario e direciona ao seu painel
            if user.groups.filter(name='Admin').exists():
                return redirect('painel-admin')
            elif user.groups.filter(name='Operador').exists():
                return redirect('painel-operador')
            elif user.groups.filter(name='Cliente').exists():
                return redirect('painel-cliente')
            #else:
                #return redirect('index')
        else:
            return render(request, 'usuario/login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'usuario/login.html')


@login_required
def sair_sistema(request):
    '''
        Logout do usuario e marca como offline
    '''
    if request.user.is_authenticated:
        request.user.online = False #Marca como offline ao sair

        request.user.save()
        logout(request) #Executa o logout padrão do django
        return redirect('index')


@login_required
def perfil_usuario(request):
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists():
        usuario_logado = request.user

        return render(request, 'usuario/perfil_usuario.html', {'usuario': usuario_logado})
    return redirect('index')


