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

'''
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Medicao



class MedicaoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        residencia_id = data['residencia']
        medicao = Medicao.objects.filter(residencia_id=residencia_id).order_by("data_hora")

        await self.send(text_data_json=json.dumps({
            'tensao': medicao.tensao,
            'corrente': medicao.corrente,
            'potencia': medicao.potencia
        }))
'''

# DADOS SIMULADOS

import json
import random, asyncio
from datetime import datetime
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from cadastro.models import Residencia
class MedicaoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        usuario = self.scope['user']
        if usuario.is_authenticated:
            residencia = Residencia.objects.get(usuario=usuario)
            self.residencia_id = residencia.id
            await self.accept()

    async def receive(self, text_data):
        while True:
            dados_simulados = {
                "residencia": self.residencia_id,
                "data_hora": datetime.now().isoformat(), # Hora atual
                "tensao": round(random.uniform(210, 230), 2), # Exemplo: 210V a 230V
                "corrente": round(random.uniform(5, 15), 2),  # Exemplo: 5A a 15A
                "potencia": round(random.uniform(1000, 3000), 2),
            }
            await self.send(text_data=json.dumps(dados_simulados))
            await asyncio.sleep(5)

