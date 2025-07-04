# Generated by Django 5.2.1 on 2025-05-14 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Medidor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=50, unique=True)),
                ('saldo_kwh', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=20)),
                ('motivo', models.CharField(blank=True, max_length=100)),
                ('data', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
