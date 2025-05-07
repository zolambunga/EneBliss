from django.db import models
from django.contrib.auth.models import User
from cadastro.models import Residencia


# Create your models here.
class HistoricoEnergia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    residencia = models.ForeignKey(Residencia, on_delete=models.CASCADE)
    tipo_transacao = models.CharField(max_length=50, choices=[('COMPRA', 'Compra'), ('CONSUMO', 'Consumo')])
    quatidade_kwh = models.FloatField(default=0.0, verbose_name='Energia em Kwh', help_text='Valor da energia em kwh')
    valor_energia_kzs = models.FloatField(default=0.0, verbose_name='Energia em Kzs', help_text='Valor da energia em kzs')
    data_transacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.quatidade_kwh} Kwh em {self.data_transacao}"
