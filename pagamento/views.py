from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import paypalrestsdk
from .paypal_config import paypalrestsdk
import requests
from notificacao.models import NotificacaoAutonoma

@login_required
def pagamento_view(request):
    '''
        Sincronizando o django com o Paypal para iniciar o pagamento
    '''
    if request.method == 'POST':
        valor = request.POST.get("valor") # Captura o valor digitado pelo cliente
        pagamento = paypalrestsdk.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "transactions": [
                    {
                        "amount": {
                            "total": f"{valor}", "currency": "USD"
                        },
                        "description": f"Recarga de {valor}kzs "
                    }
                ],
                "redirect_urls":
                {
                        "return_url": "http://127.0.0.1:8000/pagamento/concluido/",
                        "cancel_url": "http://127.0.0.1:8000/erro/"
                }

            }
        )
        if pagamento.create():
            for link in pagamento.links:
                if link['rel'] == "approval_url":
                    return redirect(link['href']) # Redireciona para o Paypal
    return render(request, "pagamento/iniciar_meu_pagamento.html")


# Após o cliente autorizar o pagamento, Paypal retorna para o nosso sistema com detalhes da transação

def pagamento_concluido(request):
    '''
        confirma o pagamento e processa a recarga
    '''
    pagamento_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    pagamento = paypalrestsdk.Payment.find(pagamento_id)

    print(f'Estado antes:{pagamento.state}')

    if pagamento.execute({"payer_id": payer_id}):
        valor_recarga = pagamento.transactions[0]['amount']['total']

        # Enviar sinal para ESP32 via HTTP
        '''url_esp32 = "http://192.168.1.100/recarga"
        dados = {"valor_recarga": valor_recarga}
        response = requests.post(url_esp32, json=dados)

        if response.status_code == 200:
            NotificacaoAutonoma.objects.create(destinatario=request.user, titulo='PAGAMENTO',
                                               mensagem=f'Parabens, o seu carregamento de {valor_recarga}kzs'
                                                        f'foi be sucedido. Se necessitar acesse comprovativo digital')

            return render(request, "paginas/sucesso.html", {"mensagem: Pagamento confirmado"})
        else:
            NotificacaoAutonoma.objects.create(destinatario=request.user, titulo='PAGAMENTO',
                                                mensagem=f'Falha na comunicação dos dispositivos com o SISTEMA. Entre em contacto...')

            return render(request, "paginas/erro.html", {"mensagem: Falha ao comunicar com o Esp32"})'''
        print(f'Estado depois:{pagamento.state} Saldo de {valor_recarga}')
        return redirect('painel-cliente')

    NotificacaoAutonoma.objects.create(destinatario=request.user, titulo='PAGAMENTO',
                                       mensagem=f'Pagamento Não Concluido. Entre em contacto...')


    return render(request, "paginas/erro.html", {"mensagem": "Pagamento não foi concluido"})

