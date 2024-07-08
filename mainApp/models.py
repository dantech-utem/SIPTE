from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=100)
    
class Usuarios(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    noControl = models.CharField(max_length=20)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    grupo = models.CharField(max_length=20)
    token = models.CharField(max_length=225, blank=True, null=True)  # Campo para almacenar el token

class Periodo(models.Model):
    periodo = models.CharField(max_length=100)   
    anio = models.IntegerField() 

class AccionTutorial(models.Model):
    tema = models.CharField(max_length=100)
    objetivos = models.CharField(max_length=400)
    actividades = models.CharField(max_length=400)
    recursos = models.CharField(max_length=400)
    tutor = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    cicloAccion = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    cierreTutorias= models.TextField()
    
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
    estado = models.IntegerField() 
    bajasAlumno = models.ForeignKey(BajaAlumnos, on_delete=models.CASCADE)

class Canalizacion(models.Model):
    atencionIndividual = models.ForeignKey(AtencionIndividual, on_delete=models.CASCADE)
    area = models.CharField(max_length=150)
    observaciones = models.TextField()
    motivo = models.TextField()
    detalles = models.TextField(null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estadoCanalizados = models.IntegerField(default=1)
    titulo = models.CharField(max_length=100, null=True)
    descripcion = models.TextField(null=True)
    FechaInicio = models.DateTimeField(null=True)
    FechaFinal = models.DateTimeField(null=True)    