# api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('credito/', views.receber_credito, name='receber_credito'),
    path('status_update/', views.status_update, name='status_update'),
]

