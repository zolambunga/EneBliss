from django.urls import path
from medicao.consumers import MedicaoConsumer

websocket_urlpatterns = [
    path('ws/medicao/', MedicaoConsumer.as_asgi()),
]
