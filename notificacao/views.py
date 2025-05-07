
'''
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
from cadastro.models import Residencia
from django.contrib.auth.models import User
from .serializers import NotifcacaoSerializer

# Create your views here.

class NotificacaoAPIView(APIView):
    def post(self, request, *args, **kwargs):
        #Recebe os dados da notificação
        data = request.data
        tipo_notificacao = data.get('tipo_notificacao')
        usuario = User.objects.get(id=data['usuario'])

        #Envio de notificação para o cliente via SMS(Twilio) ou Email
        if tipo_notificacao == 'alerta_energia':
            self.enviar_alerta_energia(usuario)
        elif tipo_notificacao == 'comunicacao_erro':
            self.enviar_comunicacao_erro(usuario)
        elif tipo_notificacao == 'nova_recarga':
            self.enviar_nova_recarga(usuario)
        return Response({"message": "Notificação enviada com sucesso!"}, status=status.HTTP_200_OK)

    def enviar_alerta_energia(self, usuario):

        #Envio de SMS via Twilio
        cliente = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        cliente.messages.create(body="Alerta! Sua energia está prestes a acabar.",
                                from_=settings.TWLIO_PHONE_NUMBER, to=usuario.telefone)

        #Envio de E-mail
        send_mail('Alerta de energia', 'Sua energia está prestes a acabar. Por favor recarregue para evitar cortes.',
                  settings.DEFAULT_FROM_EMAIL, [usuario.email], fail_silently=False)

    def enviar_comunicacao_erro(self, usuario):
        #Envio de SMS via Twilio
        cliente = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        cliente.messages.create(body='Há um problema com a sua residencia. Verifique o status de sua energia.',
                                from_=settings.TWILIO_PHONE_NUMBER, to=usuario.telefone)
        #Envio de E-mail

        send_mail('Erro na residencia', 'Há um problema com sua residencis. Por favor, verifique.',
                  settings.DEFAULT_FROM_EMAIL, [usuario.email], fail_silently=False)

    def enviar_nova_recarga(self, usuario):
        #Envio de SMS via Twilio
        cliente = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        cliente.messages.create(body="Recarga conclída com sucesso. Sua energia foi recarregada",
                                from_=settings.TWILIO_PHONE_NUMBER, to=usuario.telefone)

        #Envio de E-Mail
        send_mail('Recarga de energia', 'Sua energia foi recarregada com sucesso',
                  settings.DEFAULT_FROM_EMAIL, [usuario.email], fail_silently=False)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .email_service import send_email
from .twilio_service import send_sms
from cadastro.models import Residencia


class NotificacaoAPIView(APIView):
    def post(self, request):
        tipo = request.data.get("tipo")
        residencia_id = request.data.get("residencia_id")

        try:
            residencia = Residencia.objects.get(id=residencia_id)
            cliente = residencia.usuario
            telefone = cliente.telfone
            email = cliente.email

            if tipo == "cadastro":
                mensagem = "Seu cadastro foi concluído coom sucesso"
            elif tipo == "alerta_energia":
                mensagem = "Alerta: Sua energia está acabando"
            elif tipo == "evento":
                mensagem = "Nova mensagem do sistema para você!"
            elif tipo == "recarga":
                mensagem = "Pagamento confirmado! sua recarga foi processada"
            else:
                return Response({"erro": "tipo de notificação inválido"}, status=status.HTTP_400_BAD_REQUEST)

            send_sms(telefone, mensagem)
            send_email(email, "Notificação do Sistema", mensagem)

            return Response({"status": "Notificação enviada!"}, status=status.HTTP_200_OK)
        except Residencia.DoesNotExist:
            return Response({"erro": "Residencia não encontrada"}, status=status.HTTP_404_NOT_FOUND)



"""
Rota para receber alertas do arduino
"""
class AletaEnergiaAPIView(APIView):
    def post(self, request):
        residencia_id = request.data.get("residencia_id")
        energia_restante = request.data.get("energia_restante")

        if energia_restante < 10: #Alert quando a energia estiver abaixo de 10kwh
            NotificacaoAPIView().post(request)
        return Response({"status": "Alerta recebido"}, status=status.HTTP_200_OK)

'''

from medicao.models import Medicao
from .models import NotificacaoAutonoma, NotificacaoAdmin
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q





def visualizar_notificacoes(request, notificacao_id=None, tipo=None):

    if request.user.groups.filter(name='Cliente').exists():
        usuario = request.user

        # Identificar os grupos relevantes
        grupo_operadores = Group.objects.get(name="Cliente")

        # Operadores so veem notificações
        notificacoes_autonoma = NotificacaoAutonoma.objects.filter(destinatario=usuario).order_by('-data_criacao')
        notificacoes_admin = NotificacaoAdmin.objects.filter(grupo_destinatario=grupo_operadores).order_by('-data_criacao')

        search = request.GET.get('search')
        if search:
            notificacoes_admin = notificacoes_admin.filter(
            Q(titulo__icontains=search) | Q(data_criacao__icontains=search))
            notificacoes_autonoma = notificacoes_autonoma.filter(
            Q(titulo__icontains=search) | Q(data_criacao__icontains=search))

        # Unir ambas as consultas e ordenar pela data
        notificacoes = list(notificacoes_admin) + list(notificacoes_autonoma)
        notificacoes.sort(key=lambda x: x.data_criacao, reverse=True)

        # Verificar qual notificação está sendo visualizada

        notificacao_selecionada = None

        if notificacao_id:
            if tipo == "admin":
                notificacao_selecionada = get_object_or_404(NotificacaoAdmin, id=notificacao_id)
            elif tipo == "sistema":
                notificacao_selecionada = get_object_or_404(NotificacaoAutonoma, id=notificacao_id)


        return render(request, "notificacao/notificacoes.html", {"notificacoes": notificacoes,
                                                                          "notificacao_selecionada": notificacao_selecionada, search:'search'})


