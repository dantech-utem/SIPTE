# Generated by Django 5.0.6 on 2024-06-21 02:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('noControl', models.CharField(max_length=20)),
                ('correo', models.CharField(max_length=100)),
                ('contrasena', models.CharField(max_length=100)),
                ('grupo', models.CharField(max_length=20)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.tipousuario')),
            ],
        ),
    ]
