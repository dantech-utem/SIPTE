# Generated by Django 5.0.6 on 2024-06-22 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_bajaalumnos_motivo_bajaalumnos_observaciones_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bajaalumnos',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
