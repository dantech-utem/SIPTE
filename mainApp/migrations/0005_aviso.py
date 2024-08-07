# Generated by Django 5.0.6 on 2024-07-05 00:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_alter_bajaalumnos_fecha'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aviso',
            fields=[
                ('idAvisos', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
