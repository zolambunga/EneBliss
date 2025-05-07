from django.db.models.signals import post_save
from django.dispatch import receiver
from medicao.models import Medicao
from .models import NotificacaoAutonoma
from cadastro.models import Residencia


@receiver(post_save, sender=Medicao)
def gerar_notificacao(sender, instance, created, **kwargs):
    '''
        Este sinal é acionado sempre que um objeto do modelo Mediçao passa do limite.
        Verifica se o consumo atual ultrapassar o limite, cria uma notificação
    '''

    residencia = instance.residencia # Acessa a residencia associada a medição
    usuario = residencia.usuario #Acessa o usuario associado a residencia

    if instance.energia_restante_kwh <= 5 or instance.energia_restante_kzs <= 500:
        mensagem = f'Por Favor Recarregue a Energia e Evite Cortes'
        NotificacaoAutonoma.objects.create(destinatario=usuario, titulo='Alerta Energia', mensagem=mensagem)


# Create your tests here.
