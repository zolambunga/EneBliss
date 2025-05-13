
from django.urls import path
#from .views import MedicaoAPIView
from .views import solicitar_medicao

urlpatterns = [
    path('solicitar_medicao/', solicitar_medicao, name='solicitar-medicao')
]

