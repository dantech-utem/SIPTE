# Generated by Django 5.0.7 on 2024-07-12 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0031_alter_estudiante_nocontrol'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosAficiones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiempoLibre', models.CharField(choices=[('', 'Selecciona una opción'), ('Practicar algún deporte', 'Practicar algún deporte'), ('Leer', 'Leer'), ('Escuchar música', 'Escuchar música'), ('Salir o estar con amigos', 'Salir o estar con amigos'), ('Ir al cine', 'Ir al cine'), ('Ver TV', 'Ver TV'), ('Redes sociales', 'Redes sociales'), ('Navegar en Internet', 'Navegar en Internet'), ('Jugar juegos en computadora, celular', 'Jugar juegos en computadora, celular'), ('Otro', 'Otro')], default='', max_length=100)),
                ('horasLibre', models.CharField(choices=[('', 'Selecciona una opción'), ('Media hora', 'Media hora'), ('Una hora', 'Una hora'), ('Hora y media', 'Hora y media'), ('Dos horas', 'Dos horas'), ('Tres horas', 'Tres horas'), ('Más de tres horas', 'Más de tres horas')], default='', max_length=100)),
                ('idEstudiante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='DatosPersonalidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colaborasCasa', models.CharField(choices=[('Si', 'Sí'), ('No', 'No')], default='', max_length=2)),
                ('colaboracion', models.CharField(choices=[('Mucho', 'Mucho'), ('Regular', 'Regular'), ('Solo lo necesario', 'Solo lo necesario'), ('Poco', 'Poco'), ('Nada', 'Nada')], default='', max_length=20)),
                ('ambienteFamiliar', models.CharField(choices=[('Totalmente', 'Totalmente'), ('Bastante', 'Bastante'), ('Suficiente', 'Suficiente'), ('Regular', 'Regular'), ('Poco', 'Poco'), ('Nada', 'Nada')], default='', max_length=20)),
                ('hablaFamiliar', models.CharField(choices=[('Siempre', 'Siempre'), ('Casi siempre', 'Casi siempre'), ('A veces', 'A veces'), ('Casi nunca', 'Casi nunca'), ('Nunca', 'Nunca')], default='', max_length=20)),
                ('comunicacion', models.CharField(choices=[('Si', 'Sí'), ('No', 'No')], default='', max_length=2)),
                ('idEstudiante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='DatosSalud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estadoSalud', models.CharField(choices=[('Muy buena', 'Muy buena'), ('Buena', 'Buena'), ('Regular', 'Regular'), ('Mala', 'Mala')], max_length=20)),
                ('enfermedadGrave', models.CharField(choices=[('Si', 'Sí'), ('No', 'No')], max_length=2)),
                ('tipoEnfermedad', models.CharField(blank=True, max_length=100)),
                ('padecimientoCro', models.CharField(blank=True, max_length=100)),
                ('tipoPadecimiento', models.CharField(blank=True, max_length=100)),
                ('operaciones', models.CharField(choices=[('Si', 'Sí'), ('No', 'No')], max_length=2)),
                ('causaOperacion', models.CharField(blank=True, max_length=100)),
                ('problemaSalud', models.TextField(blank=True)),
                ('condiciones', models.CharField(choices=[('Si', 'Sí'), ('No', 'No')], max_length=2)),
                ('tipoCondiciones', models.CharField(blank=True, max_length=100)),
                ('comentario', models.TextField(blank=True)),
                ('idEstudiante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.estudiante')),
            ],
        ),
    ]