#Visualizar e responder mensagem específica
@login_required
def enviar_notificacoes_clientes(request, notificacao_id=None):
    if request.user.groups.filter(name='Admin').exists():

        grupo = Group.objects.get(name='Cliente')

        if request.method == "POST":
            conteudo = request.POST.get('conteudo').strip()

            if conteudo:
                #Identificar o grupo do destinatario

                #Criar a notificação associada ao grupo correto
                notificacao = NotificacaoAdmin.objects.create(remetente=request.user, titulo='Comunicado',
                                                              mensagem=conteudo, grupo_destinatarios=grupo)


                return redirect('enviar-notificacao-cliente', notificacao_id=notificacao.id)

        #todas_notificacoes = NotificacaoAdmin.objects.all().order_by('-data_criacao') # Lista todas as notificações no sistema
        todas_notificacoes = NotificacaoAdmin.objects.filter(grupo_destinatario=grupo).order_by('-data_criacao')

        #Verificar se uma notificação especifica foi selecionada
        notificacao_selecionada = None

        if notificacao_id:
            notificacao_selecionada = get_object_or_404(NotificacaoAdmin, id=notificacao_id)

        return render(request, 'notificacao/enviar_notificacao.html', {'todas_notificacoes': todas_notificacoes,
                                                             'notificacao_selecionada': notificacao_selecionada})




def visualizar_notificacoes_operador(request, notificacao_id=None, tipo=None):

    if request.user.groups.filter(name='Operador').exists():
        usuario = request.user

        #Identificar os grupos relevantes
        grupo_operadores = Group.objects.get(name="Operador")

        # Operadores so veem notificações
        notificacoes_autonoma = NotificacaoAutonoma.objects.filter(destinatario=usuario).order_by('-data_criacao')
        notificacoes_admin = NotificacaoAdmin.objects.filter(grupo_destinatario=grupo_operadores).order_by('-data_criacao')

        search = request.GET.get('search')
        if search:
            notificacoes_admin = notificacoes_admin.filter(Q(titulo__icontains=search) | Q(data_criacao__icontains=search))
            notificacoes_autonoma = notificacoes_autonoma.filter(Q(titulo__icontains=search) | Q(data_criacao__icontains=search))


        #Unir ambas as consultas e ordenar pela data
        notificacoes = list(notificacoes_admin) + list(notificacoes_autonoma)
        notificacoes.sort(key=lambda x: x.data_criacao, reverse=True)

        #Verificar qual notificação está sendo visualizada

        notificacao_selecionada = None

        if notificacao_id:
            if tipo == "admin":
                notificacao_selecionada = get_object_or_404(NotificacaoAdmin, id=notificacao_id)
            elif tipo == "sistema":
                notificacao_selecionada = get_object_or_404(NotificacaoAutonoma, id=notificacao_id)


        return render(request, "notificacao/notificacoes_operador.html", {"notificacoes": notificacoes,
                                                    "notificacao_selecionada": notificacao_selecionada, 'search': search})




#Visualizar e responder mensagem específica
@login_required
def enviar_notificacoes_operadores(request, notificacao_id=None):
    if request.user.groups.filter(name='Admin').exists():

        grupo = Group.objects.get(name='Operador')

        if request.method == "POST":
            conteudo = request.POST.get('conteudo').strip()

            if conteudo:
                # Identificar o grupo do destinatario

                # Criar a notificação associada ao grupo correto
                notificacao = NotificacaoAdmin.objects.create(remetente=request.user, titulo='Comunicado',
                                                              mensagem=conteudo, grupo_destinatario=grupo)

                return redirect('enviar-notificacao-operador', notificacao_id=notificacao.id)

        # todas_notificacoes = NotificacaoAdmin.objects.all().order_by('-data_criacao') # Lista todas as notificações no sistema
        todas_notificacoes = NotificacaoAdmin.objects.filter(grupo_destinatario=grupo).order_by('-data_criacao')

        # Verificar se uma notificação especifica foi selecionada
        notificacao_selecionada = None

        if notificacao_id:
            notificacao_selecionada = get_object_or_404(NotificacaoAdmin, id=notificacao_id)

        return render(request, 'notificacao/enviar_notificacao_operador.html', {'todas_notificacoes': todas_notificacoes,
                                                             'notificacao_selecionada': notificacao_selecionada})


'''
def visualizar_notificacoes_operador(request, notificacao_id=None):
    operador = request.user

    #Lista de notificações
    notificacoes_admin = NotificacaoAdmin.objects.exclude(lida_por=operador).filter(lida_por__groups__name='Operador')  #

    #Unir ambas as consultas e ordenar pela data
    notificacoes = list(notificacoes_admin)
    notificacoes.sort(key=lambda x: x.data_criacao, reverse=True)

    #Verificar qual notificação está sendo visualizada

    notificacao_selecionada = None

    if notificacao_id:
        notificacao_selecionada = get_object_or_404(NotificacaoAdmin, id=notificacao_id)




    return render(request, "notificacao/notificacoes_operador.html", {"notificacoes": notificacoes,
                                                     "notificacao_selecionada": notificacao_selecionada})

'''
