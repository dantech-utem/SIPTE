# Generated by Django 4.1.7 on 2024-06-30 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0010_remove_usuarios_apellido_remove_usuarios_contrasena_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acciontutorial',
            name='tutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]