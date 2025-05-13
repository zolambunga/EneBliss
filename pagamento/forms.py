'''
from django import forms
from django.contrib.auth.models import Group, User
from django.conf import settings
from .models import Pagamento


class PagamentoForm(forms.ModelForm):

    class Meta:

        model = Pagamento
        # Adicionando os campos necessários que devem aparecer no formulário
        fields = ['valor']

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor < settings.PAGAMENTO_MINIMO_KZ:
            raise forms.ValidationError(f'O valor mínimo é kz {settings.PAGAMENTO_MINIMO_KZ}.')
        return valor
'''

