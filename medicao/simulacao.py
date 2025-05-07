import requests
import random
from datetime import datetime

API_URL = "http://127.0.0.1:8000" # Endpoint da API
IDENTIFICADOR_RESIDENCIA = "Residencia_001"


def gerar_dados_simulados():
    for i in range(10):
        #Enviar 10 medições simuladas
        medicao = {
            "identificador_residencia": IDENTIFICADOR_RESIDENCIA,
            "tensao": round(random.uniform(210, 230), 2), # Exemplo: 210V a 230V
            "corrente": round(random.uniform(5, 15), 2), # Exemplo: 5A a 15A
            "potencia": round(random.uniform(1, 10), 2), # Exemplo: 1kwh a 10kwh
            "data_hora": datetime.now().isoformat() #Hora atual
        }

        response = requests.post(API_URL, json=medicao)
        if response.status_code == 201:
            print(f"Medição enviada com sucesso: {medicao}")
        else:
            print(f"Erro ao enviar medição: {response.json()}")

if __name__ == "__main__":
    gerar_dados_simulados()