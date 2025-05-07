'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from cadastro.models import Residencia
#from notificacao.views import enviar_notificacoes_admin
from paypalrestsdk import Payment
from django.conf import settings
from historico.models import HistoricoEnergia
#from notificacao.models import NotificacaoAutonoma
from django.http import JsonResponse
import requests

# Create your views here.


# Tarifa fixa 1kwh custa 100kzs
TARIFA_KWH = 100
def iniciar_pagamento(request):
   
    #Inicia um pagamento paypal
  

    valor_energia_kzs = float(request.POST.get('valor_energia_kzs', 0))

    #Verifica se o valor et´s acima do preco minimo

    if valor_energia_kzs < settings.ENERGIA_PRECO_MINIMO:
        return JsonResponse({"erro": f"Pagamento minimo é {settings.ENERGIA_PRECO_MINIMO}Kzs"}, status=400)

    # Calcula a quantidade de kwh
    quantidade_kwh = valor_energia_kzs / TARIFA_KWH
    
    #criar pagamento

    pagamento = Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {"total": f"{valor_energia_kzs:.2f}", "currency": settings.PAYPAL_CURRENCY},
            "description": f"Compra de {valor_energia_kzs} kwh de energia"
        }],
        "redirect_urls": {"return_url": "http://localhost:8000/pagamento-sucesso/",
                          "cancel_url": "http://localhost:8000/pagamento.cancelado"}
    })
    if pagamento.create():
        for link in pagamento.links:
            if link.rel == "approval_url":
                return redirect(link.href)
        return JsonResponse({"erro": "Erro ao criar pagamento"}, status=500)
'''

'''
#########################################################################
# Tarifa fixa 1kwh custa 100kzs
TARIFA_KWH = 100

def iniciar_pagamento_para_mim(request):

    if request.method == "POST":
        valor_energia_kzs = float(request.POST.get("valor_energia_kzs"))

        #Validacao do preço
        if valor_energia_kzs < settings.ENERGIA_PRECO_MINIMO:
            #return JsonResponse({"erro": f"Pagamento minimo é {settings.ENERGIA_PRECO_MINIMO}Kzs"}, status=400)
            return render(request, "paginas/erro.html", {"mensagem": f"Valor minimo para pagamento: {settings.ENERGIA_PRECO_MINIMO}Kzs"})

        # Renderização da pagina de confirmação
        return render(request, "pagamento/confirmar_meu_pagamento.html", {"cliente": request.user, "valor_energia_kzs": valor_energia_kzs})
    return render(request, "pagamento/iniciar_meu_pagamento.html")



def realizar_pagamento_para_mim(request, valor_energia_kzs):

    valor_energia_kzs = float(valor_energia_kzs)

    cliente_logado = request.user.residencia

    # criar pagamento no paypal

    pagamento = Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {"total": f"{valor_energia_kzs:.2f}", "currency": settings.PAYPAL_CURRENCY},
            "description": f"Compra de {valor_energia_kzs} kwh de energia"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:8000/pagamento/confirmar_para_mim/",
            "cancel_url": "http://localhost:8000/pagamento_cancelado"
        }
    })
    if pagamento.create():
        for link in pagamento.links:
            if link.rel == "approval_url":
                return redirect(link.href)
            return render(request, "paginas/erro.html",
                          {"mensagem": "Erro ao criar pagamento no Paypal"})


#Depois que o pagamento for confirmado, o sistema envia o sinal ao Esp32 do cliente logado

def confirmar_pagamento_para_mim(request, valor_energia_kzs):
    valor_energia_kzs = float(valor_energia_kzs)
    pagamento_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")
    cliente_logado = request.user

    quantidade_kwh = valor_energia_kzs / TARIFA_KWH

    # confirmar pagamento no Paypal

    pagamento = Payment.find(pagamento_id)

    if pagamento.execute({"payer_id": payer_id}):

        try:
            # Enviar o sinal ao Esp32 dos clientes
            url_esp32 = "http//esp32-responsavel/atualizar-energia"
            dados = {
                "cliente_id": cliente_logado.usuario.id,
                    "quantidade_kzs": valor_energia_kzs
            }
            resposta = request.post(url_esp32, json=dados)

            # Verfica se uma requisição HTTP foi bem-sucedida
            if resposta.status_code == 200:
                # Registrar o pagamento no historico
                (HistoricoEnergia.objects.create(usuario=request.user, tipo_transacao="COMPRA",
                                                 quantidade_kwh=quantidade_kwh, valor_energia_kzs=valor_energia_kzs))
                 # Enviar Notificação ao cliente
                #NotificacaoAutonoma.objects.create(remitente=request.user, titulo='Pagamento Confirmado',
                                           #mensagem=f'pagamento confirmado: {valor_energia_kzs}kzs = {quantidade_kwh}kwh')

        except request.exceptions.RequestException as e:
            return render(request, "paginas/erro.html",
                          {"mensagem": f"Erro na comunicação com o dispositivo Esp32: {str(e)}"})

    return render(request, "paginas/erro.html", {"mensagem": "Falha ao confirmar pagamento no Paypal"})
