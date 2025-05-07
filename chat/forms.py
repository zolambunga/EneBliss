from django import forms
from django.contrib.auth.models import User
from .models import Mensagem

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['destinatario', 'conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'placeholder': 'Escreva a sua mensagem aqui...'})
        }

class SelecionarOperadorForm(forms.Form):
    operador = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Operador'))#, ativo=True
    label = "Selecione um Operador disponivel"