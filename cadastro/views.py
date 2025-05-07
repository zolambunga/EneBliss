from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from .forms import (PTFormCreate, PostFormCreate, ResidenciaFormCreate, AdminFormCreateUsuario,
                    OperadorFormCreateCliente, UsuarioFormUpdate, ClienteFormUpdate)
from .models import PT, Post, Residencia
from notificacao.models import NotificacaoAutonoma
from medicao.models import Medicao
from django.contrib.auth.models import User, Group
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q #Para realizar a busca




'''
request (requisição ou pedido) quando uma solicitaçao é enviado do cliente ao servidor,
o servidor recebe a requisição, processa os dados conforme as regras da API e
geralmente reliza uma ação(como consultar ou alterar dados no banco de dados)
Após processar a solicitação, a API envia uma resposta de volta para o cliente
que fez a requisição (no formato JSON ou XML)
'''


##############################################Cadastros##################################################
'''
Views para cadastros de PT(Post de Transformação)
'''
@login_required
def cadastro_pt(request):
    # Verificar se o usuário logado é admin
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists():
        if request.method == 'POST':
            pt_form = PTFormCreate(request.POST)
            if pt_form.is_valid():
                user = pt_form.save()
                return redirect('sucesso-pagina')
        else:
            pt_form = PTFormCreate()

        return render(request, 'cadastro/cadastrar_pt.html', {'pt_form': pt_form})
    else:
        return redirect('index')


'''
Views para cadastros de Posts
'''
@login_required #impede que os usuarios não autenticados acessem a sua pagina
def cadastro_post(request):
    # Verificar se o usuário logado é admin
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists():
        if request.method == 'POST':
            post_form = PostFormCreate(request.POST)
            if post_form.is_valid():
                user = post_form.save()  # cria usuario
                return redirect('sucesso-pagina')
        else:
            post_form = PostFormCreate()
        return render(request, 'cadastro/cadastrar_post.html', {'post_form': post_form})
    else:
        #redirect é usado para redirecionar o usuario para outra URL(pagina)
        return redirect('index')


'''
Views para cadastros de usuarios associados a uma residencia se forem adicionados o grupo cliente
'''


@login_required# Para garantir que  operação seja feita por um usuario logado
# Para garantir que o usuario logado tenha a permissão necessaeria
def cadastro_usuario(request):
    # Verificar se o usuário logado é admin
    if request.user.groups.filter(name='Admin').exists():
        usuario = request.user
        # Verifica se o metodo da requisição é POST(significa que o formulario foi enviado)
        if request.method == 'POST':
            # cria uma instancia do formulario AdminFormCreate com os dados enviados no POST
            usuario_form = AdminFormCreateUsuario(request.POST)
            if usuario_form.is_valid():#verifica se o formulario é válido
                usuario = usuario_form.save()
                NotificacaoAutonoma.objects.create(destinatario=usuario, titulo='Cadastro', mensagem=f'Seja Bem Vindo Ao nosso Sistema. Foste cadastrado com sucesso')

                    
                    # O id do usuario é normalmente uma chave primaria automatica no django
                    #(gerada pelo banco de dados).Cada usuario tem um valor unico de id
                return redirect('sucesso-pagina')
        else:
            usuario_form = AdminFormCreateUsuario()
        return render(request, 'cadastro/cadastrar_usuario.html', {'usuario_form': usuario_form,  "modo": "cadastro"})

    # Verificar se o usuário logado é Operador
    elif request.user.groups.filter(name='Operador').exists():
        # Verifica se o metodo da requisição é POST(significa que o formulario foi enviado)
        if request.method == 'POST':
            # cria uma instancia do formulario OperadorFormCreate com os dados enviados no POST
            cliente_form = OperadorFormCreateCliente(request.POST, request.FILES)
            if cliente_form.is_valid():
                usuario = cliente_form.save()
                # O id é passado como parametro da URL ao redirecionar para outra pagina
                return redirect('cadastro-residencia', user_id=usuario.id)
        else:
            cliente_form = OperadorFormCreateCliente()
        return render(request, 'cadastro/cadastrar_cliente.html', {'cliente_form': cliente_form})
    else:
        return redirect('index')