###########################################################

#O cliente logado insere o identificador do destinatario e o valor da recarga
def iniciar_outro_pagamento(request):

    #processar o pagamento se for POST

    if request.method == "POST":

        # Inicia um pagamento paypal

        destinatario_id = request.POST.get("destinatario_id")
        valor_energia_kzs = float(request.POST.get('valor_energia_kzs', 0))



        # Verifica se o valor inserido está acima do preco minimo

        if valor_energia_kzs > settings.ENERGIA_PRECO_MINIMO:
            return render(request, "paginas/erro.html",
                          {"mensagem": f'Valor minimo para o pagamento é: {settings.ENERGIA_PRECO_MINIMO}'})

        # Verificar se o destinatario existe:
        destinatario = get_object_or_404(Residencia, usuario_id=destinatario_id)

        if destinatario:
            #Exibir a pagina de confirmação do pagamento com os dados do destinatario
            return render(request, "pagamento/confirmar_outro_pagamento.html",
                      {"destinatario": destinatario, "valor_energia_kzs": valor_energia_kzs})

    return render(request, "pagamento/iniciar_outro_pagamento.html")

'''
'''
#Após a confirmação dos dados, o pagamento é criado no Paypsl
def realizar_pagamento_para_outro(request, destinatario_id, valor_energia_kzs):
    valor_energia_kzs = float(valor_energia_kzs)
    destinatario = get_object_or_404(Residencia, usuario_id=destinatario_id)

    # criar pagamento no paypal sandbox

    pagamento = Payment(
        {
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [
                {
                    "amount": {
                                "total": f"{valor_energia_kzs:.2f}", "currency": settings.PAYPAL_CURRENCY
                            },
                    "description": f"Recarga de {valor_energia_kzs}kzs para {destinatario.usuario.username}"
                }
            ],
             "redirect_urls":
                {
                    "return_url": f"http://localhost:8000/pagamento/confirmar/{destinatario_id}/{valor_energia_kzs}",
                    "cancel_url": "http://localhost:8000/pagamento/cancelado"
                }
        }
    )
    if pagamento.create():
        for link in pagamento.links:
            if link.rel == "approval_url":
                return redirect(link.href)
            return render(request, "paginas/erro.html", {"mensagem": "Erro ao criar pagamento no paypal."})


#Após o pagamento confirmado os dados são enviados ao Esp32 de ambos clientes
def confirmar_pagamento_outros(request, destinatario_id, valor_energia_kzs):
    valor_energia_kzs = float(valor_energia_kzs)
    pagamento_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")
    destinatario = get_object_or_404(Residencia, usuario_id=destinatario_id)

    quantidade_kwh = valor_energia_kzs / TARIFA_KWH

    # confirmar pagamento no Paypal

    pagamento = Payment.find(pagamento_id)

    if pagamento.execute({"payer_id": payer_id}):

        try:
            # Enviar o sinal ao Esp32 dos clientes
            url_esp32 = "http://esp32-responsavel/atualizar-energia"
            dados = {
                    "destinatario_id": destinatario_id,
                    "quantidade_kzs": valor_energia_kzs
            }
            resposta = request.post(url_esp32, json=dados)

            # Verfica se uma requisição HTTP foi bem-sucedida
            if resposta.status_code == 200:
                # Registrar o pagamento no historico
                (HistoricoEnergia.objects.create(usuario=request.user, tipo_transacao="COMPRA",
                                        quantidade_kwh=quantidade_kwh, valor_energia_kzs=valor_energia_kzs))
                # Enviar Notificação ao cliente
                #NotificacaoAutonoma.objects.create(destinatario=request.user, titulo='Outros Pagamento Confirmado',
                                        #mensagem=f'pagamento confirmado: {valor_energia_kzs}kzs = {quantidade_kwh}kwh')
                #NotificacaoAutonoma.objects.create(destinatario=destinatario_id, titulo='Pagamento Confirmado',
                                        #mensagem=f'pagamento confirmado: {valor_energia_kzs}kzs = {quantidade_kwh}kwh vindo de {request.user.usename}')
                return render(request, "paginas/sucesso.html", {"destinatario": destinatario,
                                                                "valor_energia_kzs": valor_energia_kzs})

        except request.exceptions.RequestException as e:
            return render(request, "paginas/erro.html",
                {"mensagem": f"Erro na comunicação com o dispositivo Esp32: {str(e)}"})

    return render(request, "paginas/erro.html", {"mensagem": "Falha ao confirmar pagamento no Paypal"})
