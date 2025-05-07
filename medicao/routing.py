from django.urls import path
from medicao.consumers import MedicaoConsumer

websocket_urlpatterns = [
    path('ws/medicoes/', MedicaoConsumer.as_asgi()),
]
