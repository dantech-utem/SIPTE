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
    noControl = models.CharField(max_length=8)
    nombre = models.CharField(max_length=200)
    carrera = models.CharField(max_length=200, choices=[
        ('Licenciatura en Diseño y Gestión de Redes Logísticas', 'Licenciatura en Diseño y Gestión de Redes Logísticas'),
        ('Ingeniería en Energías Renovables', 'Ingeniería en Energías Renovables'),
        ('Licenciatura en Contaduría', 'Licenciatura en Contaduría'),
        ('Licenciatura en Gastronomía', 'Licenciatura en Gastronomía'),
        ('Ingeniería en Logística Comercial Global', 'Ingeniería en Logística Comercial Global'),
        ('Ingeniería en Mantenimiento Industrial', 'Ingeniería en Mantenimiento Industrial'),
        ('Ingeniería en Procesos Químicos', 'Ingeniería en Procesos Químicos'),
        ('Ingeniería en Desarrollo y Gestión de Software', 'Ingeniería en Desarrollo y Gestión de Software'),
    ])
    tutor = models.CharField(max_length=200, choices=[
        ('Guillermo Jair Rincón Cruzado', 'Guillermo Jair Rincón Cruzado'),
        ('Miriam Minerva Jiménez Lara', 'Miriam Minerva Jiménez Lara'),
        ('Heriberto Pérez Romero', 'Heriberto Pérez Romero'),
        ('Alicia Judith Figueroa García', 'Alicia Judith Figueroa García'),
        ('Juan Ríos Hernández', 'Juan Ríos Hernández'),
        ('Francisco Fortino Güereña Galaz', 'Francisco Fortino Güereña Galaz'),
        ('David Manuel Ramos Sánchez', 'David Manuel Ramos Sánchez'),
        ('Juan Manuel Fernández Álvarez', 'Juan Manuel Fernández Álvarez'),
    ])
    grupo = models.CharField(max_length=20, choices=[
        ('1-GAS-1', '1-GAS-1'),
        ('9-IDG-1', '9-IDG-1'),
        ('4-TID-1', '4-TID-1'),
    ])
    fechaR = models.DateField(auto_now_add=True)
    telCasa = models.CharField(max_length=10)
    correo = models.EmailField()
    telCelular = models.CharField(max_length=10)
    edad = models.CharField(max_length=10, choices=[
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('Más de 30', 'Más de 30'),
    ])

    def __str__(self):
        return self.nombre 

class DatosFamiliares(models.Model):
    idEstudiante = models.ForeignKey(Estudiante, null=True, blank=True, on_delete=models.CASCADE)
    conviveCon = models.CharField(max_length=200, choices=[
        ('Mis papás', 'Mis papás'),
        ('Con mi papá', 'Con mi papá'),
        ('Con mi mamá', 'Con mi mamá'),
        ('Con mis parientes(tíos,abuelos,etc.)', 'Con mis parientes(tíos,abuelos,etc.)'),
        ('Con mis amigos', 'Con mis amigos'),
        ('Solo', 'Solo'),
        ('Otra situación', 'Otra situación'),
    ])
    otra_situacion = models.CharField(max_length=200, blank=True)
    huerfano = models.CharField(max_length=2, choices=[
        ('Si', 'Si'),
        ('No', 'No'),
    ])
    huerfanoQuien = models.CharField(max_length=20, choices=[
        ('No aplica', 'No aplica'),
        ('Padre', 'Padre'),
        ('Madre', 'Madre'),
        ('Ambos', 'Ambos'),
    ])
    totalHermanos = models.IntegerField()
    lugarHermano = models.IntegerField()
    estadoCivil = models.CharField(max_length=20, choices=[
        ('Soltero', 'Soltero'),
        ('Casado', 'Casado'),
        ('Unión libre', 'Unión libre'),
        ('Divorciado(a)', 'Divorciado(a)'),
    ])

    def __str__(self):
        if self.idEstudiante:
            return f"Datos familiares de estudiante con No. de control {self.idEstudiante.noControl}"
        else:
            return "Datos familiares sin estudiante asociado"