###########################################################


#################################################################3


def transferir_energia(request):

    if request.method == 'POST':

        #tipo_transferencia = request.POST.get("tipo_transferencia")# kzs ou kwh
        destinatario_id = request.POST.get("destinatario_id")
        valor_energia_kzs = float(request.POST.get("valor_energia_kzs"))

        #quantidade = float(request.POST.get("quantidade"))
        remetente = request.user.residencia.medicao

        # Verificar o saldo da conta
        if valor_energia_kzs > (remetente.energia_restante_kwh * TARIFA_KWH):
            return render(request, "paginas/erro.html", {"mensagem": "saldo insuficiente para transferencia"})


        # Verificar se o destinatario existe
        if destinatario_id:
            destinatario = get_object_or_404(User, id=destinatario_id, groups__name='Cliente')

            if hasattr(destinatario, "residencia"):

                destinatario_residencia = destinatario.residencia

                #renderzar para a pgina de confirmação
                return render(request, "pagamento/confirmar_transferencia.html",
                      {"destinatario": destinatario_residencia,
                       "valor_energia_kzs": valor_energia_kzs})

    return render(request, "pagamento/iniciar_transferencia.html")
'''

'''
def realizar_transferencia(request, destinatario_id, valor_energia_kzs):
    valor_energia_kzs = float(valor_energia_kzs)

    remetente = request.user.residencia.medicao

    destinatario = get_object_or_404(User, id=destinatario_id, groups__name='Cliente')

    if hasattr(destinatario, "residencia"):
        destinatario_residencia = destinatario.residencia.id

        #destinatario_medicao = destinatario_residencia.medicao

        quantidade_kwh = valor_energia_kzs / TARIFA_KWH


        #Enviar sinal ao Esp32

        try:
            # Enviar o sinal ao Esp32 dos clientes
            url_esp32 = "http://esp32-responsavel/transferencia-energia"
            dados = {
                "remetente_id": remetente.residencia.id,
                "destinatario_id": destinatario_residencia.id,
                "quantidade_kzs": valor_energia_kzs
            }
            resposta = request.post(url_esp32, json=dados)

            # Verfica se uma requisição HTTP foi bem-sucedida
            if resposta.status_code == 200:
                # Registrar o pagamento no historico
                (HistoricoEnergia.objects.create(usuario=request.user, tipo_transacao="COMPRA",
                                             quantidade_kwh=quantidade_kwh,
                                             valor_energia_kzs=valor_energia_kzs))
                # Enviar Notificação ao cliente
                #NotificacaoAutonoma.objects.create(destinatario=request.user, titulo='Transferência Confirmada', mensagem=f'pagamento confirmado: {valor_energia_kzs}kzs = {quantidade_kwh}kwh')
                #NotificacaoAutonoma.objects.create(destinatario=request.user, titulo='Transferência Confirmada', mensagem=f'pagamento confirmado: {valor_energia_kzs}kzs = {quantidade_kwh}kwh vindo de {request.user.usename}')
                return render(request, "paginas/transferencia_sucesso.html", {"destinatario": destinatario,
                                                                            "valor_energia_kzs": valor_energia_kzs})

        except request.exceptions.RequestException as e:
            return render(request, "paginas/erro.html",
                              {"mensagem": f"Erro na comunicação com o dispositivo Esp32: {str(e)}"})

        return render(request, "paginas/erro.html", {"mensagem": "Falha ao confirmar pagamento no Paypal"})
'''

import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Pagamento
from .forms import PagamentoForm

@login_required
def pagamento_view(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.usuario = request.user
            pagamento.status = 'Pendente'
            pagamento.save()

            #criar ordem no Paypal

            headers = {"Content-Type":"application/json",
                       "Authorization": f"Bearer{settings.PAYPAL_CLIENT_SECRET}"
            }
            data = {"intent": "CAPTURE",
                    "purchase_units": [{
                        "amount": {
                            "currency_code": settings.PAYPAL_CURRENCY,
                            "value": str(pagamento.valor)
                        }
                    }]
            }

            response = requests.post(f'{settings.PAYPAL_API_URL}/v2/checkout/ords', json=data, headers=headers)
            order_data = response.json()

            return redirect(order_data['links'][1]["href"])
    else:
        form = PagamentoForm()
    return render(request, "pagamento/iniciar_meu_pagamento.html", {'form': form})


