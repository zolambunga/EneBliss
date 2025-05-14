from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Medidor, StatusLog

@api_view(['POST'])
def receber_credito(request):
    device_id = request.data.get('device_id')
    valor_kwh = float(request.data.get('valor_kwh', 0))

    if not device_id or valor_kwh <= 0:
        return Response({'erro': 'Dados inválidos'}, status=400)

    medidor, _ = Medidor.objects.get_or_create(device_id=device_id)
    medidor.saldo_kwh += valor_kwh
    medidor.save()

    return Response({'mensagem': 'Crédito adicionado com sucesso'}, status=200)

@api_view(['POST'])
def status_update(request):
    device_id = request.data.get('device_id')
    status_text = request.data.get('status')
    motivo = request.data.get('motivo', '')

    if not device_id or not status_text:
        return Response({'erro': 'Dados incompletos'}, status=400)

    StatusLog.objects.create(device_id=device_id, status=status_text, motivo=motivo)
    return Response({'mensagem': 'Status recebido com sucesso'}, status=200)
