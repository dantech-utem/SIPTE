# Generated by Django 5.0.6 on 2024-07-05 02:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_aviso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aviso',
            name='idUsuario',
        ),
    ]