'''
Views para cadastros de Residencias caso algum usuario for adionado no grupo cliente
'''
@login_required
def cadastro_residencia(request, user_id):

    # Verificar se o usuário logado é Operador
    if request.user.groups.filter(name='Operador').exists():
        '''
            get_object_or_404(Model->que se deseja consultar): é uma função do django usada para 
            recuperar um objecto do banco de dados com base em um riterio especifico, Se o objecto não
            for encontrado ele levanta automaticamente um erro Http404
        '''
        user = get_object_or_404(User, id=user_id)

        # Verifica se o metodo da requisição é POST(significa que o formulario foi enviado)
        if request.method == 'POST':
            # Passa a instancia do usuario para o formulário
            # #cria uma instancia do formulario ResidenciaFormCreate com os dados enviados no POST

            residencia_form = ResidenciaFormCreate(request.POST)

            if residencia_form.is_valid():
                # criamos uma instancia do modelo Residencia, mas não salvamos ainda(commit=False)
                # pois queremos associa-la ao usuario
                residencia = residencia_form.save(commit=False)
                residencia.usuario = user
                residencia.save()
                Medicao.objects.create(residencia=residencia, energia_consumida_kwh=0.0, energia_restante_kwh=0.0,
                                       energia_comprada_kwh=0.0, energia_consumida_kzs=0.0, energia_restante_kzs=0.0,
                                       energia_comprada_kzs=0.0, status=False)

                #Enviando notificacao para o usuario cadastrado
                NotificacaoAutonoma.objects.create(destinatario=user, titulo='Cadastro', mensagem=f'Seja Bem Vindo Ao nosso Sistema. Foste acdastrado com sucesso')

                # Redireciona para a página de lista de usuarios
                return redirect('sucesso-pagina')
        else:
            residencia_form = ResidenciaFormCreate()
        return render(request, 'cadastro/cadastrar_residencia.html', {'residencia_form': residencia_form})
    else:
        return redirect('index')






###########################################Editar Cadastros###########################################

##########Views para Editar PTs##########
def editar_pt(request, pt_id):
    pt = get_object_or_404(PT, id=pt_id)
    # Verificar se o usuário logado é adminou operador
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists():
        if request.method == 'POST':
            # Passa a instancia do usuario para o formulário
            pt_form = PTFormCreate(request.POST, instance=pt)
            if pt_form.is_valid():
                pt = pt_form.save()
                # Redireciona para a página de lista de usuarios
                if request.user.groups.filter(name='Admin').exists():
                    return redirect('painel-admin')
                else:
                    return redirect('painel-operador')
        else:
            # Cria o formulario com os dados do usuario para ediçao
            pt_form = PTFormCreate(instance=pt)
        return render(request, 'cadastro/cadastrar_pt.html', {'pt_form': pt_form, 'pt': pt})
    else:
        return redirect('index')


#####Views edição de cadastros de Posts#######
def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Verificar se o usuário logado é adminou operador
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists():
        if request.method == 'POST':
            # Passa a instancia do usuario para o formulário
            post_form = PostFormCreate(request.POST, instance=post)
            if post_form.is_valid():
                post_form = post_form.save()
                # Redireciona para a página de lista de usuarios
                if request.user.groups.filter(name='Admin').exists():
                    return redirect('painel-admin')
                else:
                    return redirect('painel-operador')
        else:
            # Cria o formulario com os dados do usuario para ediçao
            post_form = PostFormCreate(instance=post)
        return render(request, 'cadastro/cadastrar_post.html', {'post_form': post_form, 'post': post})
    else:
        return redirect('index')

#####Views edição de cadastros de usuarios#######
@login_required
def editar_usuario(request):
    # Verificar se o usuário logado é cliente
    if request.user.groups.filter(name='Cliente').exists():
        usuario = request.user  # get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            cliente_form = ClienteFormUpdate(request.POST, request.FILES, instance=usuario)
            if cliente_form.is_valid():
                user = cliente_form.save(commit=False)
                if cliente_form.cleaned_data['password1']:
                    #Só atualiza a senha se o usuario preencheu o campo
                    user.set_password(cliente_form.cleaned_data['password1'])
                    update_session_auth_hash(request, user) # Mantém o usuario logado
                #return redirect('cadastro-residencia', user_id=usuario.id)
                user.save()
                return redirect('painel-cliente')
        else:
            # Cria o formulario com os dados do usuario para ediçao
            cliente_form = ClienteFormUpdate(instance=usuario)
        return render(request, 'cadastro/cadastrar_cliente.html', {'cliente_form': cliente_form})

    elif request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists():
        usuario = request.user  # get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            usuario_form = UsuarioFormUpdate(request.POST, request.FILES, instance=usuario)
            if usuario_form.is_valid():
                user = usuario_form.save(commit=False)
                if usuario_form.cleaned_data['password1']:
                    # Só atualiza a senha se o usuario preencheu o campo
                    user.set_password(usuario_form.cleaned_data['password1'])
                    update_session_auth_hash(request, user)  # Mantém o usuario logado
                user.save()
                if request.user.groups.filter(name='Admin').exists():
                    return redirect('painel-admin')
                else:
                    return redirect('painel-operador')
        else:
            # Cria o formulario com os dados do usuario para ediçao
            usuario_form = UsuarioFormUpdate(instance=usuario)

        return render(request, 'cadastro/cadastrar_usuario.html', {'usuario_form': usuario_form, "modo": "edicao"})


