
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MensagemForm
from .models import Mensagem
from django.db.models import Q, Max




# Create your views here.
#Recebidas pelo cliente


@login_required
def lista_operadores_clientes(request):
    # Verifica se o usuario e admin
    if request.user.groups.filter(name='Cliente').exists():
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
        return redirect('index')
        #return HttpResponseForbidden('Erro Só Admin')




#Visualizar e responder mensagem específica
@login_required
def enviar_visualizar_mensagem(request, operador_id=None):
    if request.user.groups.filter(name='Cliente').exists() or request.user.groups.filter(name='Operador').exists() or request.user.groups.filter(name='Admin').exists():
        operadores = User.objects.filter(groups__name='Operador')#, status_disponivel=True, municipio=request.user.municipio

        # Pesquisa
        search = request.GET.get('search')

        if search:
            # Pesquisa Por nome de usuario, email ou telefone
            operadores = operadores.filter(
                Q(id__icontains=search)
            )

        # Se nenhum operador for selecionado
        mensagens = None

        if operador_id:
            operador = get_object_or_404(User, id=operador_id, groups__name='Operador')#status_disponivel=True

            mensagens = Mensagem.objects.filter(
                remetente__in=[operador, request.user],
                destinatario__in=[operador, request.user],
                status__in=["enviada", "recebida", "visualizada"]
            ).order_by('data_envio')

            for i in mensagens:
                if i.remetente.id != request.user.id:
                    i.status = "visualizada"
                    i.save()

            #mensagens.update(status="enviada")



            # Enviar Mensagem se o formulario for submetido

            if request.method == "POST":
                conteudo = request.POST.get('conteudo')
                if conteudo:
                    Mensagem.objects.create(
                        remetente=request.user,
                        destinatario=operador,
                        conteudo=conteudo,
                        #status="enviada"
                    )



                return redirect('enviar-mensagem', operador_id=operador.id)

        return render(request, 'chat/enviar_mensagem.html', {'mensagens': mensagens,
                                                             'operadores': operadores, 'search': search})





@login_required
def visualizar_responder_mensagem(request, cliente_id=None):

    if request.user.groups.filter(name='Operador').exists():

        #Operador logado
        operador = request.user

        #lista de clientes com quem o operador já conversou
        #clientes = User.objects.filter(mensagens_enviadas__destinatario=operador).distinct()
        clientes = User.objects.filter(groups__name="Cliente")

        #  Adiciona a mensagem enviada por admin na lista de mensagens

        for cliente in clientes:
            ultima_mensagem = Mensagem.objects.filter(
                remetente=cliente,
                destinatario=operador,
            ).order_by('-data_envio').first()
            if ultima_mensagem:
                cliente.ultima_mensagem = ultima_mensagem.conteudo# if ultima_mensagem else "Nenhuma mensagem"

        #  Adiciona a mensagem enviada por cliente na lista_operadores_clientes
        '''

        for cliente in clientes:
            ultima_mensagem = Mensagem.objects.filter(
                remetente=cliente,
                destinatario=operador,
            ).order_by('-data_envio').first()
           # cliente.ultima_mensagem.update(status="visualizada")
            cliente.ultima_mensagem = ultima_mensagem.conteudo if ultima_mensagem else "Nenhuma mensagem"
        '''


        #carregar mensagem com o cliente especifico
        mensagens = None

        if cliente_id:
            cliente = get_object_or_404(User, id=cliente_id)
            mensagens = Mensagem.objects.filter(
                remetente__in=[operador, cliente],
                destinatario__in=[operador, cliente],
                status__in=["enviada", "recebida", "visualizada"]
            ).order_by('data_envio')

            for i in mensagens:
                if i.remetente.id != request.user.id:
                    i.status = "visualizada"
                    i.save()


            #Se o operdor enviar uma mensagem ela ser+a registada
            if request.method == "POST":
                conteudo = request.POST.get('conteudo')

                if conteudo:
                    Mensagem.objects.create(
                        remetente=request.user,
                        destinatario=cliente,
                        conteudo=conteudo,
                    )

                    #.__class__.objects.filter(id=Mensagem.objects.latest("id").id).update(status="recebida" if cliente.online else "enviada"))

                    #status = 'recebida' if cliente.online else 'enviada' # Atualizar o Status para mensagem recebida se o destinatario estiver online


                return redirect("visualizar-responder", cliente_id=cliente.id)

        return render(request, 'chat/visualizar_responder.html', {'clientes': clientes,
                                                                       'mensagens': mensagens})






@login_required
def responder_admin(request, admin_id=None):
    if request.user.groups.filter(name='Operador').exists():

        # Operador logado
        operador = request.user

        # lista de Admin com quem o operador já conversou
        #admin = User.objects.filter(mensagens_enviadas__destinatario=operador).distinct()
        admin = User.objects.filter(groups__name="Admin")

        #  Adiciona a mensagem enviada por admin na lista de mensagens

        for ad in admin:
            ultima_mensagem = Mensagem.objects.filter(
                remetente=ad,
                destinatario=operador,
            ).order_by('-data_envio').first()
            ad.ultima_mensagem = ultima_mensagem.conteudo if ultima_mensagem else "Nenhuma mensagem"

        # carregar mensagem com o cliente especifico
        mensagens = None

        if admin_id:
            ad = get_object_or_404(User, id=admin_id)
            mensagens = Mensagem.objects.filter(
                remetente__in=[operador, ad],
                destinatario__in=[operador, ad],
                status__in=["enviada", "recebida", "visualizada"]
            ).order_by('data_envio')

            for i in mensagens:
                if i.remetente.id != request.user.id:
                    i.status = "visualizada"
                    i.save()

            # Se o operdor enviar uma mensagem ela ser+a registada
            if request.method == "POST":
                conteudo = request.POST.get('conteudo')
                Mensagem.objects.create(
                    remetente=request.user,
                    destinatario=ad,
                    conteudo=conteudo,
                )

                return redirect("responder-admin", admin_id=ad.id)

        return render(request, 'chat/responder_admin.html', {'admin': admin,
                                                                  'mensagens': mensagens})



#Cliente apaaga as mensagens
@login_required
def apagar_mensagem(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, id=mensagem_id, remetente=request.user)
    mensagem.delete()
    return redirect('enviar-visualizar-mensagem')


###################################Mensagens Gerais##################################################


###################################Mensagens Do Operador###############################################



###################################Mensagens Do Administrador##############################################

