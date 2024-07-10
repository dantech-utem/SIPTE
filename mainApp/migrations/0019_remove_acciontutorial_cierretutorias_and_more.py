# Generated by Django 5.0.6 on 2024-07-09 23:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0018_evaluaciontutor_cicloevaluacion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acciontutorial',
            name='cierreTutorias',
        ),
        migrations.AddField(
            model_name='atencionindividual',
            name='cicloAccion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.periodo'),
        ),
        migrations.AddField(
            model_name='bajaalumnos',
            name='cicloAccion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.periodo'),
        ),
        migrations.AddField(
            model_name='canalizacion',
            name='cicloAccion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.periodo'),
        ),
        migrations.AddField(
            model_name='canalizacion',
            name='descripcion',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='canalizacion',
            name='estadoCanalizados',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='canalizacion',
            name='motivo',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='canalizacion',
            name='observaciones',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='canalizacion',
            name='titulo',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='canalizacion',
            name='FechaFinal',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='canalizacion',
            name='FechaInicio',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='canalizacion',
            name='atencionIndividual',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.atencionindividual'),
        ),
        migrations.AlterField(
            model_name='canalizacion',
            name='detalles',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='CierreTutorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cierreTutorias', models.TextField(blank=True, null=True)),
                ('cicloAccion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.periodo')),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Evidencia',
        ),
    ]
