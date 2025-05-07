from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Mensagem(models.Model):
    remetente = models.ForeignKey(User, related_name="mensagens_enviadas", on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, related_name="mensagens_recebidas", on_delete=models.CASCADE)
    conteudo = models.TextField()
    lida = models.BooleanField(default=False)
    data_envio = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ("enviada", "✓"),
        ("recebida", "✓✓"),
        ("visualizada", "✓✓ azul")
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="enviada")

    def __str__(self):
        return f'{self.remetente.username} to {self.destinatario.username} {self.status}'