####Views para editar cadastros de Residencias caso algum usuario for adicionado no grupo cliente
'''
    A função cadastro_residencia recebe o request e o user_id da URL.
    Ela utiliza o user_id para buscar um usuario especifico no banco
    de dados usando o modelo User
    Depois de obter o usuario ele e assoiado a residencia
'''
@login_required
def editar_residencia(request, user_id):
    # Verificar se o usuário logado é admin
    if request.user.groups.filter(name='Operador').exists():
        # Obtem o usuario e a residencia associada ao usuario
        usuario = get_object_or_404(User, id=user_id)
        #Aqui buscamos a residencia associada ao usuario usando a relação entre as tabelas
        #Residencia e User
        residencia = get_object_or_404(Residencia, usuario=usuario)
        #Verifica se o metodo da requisição é POST(significa que o formulario foi enviado)
        if request.method == 'POST':
            #Passando a instancia de residencia para o formulario faz com que o formulario
            #seja preenchido com os dados existentes
            residencia_form = ResidenciaFormCreate(request.POST, instance=residencia)
            if residencia_form.is_valid():
                residencia = residencia_form.save()
                # Redireciona para a página de lista de usuarios
                return redirect('painel-operador')
        else:
            #Se não for Post, exibe o formulario com os dados existentes
            residencia_form = ResidenciaFormCreate(instance=residencia)
        return render(request, 'cadastro/cadastrar_residencia.html', {'residencia_form': residencia_form})
    else:
        return redirect('index')







###########################################Eliminar Cadastros###########################################

##########Views para Eliminar PTs##########
def deletar_pt(request, pt_id):
    #pt_delete = get_object_or_404(PT, id=pt_id)
    form = get_object_or_404(PT, id=pt_id)
    # Verificar se o usuário logado é adminou operador
    if request.user.groups.filter(name='Admin').exists():
        if request.method == 'POST':
            # Eliminar PT
            #pt_delete.delete()
            form.delete()
            # Redireciona para a página de lista de usuarios
            return redirect('painel-admin')
        return render(request, 'cadastro/form3.html', {'form': form})#,'pt_delete': pt_delete})

    elif request.user.groups.filter(name='Operador').exists():
        if request.method == 'POST':
            # Eliminar PT
            #pt_delete.delete()
            form.delete()
            # Redireciona para a página de lista de usuarios
            return redirect('painel-operador')
        return render(request, 'cadastro/form3.html', {'form': form})#'pt_delete': pt_delete})
    else:
        return redirect('login')

#####Views deletar de cadastros de Posts#######
def deletar_post(request, post_id):
    #post_delete = get_object_or_404(PT, id=post_id)
    form = get_object_or_404(PT, id=post_id)
    # Verificar se o usuário logado é admin
    if request.user.groups.filter(name='Admin').exists():
        if request.method == 'POST':
            # Eliminar Post
            #post_delete.delete()
            form.delete()
            # Redireciona para a página de lista de usuarios
            return redirect('painel-admin')
        return render(request, 'cadastro/form3.html', {'form': form})#'post_delete': post_delete})
    elif request.user.groups.filter(name='Operador').exists():
        if request.method == 'POST':
            # Eliminar Post
            #post_delete.delete()
            form.delete()
            # Redireciona para a página de lista de usuarios
            return redirect('painel-operador')
        return render(request, 'cadastro/form3.html', {'form': form})#'post_delete': post_delete})
    else:
        return redirect('login')

#####Views edição de cadastros de usuarios#######
def deletar_usuario(request, user_id):
    usuario_delete = get_object_or_404(User, id=user_id)
    # Verificar se o usuário logado é admin
    if request.user.groups.filter(name='Admin').exists():
        if request.method == 'POST':
            #Verificar se o usuario aa ser eliminado e do grupo cliente
            usuario_delete.delete()
            return redirect('painel-admin')

        return render(request, 'cadastro/form.html', {'usuario_delete': usuario_delete})

    # Verificar se o usuário logado é Operador
    elif request.user.groups.filter(name='Operador').exists():
        if usuario_delete.groups.filter(name='Cliente').exists():
            if request.method == 'POST':
                usuario_delete.delete()
                return redirect('painel-operador')
            return render(request, 'cadastro/form.html', {'usuario_delete': usuario_delete})
        return HttpResponseForbidden('Não existe')
    else:
        return redirect('index')