class Socioeconomicos(models.Model):
    idEstudiante = models.ForeignKey(Estudiante, null=True, blank=True, on_delete=models.CASCADE)
    vivienda = models.CharField('vivienda', max_length=100, choices=[
        ('', 'Selecciona una opción'),
        ('Casa', 'Casa'),
        ('Casa en coto privado', 'Casa en coto privado'),
        ('Departamento', 'Departamento'),
        ('Departamento multifamiliar', 'Departamento multifamiliar'),
        ('Casa de huéspedes', 'Casa de huéspedes'),
    ], default='')

    tenencia = models.CharField('tenencia', max_length=100, choices=[
        ('', 'Selecciona una opción'),
        ('Propia', 'Propia'),
        ('Rentada', 'Rentada'),
        ('Prestada', 'Prestada'),
        ('Hipotecada', 'Hipotecada'),
        ('Otra', 'Otra'),
    ], default='')

    habitaciones = models.CharField('habitaciones', max_length=100, choices=[
        ('', 'Selecciona una opción'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('Más de 10', 'Más de 10'),
    ], default='')

    vehiculos = models.CharField('vehiculos', max_length=100, choices=[
        ('', 'Selecciona una opción'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('Más de 10', 'Más de 10'),
    ], default='')

    trabajoPapa = models.CharField('trabajoPapa', max_length=100, choices=[
        ('', 'Selecciona una opción'),
        ('Desempleado(a)', 'Desempleado(a)'),
        ('Jubilado(a) o pensionado(a)', 'Jubilado(a) o pensionado(a)'),
        ('Empleado del gobierno(a)', 'Empleado del gobierno(a)'),
        ('Agroproductor(a)', 'Agroproductor(a)'),
        ('Operario de producción(a)', 'Operario de producción(a)'),
        ('Comerciante', 'Comerciante'),
        ('Profesionista trabaja por cuenta propia', 'Profesionista trabaja por cuenta propia'),
        ('Militar (ejército o armada)', 'Militar (ejército o armada)'),
        ('Otro', 'Otro'),
    ], default='')

    trabajoextraPapa = models.CharField('trabajoextraPapa', max_length=100, blank=True)

    trabajoMama = models.CharField('trabajoMama', max_length=100, choices=[
        ('', 'Selecciona una opción'),
        ('Desempleado(a)', 'Desempleado(a)'),
        ('Jubilado(a) o pensionado(a)', 'Jubilado(a) o pensionado(a)'),
        ('Empleado del gobierno(a)', 'Empleado del gobierno(a)'),
        ('Agroproductor(a)', 'Agroproductor(a)'),
        ('Operario de producción(a)', 'Operario de producción(a)'),
        ('Comerciante', 'Comerciante'),
        ('Profesionista trabaja por cuenta propia', 'Profesionista trabaja por cuenta propia'),
        ('Militar (ejército o armada)', 'Militar (ejército o armada)'),
        ('Otro', 'Otro'),
    ], default='')

    trabajoextraMama = models.CharField('trabajoextraMama', max_length=100, blank=True)

    manutencion = models.CharField('manutencion', max_length=100, choices=[
        ('', 'Selecciona una opción'),
        ('Por cuenta propia', 'Por cuenta propia'),
        ('Mis papás costean mis gastos', 'Mis papás costean mis gastos'),
        ('Parte mis papás, parte yo', 'Parte mis papás, parte yo'),
    ], default='')

    trabajas =  models.CharField(max_length=10, choices=[
        ('Si', 'Si'),
        ('No', 'No'),
    ])

    relacionCarrera = models.CharField('relacionCarrera', max_length=100, choices=[
        ('', 'Selecciona una opción'),
        ('Mucho', 'Mucho'),
        ('Algo', 'Algo'),
        ('Nada', 'Nada'),
    ], default='')

    ingresoFam = models.CharField('ingresoFam', max_length=100, choices=[
        ('', 'Selecciona una opción'),
        ('De 3,000 a 5,000', 'De 3,000 a 5,000'),
        ('De 5,001 a 10,000', 'De 5,001 a 10,000'),
        ('De 10,001 a 15,000', 'De 10,001 a 15,000'),
        ('De 15,001 a 20,000', 'De 15,001 a 20,000'),
        ('De 20,001 a 25,000', 'De 20,001 a 25,000'),
        ('De 25,001 a 26,000', 'De 25,001 a 26,000'),
        ('De 26,001 a 30,000', 'De 26,001 a 30,000'),
        ('Más de 30,000', 'Más de 30,000'),
    ], default='')

    contribuyentes = models.CharField('contribuyentes', max_length=100, choices=[
        ('', 'Selecciona una opción'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('Más de 5', 'Más de 5'),
    ], default='')

    dependientesIngresos = models.CharField('dependientesIngresos', max_length=100, choices=[
        ('', 'Selecciona una opción'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('Más de 5', 'Más de 5'),
    ], default='')

    def __str__(self):
        return f"Socioeconómicos del estudiante {self.idEstudiante.noControl}"

class AntecedenteAcademico(models.Model):
    idEstudiante = models.ForeignKey(Estudiante, null=True, blank=True, on_delete=models.CASCADE)
    bachillerato = models.CharField(max_length=100)
    modalidad = models.CharField(max_length=50, choices=[
        ('Escolarizada', 'Escolarizada'),
        ('Semiescolarizada', 'Semiescolarizada'),
        ('Abierta', 'Abierta'),
        ('A distancia', 'A distancia'),
        ('Examen único', 'Examen único'),
    ])
    duracion = models.CharField(max_length=50, choices=[
        ('Menos de uno', 'Menos de uno'),
        ('Alrededor de un año', 'Alrededor de un año'),
        ('Más de un año', 'Más de un año'),
        ('Dos años', 'Dos años'),
        ('Tres años', 'Tres años'),
        ('Más de tres años', 'Más de tres años'),
    ])
    promedio = models.CharField(max_length=50, choices=[
        ('Entre 10 y 9.5', 'Entre 10 y 9.5'),
        ('Entre 9.4 y 9.0', 'Entre 9.4 y 9.0'),
        ('Entre 8.9 y 8.5', 'Entre 8.9 y 8.5'),
        ('Entre 8.4 y 8.0', 'Entre 8.4 y 8.0'),
        ('Entre 7.9 y 7.5', 'Entre 7.9 y 7.5'),
        ('Entre 7.4 y 6.0', 'Entre 7.4 y 6.0'),
        ('Menos de 6', 'Menos de 6'),
    ])
    rendimiento = models.CharField(max_length=50, choices=[
        ('Muy bueno', 'Muy bueno'),
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
        ('Malo', 'Malo'),
    ])
    materiasFacil = models.CharField(max_length=100)
    materiasDificil = models.CharField(max_length=100)
    materiasExtras = models.IntegerField()
    cualesExtras = models.CharField(max_length=100)
    repAnio = models.CharField(max_length=10, choices=[
        ('Si', 'Si'),
        ('No', 'No'),
    ])
    nivelRep = models.CharField(max_length=50, choices=[
        ('Primaria', 'Primaria'),
        ('Secundaria', 'Secundaria'),
        ('Bachillerato', 'Bachillerato'),
        ('Carrera Técnica', 'Carrera Técnica'),
        ('Otra', 'Otra'),
    ])
    obstaculos = models.TextField()

    def __str__(self):
        return f'Antecedente Académico de {self.idEstudiante.noControl}'
    


class HabitosEstudio(models.Model):
    idEstudiante = models.ForeignKey(Estudiante, null=True, blank=True, on_delete=models.CASCADE)
    respuestas = [
        (1, 'Nunca'),
        (2, 'Casi nunca'),
        (3, 'Casi siempre'),
        (4, 'Siempre')
    ]
    
    gustoLectura = models.CharField(max_length=10, choices=[
        ('Si', 'Si'),
        ('No', 'No'),
    ])
    tipoLectura = models.CharField(max_length=50, choices=[
        ('Novelas', 'Novelas'),
        ('Cuentos', 'Cuentos'),
        ('Poesía', 'Poesía'),
        ('Noticias', 'Noticias'),
        ('Ciencia Ficción', 'Ciencia Ficción'),
        ('Libros de texto', 'Libros de texto'),
        ('Artículos de divulgación', 'Artículos de divulgación'),
        ('Artículos de opinión', 'Artículos de opinión'),
        ('Otro', 'Otro'),
    ])
    sitioLectura = models.CharField(max_length=10, choices=[
        ('Si', 'Si'),
        ('No', 'No'),
    ])
    descripEstudio = models.TextField()
    horas = models.CharField(max_length=10, choices=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('Más de 5', 'Más de 5'),
    ])
    horario = models.CharField(max_length=10, choices=[
        ('Si', 'Si'),
        ('No', 'No'),
    ])
    musica = models.CharField(max_length=10, choices=[
        ('Si', 'Si'),
        ('No', 'No'),
    ])

    def __str__(self):
        return f'Hábitos de estudio de {self.idEstudiante.noControl}'
    


    
class DatosAficiones(models.Model):
    idEstudiante = models.ForeignKey(Estudiante, null=True, blank=True, on_delete=models.CASCADE)
    tiempoLibre = [
        ('', 'Selecciona una opción'),
        ('Practicar algún deporte', 'Practicar algún deporte'),
        ('Leer', 'Leer'),
        ('Escuchar música', 'Escuchar música'),
        ('Salir o estar con amigos', 'Salir o estar con amigos'),
        ('Ir al cine', 'Ir al cine'),
        ('Ver TV', 'Ver TV'),
        ('Redes sociales', 'Redes sociales'),
        ('Navegar en Internet', 'Navegar en Internet'),
        ('Jugar juegos en computadora, celular', 'Jugar juegos en computadora, celular'),
        ('Otro', 'Otro'),
    ]
    
    horasLibre = [
        ('', 'Selecciona una opción'),
        ('Media hora', 'Media hora'),
        ('Una hora', 'Una hora'),
        ('Hora y media', 'Hora y media'),
        ('Dos horas', 'Dos horas'),
        ('Tres horas', 'Tres horas'),
        ('Más de tres horas', 'Más de tres horas'),
    ]

    tiempoLibre = models.CharField(
        max_length=100,
        choices=tiempoLibre,
        default='',
        blank=False,
    )
    horasLibre = models.CharField(
        max_length=100,
        choices=horasLibre,
        default='',
        blank=False,
    )

    def __str__(self):
        return f"Datos de aficiones {self.idEstudiante.noControl}"

class DatosSalud(models.Model):
    idEstudiante = models.ForeignKey(Estudiante, null=True, blank=True, on_delete=models.CASCADE)
    estadoSalud = models.CharField(max_length=20, choices=[
        ('Muy buena', 'Muy buena'),
        ('Buena', 'Buena'),
        ('Regular', 'Regular'),
        ('Mala', 'Mala'),
    ])
    enfermedadGrave = models.CharField(max_length=2, choices=[
        ('Si', 'Sí'),
        ('No', 'No'),
    ])
    tipoEnfermedad = models.CharField(max_length=100, blank=True)
    padecimientoCro = models.CharField(max_length=100, blank=True)
    tipoPadecimiento = models.CharField(max_length=100, blank=True)
    operaciones = models.CharField(max_length=2, choices=[
        ('Si', 'Sí'),
        ('No', 'No'),
    ])
    causaOperacion = models.CharField(max_length=100, blank=True)
    problemaSalud = models.TextField(blank=True)
    condiciones = models.CharField(max_length=2, choices=[
        ('Si', 'Sí'),
        ('No', 'No'),
    ])
    tipoCondiciones = models.CharField(max_length=100, blank=True)
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"Datos de Salud: {self.idEstudiante.noControl}"
    

class DatosPersonalidad(models.Model):
      idEstudiante = models.ForeignKey(Estudiante, null=True, blank=True, on_delete=models.CASCADE)
      colaborasCasa = models.CharField(max_length=2, choices=[
        ('Si', 'Sí'),
        ('No', 'No'),
    ])
      colaboracion = models.CharField(max_length=20, choices=[
        ('Mucho', 'Mucho'),
        ('Regular', 'Regular'),
        ('Solo lo necesario', 'Solo lo necesario'),
        ('Poco', 'Poco'),
        ('Nada', 'Nada'),
    ])
      ambienteFamiliar = models.CharField(max_length=20, choices=[
            ('Totalmente', 'Totalmente'),
            ('Bastante', 'Bastante'),
            ('Suficiente', 'Suficiente'),
            ('Regular', 'Regular'),
            ('Poco', 'Poco'),
            ('Nada', 'Nada'),
    ])
      hablaFamiliar = models.CharField(max_length=20, choices=[
            ('Siempre', 'Siempre'),
            ('Casi siempre', 'Casi siempre'),
            ('A veces', 'A veces'),
            ('Casi nunca', 'Casi nunca'),
            ('Nunca', 'Nunca'),
    ])
      comunicacion = models.CharField(max_length=2, choices=[
        ('Si', 'Sí'),
        ('No', 'No'),
    ])
      def __str__(self):
        return f"Datos de personalidad {self.idEstudiante.noControl}"

