
from django.urls import path
from .views import MedicaoAPIView

urlpatterns = [
    path('medicoes/', MedicaoAPIView.as_view(), name='medicoes')
]