'''
@login_required
def deletar_residencia(request, user_id):
    # Verificar se o usuário logado é admin
    if request.user.groups.filter(name='Admin').exists():
        # Obtem o usuario e a residencia associada ao usuario
        usuario = get_object_or_404(User, id=user_id)
        #Associa a residencia ao usuario
        residencia = get_object_or_404(Residencia, usuario=usuario)
        if request.method == 'POST':
           residencia.delete()# Deleta a residencia
            return redirect('painel-admin')
        
        return render(request, 'cadastro/form2.html', {'residencia_form': residencia_form})

    # Verificar se o usuário logado é Operador
    elif request.user.groups.filter(name='Operador').exists():
        usuario = get_object_or_404(User, id=user_id)
        residencia = get_object_or_404(Residencia, usuario=usuario)
        if request.method == 'POST':
            residencia.delete()#deleta a residencia associada ao usuario
            return redirect('painel-operador')
        return render(request, 'cadastro/form2.html', {'residencia_form': residencia_form})
    else:
        return redirect('login')





def eliminar_usuario(request, user_id):
    # Verificar se o usuário logado é admin
    if request.user.groups.filter(name='Admin').exists():
        user = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            user.delete()
            # Redireciona para a lista dos usuarios
            return redirect('user_lista')

        return render(request, 'usuario/confirmar_elimin.html', {'user': user})
    else:
        return HttpResponseForbidden("Voce não tem permissão para acessar essa página")
'''

###########################################Lista Usuarios###########################################

####Listar Clientes####
@login_required
def lista_clientes(request):
    # Verifica se o usuario e admin ou operador
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists():

        # Filtra os usuarios que pertencem ao grupo Cliente
        clientes = User.objects.filter(groups__name='Cliente')


        #Pesquisa
        #No django request.GET é usado para capturar dados via o método Get da requisição HTTP
        #O metodo GET é usado para enviar dadoa através da URL, como parametro de consultas
        search = request.GET.get('search')# .get é usado para acessar um valoe especifico do
        #dicionario. Ele retorna o valor assoicado a chave fornecida(search), caso não exista,
        #o metodo retorna o valor None ou um valor padrão

        if search:
            #Pesquisa Por nome de usuario ou email ou telefone
            clientes = clientes.filter(
                #Estamos criando uma consulta no query que é uma requisição feita a um banco de
                #dados com o objectivo de obter, modificar ou excluir dados
                #Q de Query, se o usuario passar algum valor no query a pesquisa sera feita nos
                #campos pré determinados
                Q(username__icontains=search) | Q(email__icontains=search) | Q(telefone__icontains=search)
            )
        return render(request, 'cadastro/listas/contactos_cliente.html', {'clientes': clientes,
                                                            'search': search})
    else:
        return redirect('index')

####Listar Operadores####
@login_required
def lista_operadores(request):
    # Verifica se o usuario e admin
    if request.user.groups.filter(name='Admin').exists():
        # Filtra os usuarios que pertencem ao grupo Operador
        operadores = User.objects.filter(groups__name='Operador')

        # Pesquisa
        search = request.GET.get('search')

        if search:
            # Pesquisa Por nome de usuario, email ou telefone
            operadores = operadores.filter(
                Q(username__icontains=search) | Q(email__icontains=search) | Q(telefone__icontains=search)
            )
        return render(request, 'cadastro/listas/tabela_operador.html', {'operadores': operadores,
                                                                    'search': search})
    else:
        #return redirect('index')
        return HttpResponseForbidden('Erro Só Admin')


@login_required
def lista_usuarios(request):
    # Verifica se o usuario e admin
    if request.user.groups.filter(name='Admin').exists():
        # Filtra os usuarios que pertencem ao grupo Operador
        operadores = User.objects.filter(groups__name='Operador')

        # Pesquisa
        search = request.GET.get('search')

        if search:
            # Pesquisa Por nome de usuario, email ou telefone
            operadores = operadores.filter(
                Q(username__icontains=search) | Q(email__icontains=search) | Q(telefone__icontains=search)
            )
        return render(request, 'paginas/admin/dashboard.html', {'operadores': operadores,
                                                                    'search': search})
    else:
        #return redirect('index')
        return HttpResponseForbidden('Erro Só Admin')


