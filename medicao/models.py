from django.db import models
from django.contrib.auth.models import User
from cadastro.models import Residencia

'''
Modelo medição será responsável por armazenar os dados que o gateway envia
(como consumo de energia, energia restante, etc) Ela terá uma chave estrangeira
para a tabela Residencia, que se relaciona com o usuario
'''
# Create your models here.

class Medicao(models.Model):
    residencia = models.ForeignKey(Residencia, related_name='medicao', on_delete=models.CASCADE)
    energia_consumida_kwh = models.FloatField(default=0.0, verbose_name='Energia consumida em kwh', help_text='Valor da energia consumida em kwh')
    energia_restante_kwh = models.FloatField(default=0.0, verbose_name='Energia restante em kwh', help_text='Valor da energia restante em kwh')
    energia_comprada_kwh = models.FloatField(default=0.0, verbose_name='Energia comprada em kwh', help_text='Valor da energia comprada em kwh')
    energia_consumida_kzs = models.FloatField(default=0.0, verbose_name='Energia consumida em kzs', help_text='Valor da energia consumida em kzs')
    energia_restante_kzs = models.FloatField(default=0.0, verbose_name='Energia restante em kzs', help_text='Valor da energia restante em kzs')
    energia_comprada_kzs = models.FloatField(default=0.0, verbose_name='Energia comprada em kzs', help_text='Valor da energia comprada em kzs')
    status = models.BooleanField(default=False, help_text='Estado do relé: ON/OFF', verbose_name='Estado')
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Medição-{self.data_hora}'
    