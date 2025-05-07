from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Mensagem


@receiver(post_save, sender=User)
def atualizar_mensagens_recebidas(sender, instance, created, **kwargs):
    '''
        Este sinal é acionado sempre que um Usuario estiver online. Verifica se o usuario tem
        novas mensagens, se tiver atualiza o status da mensagem para recebido
    '''

    print(f'SINAL ATIVO: {instance.username} ficou online')

    if instance.online:
       Mensagem.objects.filter(destinatario=instance,
                               status="enviada").update(status="recebida")

       #print(f'Mensagens pendentes encontradas: {mensagens.count()}')
       #mensagens.update(status="recebida")

       #mensagens.update(status="recebida")
