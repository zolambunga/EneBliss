from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Medicao
from .serializers import MedicaoSerializer
from cadastro.models import Residencia
from django.http import JsonResponse


'''
class MedicaoAPIView(APIView):
    def __post__(self, request):
        data = request.data
        try:
            residencia = Residencia.objects.get(identificador=data.get("identificador_residencia"))
        except Residencia.DoesNotExist:
            return Response({"error": "Residencia não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Salvar os dadsos no banco de dados

        Medicao.objects.create(
            residencia=residencia,
            tensao=data.get("tensao"),
            corrente=data.get("corrente"),
            potencia=data.get("potencia"),
            energia=data.get("energia")
        )
        return Response({"sucesso": "Medicao registrada com sucesso!"}, status=status.HTTP_201_CREATED)
'''

def solicitar_medicao(request):

    usuario = request.user
    residencia_id = usuario.residencia.id
    url_esp32 = f'http://esp32-ip-local/medir?residencia={residencia_id}'
    resposta = request.get(url_esp32)

    if resposta.status_code == 200:
        dados = resposta.json()
        medicao = Medicao.objects.create(

            residencia=usuario.residencia,
            tensao=dados.get["tensao"],
            corrente=dados.ge["corrente"],
            potencia=dados.get["potencia"],
            energia=dados.get["energia"],

        )
        return JsonResponse(MedicaoSerializer(MedicaoSerializer(medicao)).data)

    else:

        return JsonResponse({'Erro': 'Falha ao obterv dados do Esp32'}, status=500)


