# Generated by Django 5.0.7 on 2024-07-12 10:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0027_alter_antecedenteacademico_modalidad_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HabitosEstudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gustoLectura', models.IntegerField(choices=[(1, 'Nunca'), (2, 'Casi nunca'), (3, 'Casi siempre'), (4, 'Siempre')])),
                ('tipoLectura', models.CharField(choices=[('Novelas', 'Novelas'), ('Cuentos', 'Cuentos'), ('Poesía', 'Poesía'), ('Noticias', 'Noticias'), ('Ciencia Ficción', 'Ciencia Ficción'), ('Libros de texto', 'Libros de texto'), ('Artículos de divulgación', 'Artículos de divulgación'), ('Artículos de opinión', 'Artículos de opinión'), ('Otro', 'Otro')], max_length=50)),
                ('sitioLectura', models.IntegerField(choices=[(1, 'Nunca'), (2, 'Casi nunca'), (3, 'Casi siempre'), (4, 'Siempre')])),
                ('descripEstudio', models.TextField()),
                ('horas', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('Más de 5', 'Más de 5')], max_length=10)),
                ('horario', models.IntegerField(choices=[(1, 'Nunca'), (2, 'Casi nunca'), (3, 'Casi siempre'), (4, 'Siempre')])),
                ('musica', models.IntegerField(choices=[(1, 'Nunca'), (2, 'Casi nunca'), (3, 'Casi siempre'), (4, 'Siempre')])),
                ('idEstudiante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.estudiante')),
            ],
        ),
    ]
