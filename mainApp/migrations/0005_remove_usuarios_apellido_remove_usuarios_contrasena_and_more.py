# Generated by Django 5.0.6 on 2024-06-30 00:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_alter_bajaalumnos_fecha'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarios',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='usuarios',
            name='contrasena',
        ),
        migrations.RemoveField(
            model_name='usuarios',
            name='correo',
        ),
        migrations.RemoveField(
            model_name='usuarios',
            name='nombre',
        ),
        migrations.AddField(
            model_name='usuarios',
            name='User',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]