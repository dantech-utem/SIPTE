# Generated by Django 5.0.7 on 2024-07-12 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0018_socioeconomicos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socioeconomicos',
            name='manutencion',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='socioeconomicos',
            name='relacionCarrera',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='socioeconomicos',
            name='tenencia',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='socioeconomicos',
            name='trabajoMama',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='socioeconomicos',
            name='trabajoPapa',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='socioeconomicos',
            name='vivienda',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]