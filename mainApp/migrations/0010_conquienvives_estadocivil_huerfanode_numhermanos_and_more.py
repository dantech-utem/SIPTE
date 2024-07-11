# Generated by Django 5.0.6 on 2024-07-10 00:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0009_rename_estudiantes_estudiante'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConQuienVives',
            fields=[
                ('idVives', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoCivil',
            fields=[
                ('idCivil', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HuerfanoDe',
            fields=[
                ('idHuerfano', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NumHermanos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DatosFamiliares',
            fields=[
                ('idDatosf', models.AutoField(primary_key=True, serialize=False)),
                ('otra_situacion', models.TextField(blank=True, null=True)),
                ('huerfano', models.BooleanField()),
                ('lugarHermano', models.IntegerField()),
                ('conviveCon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.conquienvives')),
                ('idEstudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.estudiante')),
                ('estadoCivil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.estadocivil')),
                ('huerfanoQuien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.huerfanode')),
                ('totalHermanos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.numhermanos')),
            ],
        ),
    ]