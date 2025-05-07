''''
Serializer: Convertendo os dados
O serializer transforma o objecto Medicao em Json para facilitar a comunicação entre o Django e o Esp32
'''

from rest_framework import serializers
from .models import Medicao

class MedicaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicao
        fields = '__all__'