@login_required
def lista_sms(request):
    # Verifica se o usuario e admin
    if request.user.groups.filter(name='Admin').exists():
        # Filtra os usuarios que pertencem ao grupo Operador
        operadores = User.objects.filter(groups__name='Operador')

        # Pesquisa
        search = request.GET.get('search')

        if search:
            # Pesquisa Por nome de usuario, email ou telefone
            operadores = operadores.filter(
                Q(username__icontains=search) | Q(email__icontains=search) | Q(telefone__icontains=search)
            )
        return render(request, 'chat/visualizar_mensagem.html', {'operadores': operadores,
                                                                    'search': search})
    else:
        #return redirect('index')
        return HttpResponseForbidden('Erro Só Admin')





def lista_admin(request):
    # Verifica se o usuario e admin
    if request.user.groups.filter(name='Admin').exists():
        # Filtra os usuarios que pertencem ao grupo Operador
        admin = User.objects.filter(groups__name='Admin')

        # Pesquisa
        search = request.GET.get('search')

        if search:
            # Pesquisa Por nome de usuario, email ou telefone
            admin = admin.filter(
                Q(username__icontains=search) | Q(email__icontains=search) | Q(telefone__icontains=search)
            )
        return render(request, 'cadastro/listas/tabela_admin.html', {'admin': admin,
                                                                    'search': search})
    else:
        #return redirect('index')
        return HttpResponseForbidden('Erro Só Admin')


###########################################Listas de PTS, POST e Residencia###########################################

####Listar Clientes####
@login_required
def lista_pt(request):
    # Verifica se o usuario e admin ou operador
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists():

        # Filtra os Post de Transformação (PT)
        pts = PT.objects.all()

        #Pesquisa
        search = request.GET.get('search')

        if search:
            #Pesquisa Por nome, bairro, numero, municipio ou data
            pts = pts.filter(
                Q(nome_pt__icontains=search) | Q(numero_pt__icontains=search) | Q(municipio_pt__icontains=search)|
                Q(bairro_pt__icontains=search) | Q(data_pt__icontains=search)
            )
        return render(request, 'cadastro/listas/tabela_pt.html', {'pts': pts,
                                                            'search': search})
    else:
        #return redirect('index')
        return HttpResponseForbidden('Erro Só Admin ou Operador')

####Listar Operadores####
@login_required
def lista_post(request):
    # Verifica se o usuario e admin
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists():
        # Filtra os Post
        posts = Post.objects.all()

        # Pesquisa
        search = request.GET.get('search')

        if search:
            # Pesquisa Por pt, numero_post, rua_post, data_post
            posts = posts.filter(
                Q(pt__icontains=search) | Q(numero_post__icontains=search) | Q(rua_post__icontains=search)|
                Q(data_post__icontains=search)
            )
        return render(request, 'cadastro/listas/tabela_post.html', {'posts': posts,
                                                                    'search': search})
    else:
        #return redirect('index')
        return HttpResponseForbidden('Erro Só Admin e Operador')


def lista_residencia(request):
    # Verifica se o usuario e admin
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists():
        # Filtra os usuarios que pertencem ao grupo Operador
        residencias = Residencia.objects.all()

        # Pesquisa
        search = request.GET.get('search')

        if search:
            # Pesquisa Por nome de usuario, numero_residenica, nome_proprietario, endereço
            residencias = residencias.filter(
                Q(numero_residencia__icontains=search) | Q(nome_proprietario__icontains=search) |
                Q(endereco_residencia__icontains=search)
            )
        return render(request, 'cadastro/listas/tabela_residencia.html', {'residencias': residencias, 'search': search})
    else:
        #return redirect('index')
        return HttpResponseForbidden('Erro Só Admin')




def operador_ver_perfil_cliente(request, cliente_id=None):
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Operador').exists():

        if cliente_id:
            usuario = get_object_or_404(User, id=cliente_id, groups__name='Cliente')

            if hasattr(usuario, "residencia") and hasattr(usuario.residencia, "medicao"):
                medicao = usuario.residencia.medicao.latest('data_hora')  # acesso direto
                #residencia = cliente_id.residencia
                dados_medicao = {
                    "energia_consumida_kwh": medicao.energia_consumida_kwh,
                    "energia_restante_kwh": medicao.energia_restante_kwh,
                    "energia_comprada_kwh": medicao.energia_comprada_kwh
                }
            else:
                dados_medicao = None  # caso o usuario nao tenha medicao associada

            return render(request, 'paginas/cliente/cliente_dashboard.html', {'usuario': usuario,
                                                                              "medicao": dados_medicao})
    return redirect('index')
    # return HttpResponseForbidden('Você Não Tem Permissão Para Acessar o Painel Cliente')











