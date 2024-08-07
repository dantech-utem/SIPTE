# Generated by Django 5.0.7 on 2024-07-12 08:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0024_alter_socioeconomicos_trabajas_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AntecedenteAcademico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bachillerato', models.CharField(max_length=100)),
                ('modalidad', models.CharField(max_length=100)),
                ('duracion', models.CharField(max_length=50)),
                ('promedio', models.IntegerField()),
                ('rendimiento', models.CharField(max_length=50)),
                ('materiasFacil', models.CharField(max_length=100)),
                ('materiasDificil', models.CharField(max_length=100)),
                ('materiasExtras', models.IntegerField()),
                ('cualesExtras', models.CharField(max_length=100)),
                ('repAnio', models.BooleanField()),
                ('nivelRep', models.CharField(max_length=100)),
                ('obstaculos', models.CharField(max_length=100)),
                ('idEstudiante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.estudiante')),
            ],
        ),
    ]
