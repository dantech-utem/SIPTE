from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=100)
    
class Usuarios(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    noControl = models.CharField(max_length=20)
    correo = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    grupo = models.CharField(max_length=20)
    
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
    detalles = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    FechaInicio = models.DateTimeField()
    FechaFinal = models.DateTimeField()

class Aviso(models.Model):
    idAvisos = models.AutoField(primary_key=True)
    #id_Usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='avisos')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    
    def __str__(self):
        return self.titulo
    
class Estudiante(models.Model):
    idEstudiante = models.AutoField(primary_key=True)
    carrera = models.CharField(max_length=255)
    tutor = models.CharField(max_length=255)
    grupo = models.CharField(max_length=50)
    fechaR = models.DateField()
    nombre = models.CharField(max_length=255)
    noControl = models.CharField(max_length=8, unique=True)
    telCasa = models.CharField(max_length=10)
    correo = models.EmailField(unique=True)
    telCelular = models.CharField(max_length=10)
    edad = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre 

class DatosFamiliares(models.Model):
    idEstudiante = models.ForeignKey(Estudiante, null=True, blank=True, on_delete=models.CASCADE)
    conviveCon = models.CharField(max_length=100)
    otra_situacion = models.CharField(max_length=100, blank=True)
    huerfano = models.BooleanField()
    huerfanoQuien = models.CharField(max_length=100)
    totalHermanos = models.IntegerField()
    lugarHermano = models.IntegerField()
    estadoCivil = models.CharField(max_length=50)

    def __str__(self):
        if self.idEstudiante:
            return "Datos familiares de estudiante con No. de control {self.idEstudiante.noControl}"
        else:
            return "Datos familiares sin estudiante asociado"
