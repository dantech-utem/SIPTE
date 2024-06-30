# Generated by Django 4.1.7 on 2024-06-30 00:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0009_alter_acciontutorial_tutor'),
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
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
