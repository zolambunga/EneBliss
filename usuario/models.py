from django.db import models
from django.contrib.auth.models import User


# Create your models here.


User.add_to_class('online', models.BooleanField(default=False))
User.add_to_class('tempo_de_atividade', models.DateTimeField(auto_now=True)) #Ultima atividade do usuario

