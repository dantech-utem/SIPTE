from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=100)
    
class Usuarios(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    noControl = models.CharField(max_length=20)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    grupo = models.CharField(max_length=20)
    
class Periodo(models.Model):
    periodo = models.CharField(max_length=100)   
    anio = models.IntegerField() 
    estado =models.BooleanField(default=True)

class AccionTutorial(models.Model):
    tema = models.CharField(max_length=100)
    objetivos = models.CharField(max_length=400)
    actividades = models.CharField(max_length=400)
    recursos = models.CharField(max_length=400)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    cicloAccion = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    cierreTutorias= models.TextField(blank=True, null=True)
    evidencias = models.CharField(max_length=400, blank=True)
    
    
class Evidencia(models.Model):
    evidencia = models.FileField(upload_to='evidenciaAccionTutorial/')
    accionRutorial = models.ForeignKey(AccionTutorial, on_delete=models.CASCADE)
    
class EvaluacionTutor(models.Model):
    estudiante = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    respuestaUno = models.IntegerField() 

class BajaAlumnos(models.Model):
    tipo = models.CharField(max_length=100)
    observaciones = models.TextField()
    motivo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

class AtencionIndividual(models.Model):
    estudiante = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    asuntoTratar = models.CharField(max_length=400)
    observaciones = models.CharField(max_length=400)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.IntegerField(blank=True, null=True) 
    bajasAlumno = models.ForeignKey(BajaAlumnos, on_delete=models.CASCADE, null=True, blank=True)

    
class Canalizacion(models.Model):
    atencionIndividual = models.ForeignKey(AtencionIndividual, on_delete=models.CASCADE)
    area = models.CharField(max_length=150)
    detalles = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    FechaInicio = models.DateTimeField()
    FechaFinal = models.DateTimeField()