
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pagamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    referencia_esp32 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.usuario} - Kzs {self.valor} ({self.status})'


