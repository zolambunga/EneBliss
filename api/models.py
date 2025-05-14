from django.db import models

# Create your models here.
class   Medidor(models.Model):
    device_id = models.CharField(max_length=50, unique=True)
    saldo_kwh = models.FloatField(default=0)

class   StatusLog(models.Model):
    device_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    motivo = models.CharField(max_length=100, blank=True)
    data = models.DateTimeField(auto_now_add=True)
