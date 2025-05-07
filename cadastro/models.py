from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
#from medicao.models import Medicao

# Create your models here.

'''
A tabela PT representará a central que distribui a energia até os posts.
Dependencia: a tabela PT será independente
'''
class PT(models.Model):
    nome_pt = models.CharField(max_length=255, unique=True, verbose_name='Nome do PT')
    numero_pt = models.IntegerField(unique=True, verbose_name='Numero do PT')
    municipio_pt = models.CharField(max_length=255, verbose_name='Município')
    bairro_pt = models.CharField(max_length=255, verbose_name='Bairro')
    data_pt = models.DateTimeField(auto_now=True, verbose_name='Data de cadastramento')

    def __str__(self):
        return f'{self.nome_pt}({self.numero_pt})'


'''
A tabela post será responsável por identificar os posts que distribuem energia  para as residências
Dependencia: A tabelas Post será dependente da tabela PT
'''
class Post(models.Model):
    pt = models.ForeignKey(PT, related_name='posts', on_delete=models.CASCADE, verbose_name='Posto de Transformação(PT)')
    nome_post = models.CharField(max_length=255, verbose_name='Nome do Post')
    numero_post = models.IntegerField(verbose_name='Numero do Post')
    rua_post = models.CharField(max_length=255, verbose_name='Rua')
    data_post = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('numero_post', 'pt')

    def __str__(self):
        #return f'Nome do Post: {self.nome_post}({self.numero_post})'
        return f'Nome do Post: {self.nome_post}({self.numero_post})'


User.add_to_class('telefone', models.CharField(max_length=13,
                                               validators=[RegexValidator(regex=r'^\+244\d{9}$',
                                                message="Formato inválido!")],
                                               default="+244", blank=False))
User.add_to_class('foto_perfil', models.ImageField(upload_to='fotos_usuarios/', default='fotos_usuarios/sem-foto.png'))






'''
A tabela residência armazenará as informações das residencias que
estão recebendo a medicao, incluindo o estado do relé e a medicao restante
Dependência: cada residência pertence a um post e está associado a um usuario
'''

class Residencia(models.Model):
    post = models.ForeignKey(Post, related_name='residencias', on_delete=models.CASCADE)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='residencia', null=False)
    #medicao = models.ForeignKey(Medicao, on_delete=models.CASCADE, related_name="medição")
    numero_residencia = models.IntegerField(verbose_name='Numero da Residência')
    nome_proprietario = models.CharField(max_length=255, verbose_name='Proprietário')
    endereco_residencia = models.CharField(max_length=255, verbose_name='Endereço', help_text='Endereço')
    endereco_esp32 = models.CharField(max_length=255, verbose_name="Esp32 Endereço") #Ip do gateway
    ativo_residencia = models.BooleanField(default=True, verbose_name='Residência no activo')
    data_residencia = models.DateTimeField(auto_now_add=True, verbose_name='Data de registro')


    class Meta:
        #Garante que não pode haver numero de casas iguais para o mesmo Post
        unique_together = ('numero_residencia', 'post')


    def __str__(self):
        return f'Residencia de {self.nome_proprietario}, Post {self.post.nome_post}'






