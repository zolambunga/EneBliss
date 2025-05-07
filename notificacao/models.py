
from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.

class NotificacaoAutonoma(models.Model):
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255, verbose_name='Titulo')
    mensagem = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return f'Notificação para {self.destinatario.username} - {self.mensagem[:50]}'


class NotificacaoAdmin(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Titulo')
    remetente = models.ForeignKey(User, on_delete=models.CASCADE)
    mensagem = models.TextField()
    grupo_destinatario = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="notificacoes_admin")
    #grupo_destino = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="notificacoes_admin")
    STATUS_CHOICES = [("enviada", "✓")]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="enviada"),
    data_criacao = models.DateTimeField(auto_now_add=True)

    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return f'Notificação do Admin {self.remetente.username} - {self.mensagem[:50]}({self.grupo_destinatario})'

