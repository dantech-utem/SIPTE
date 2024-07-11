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
    token = models.CharField(max_length=225, blank=True, null=True)
    estado = models.IntegerField(default = 1) 

    
class Periodo(models.Model):
    periodo = models.CharField(max_length=100)   
    anio = models.IntegerField() 
    estado =models.BooleanField(default=True)

class CierreTutorias(models.Model):
    cierreTutorias= models.TextField(blank=True, null=True)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    cicloAccion = models.ForeignKey(Periodo, on_delete=models.CASCADE,null=True)

class AccionTutorial(models.Model):
    tema = models.CharField(max_length=100)
    objetivos = models.CharField(max_length=400)
    actividades = models.CharField(max_length=400)
    recursos = models.CharField(max_length=400)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    evidencias = models.CharField(max_length=400, blank=True)
    cicloAccion = models.ForeignKey(Periodo, on_delete=models.CASCADE, null=True)

respuestas=[1,'Nunca'],[2,'Casi nunca'],[3,'Casi siempre'],[4,'Siempre']
    
class EvaluacionTutor(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    puntualidad = models.IntegerField(choices=respuestas,default=4)
    proposito = models.IntegerField(choices=respuestas,default=4)
    planTrabajo = models.IntegerField(choices=respuestas,default=4)
    temasPrevistos = models.IntegerField(choices=respuestas,default=4)
    temasInteres = models.IntegerField(choices=respuestas,default=4)
    disposicionTutor = models.IntegerField(choices=respuestas,default=4)
    cordialidad = models.IntegerField(choices=respuestas,default=4)
    orientacion = models.IntegerField(choices=respuestas,default=4)
    dominio = models.IntegerField(choices=respuestas,default=4)
    impacto = models.IntegerField(choices=respuestas,default=4)
    serviciosApoyo = models.IntegerField(choices=respuestas,default=4)
    cicloEvaluacion = models.ForeignKey(Periodo, on_delete=models.CASCADE,null=True)

class BajaAlumnos(models.Model):
    cicloAccion = models.ForeignKey(Periodo, on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=100)
    observaciones = models.TextField()
    motivo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

class AtencionIndividual(models.Model):
    estudiante = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    cicloAccion = models.ForeignKey(Periodo, on_delete=models.CASCADE, null=True)
    asuntoTratar = models.CharField(max_length=400)
    observaciones = models.CharField(max_length=400)
    fecha = models.DateTimeField(auto_now_add=True)
    bajasAlumno = models.ForeignKey(BajaAlumnos, on_delete=models.CASCADE, null=True, blank=True)
    

class Canalizacion(models.Model):
    atencionIndividual = models.ForeignKey(AtencionIndividual, on_delete=models.CASCADE, null=True)
    cicloAccion = models.ForeignKey(Periodo, on_delete=models.CASCADE,null=True)
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