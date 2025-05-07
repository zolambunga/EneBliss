'''

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Medicao



class MedicaoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Id da residencia do cliente logado
        self.residencia_id = self.scope['user'].residencia.id

       #
        await self.channel_layer.group_add(f'medicao_{self.residencia_id}', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        self.channel_layer.group_discard(f'medicao_{self.residencia_id}', self.channel_name)


    async def receive(self, text_data):
        #Receber dados enviados pelo websocket
        medicoes = Medicao.objects.filter(residencia_id=self.residencia_id).order_by("-data_hora")[:10]
        data = [{"data_hora": medicao.data_hora.strftime("%H:%M:%S"), "energia": medicao.energia}
                for medicao in medicoes]
        await self.send(text_data_json=json.dumps(data))
'''

# DADOS SIMULADOS

import json
import random
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
class MedicaoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Id da residencia do cliente logado
        self.residencia_id = "Residencia_001"

       #
        await self.channel_layer.group_add(f'medicao_{self.residencia_id}', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        self.channel_layer.group_discard(f'medicao_{self.residencia_id}', self.channel_name)

    async def gerar_dados_simulados(self):
        # Gerar medições simuladas

        return {
            "data_hora": datetime.now().isoformat(), # Hora atual
            "energia": round(random.uniform(1, 10), 2),  # Exemplo: 1kwh a 10kwh
            "tensao": round(random.uniform(210, 230), 2), # Exemplo: 210V a 230V
            "corrente": round(random.uniform(5, 15), 2),  # Exemplo: 5A a 15A
            "potencia": round(random.uniform(1000, 3000), 2),  #
        }

    async def receive(self, text_data):
        #Envia  dados simulados ao frontend
        medicao_simulada = await self.gerar_dados_simulados()
        await self.send(text_data=json.dumps(medicao_simulada))


