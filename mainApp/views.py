from audioop import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Aviso
from .models import Estudiante
from .models import *
from django.db import IntegrityError

# Create your views here.
class inicio(View):
   def get(self, request):
        return render(request, 'login.html')
     
class loginTest(View):
   def get(self, request): 
      return render(request,'test/prueba.html')
   
class aviso(View):
   def get(self, request):
      return render(request,'entrevistas/alumno/aviso.html')
   
class formulario(View):
   def get(self, request):
      return render(request,'entrevistas/alumno/formulario.html')
   
class resumenresp(View):
   def get(self, request):
      return render(request,'entrevistas/alumno/resumenresp.html')
   
class index(View):
   def get(self, request):
      avisos = Aviso.objects.all()
      return render(request,'entrevistas/administrador/index.html', {'avisos': avisos})
   
class registro(View):
   def get(self, request):
      return render(request,'entrevistas/administrador/registro.html')
   
class informe(View):
   def get(self, request):
      return render(request,'entrevistas/administrador/informe.html')

#ADMINISTRADOR
def registrarAviso(request):
   titulo=request.POST['titulo']
   descripcion=request.POST['descripcion']
   fechaInicio=request.POST['fechaInicio']
   fechaFin=request.POST['fechaFin']

   aviso = Aviso.objects.create(titulo=titulo, descripcion=descripcion, fechaInicio=fechaInicio,fechaFin=fechaFin)
   return redirect('index')

def edicionAviso(request, idAvisos):
    aviso = Aviso.objects.get(idAvisos=idAvisos)
    return render(request, "entrevistas/administrador/editar.html", {"aviso": aviso})

def editarAviso(request):
   idAvisos=request.POST['idAvisos']
   titulo = request.POST['titulo']
   descripcion=request.POST['descripcion']
   fechaInicio=request.POST['fechaInicio']
   fechaFin=request.POST['fechaFin']

   aviso = Aviso.objects.get(idAvisos = idAvisos)
   aviso.titulo = titulo
   aviso.descripcion = descripcion
   aviso.fechaInicio = fechaInicio
   aviso.fechaFin = fechaFin
   aviso.save()
   return redirect('index')

def eliminarAviso(request, idAvisos):
    aviso = Aviso.objects.get(idAvisos=idAvisos)
    aviso.delete()
    return redirect('index')

#ALUMNO
class aviso(View):
    def get(self, request):
        avisos = Aviso.objects.all()
        return render(request, "entrevistas/alumno/aviso.html", {'avisos': avisos})



class resumenresp(View):
    def get(self, request, idEstudiante):
        estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
        datos_familiares = get_object_or_404(DatosFamiliares, idEstudiante=estudiante)
        datos_socioeconomicos = get_object_or_404(Socioeconomicos, idEstudiante=estudiante)
        datos_academicos = get_object_or_404(AntecedenteAcademico, idEstudiante=estudiante)
        datos_estudio = get_object_or_404(HabitosEstudio, idEstudiante=estudiante)
        
        context = {
            'estudiante': estudiante,
            'datos_familiares': datos_familiares,
            'datos_socioeconomicos': datos_socioeconomicos,
            'datos_academicos': datos_academicos,
            'datos_estudio': datos_estudio,
        }
   
        return render(request, 'entrevistas/alumno/resumenresp.html', context)

 

def crearEstudiante(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        carrera = request.POST.get('carrera')
        tutor = request.POST.get('tutor')
        grupo = request.POST.get('grupo')
        fechaR = request.POST.get('fechaR')
        nombre = request.POST.get('nombre')
        noControl = request.POST.get('noControl')
        telCasa = request.POST.get('telCasa')
        correo = request.POST.get('correo')
        telCelular = request.POST.get('telCelular')
        edad = request.POST.get('edad')


        # Crear el estudiante
        estudiante = Estudiante.objects.create(
            carrera=carrera,
            tutor=tutor,
            grupo=grupo,
            fechaR=fechaR,
            nombre=nombre,
            noControl=noControl,
            telCasa=telCasa,
            correo=correo,
            telCelular=telCelular,
            edad=edad
        )

        conviveCon = request.POST.get('conviveCon')
        otra_situacion = request.POST.get('otra_situacion')
        huerfano = request.POST.get('huerfano')
        huerfanoQuien = request.POST.get('huerfanoQuien')
        totalHermanos = request.POST.get('totalHermanos')
        lugarHermano = request.POST.get('lugarHermano')
        estadoCivil = request.POST.get('estadoCivil')

        _idestudiante = estudiante.idEstudiante
        # Crear los datos familiares asociados al estudiante encontrado
        datos_familiares = DatosFamiliares.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            conviveCon=conviveCon,
            otra_situacion=otra_situacion,
            huerfano=huerfano,
            huerfanoQuien=huerfanoQuien,
            totalHermanos=totalHermanos,
            lugarHermano=lugarHermano,
            estadoCivil=estadoCivil
        )


        vivienda = request.POST.get('vivienda')
        tenencia = request.POST.get('tenencia')
        habitaciones = request.POST.get('habitaciones')
        vehiculos = request.POST.get('vehiculos')
        trabajoPapa = request.POST.get('trabajoPapa')
        trabajoextraPapa = request.POST.get('trabajoextraPapa')
        trabajoMama = request.POST.get('trabajoMama')
        trabajoextraMama = request.POST.get('trabajoextraMama')
        manutencion = request.POST.get('manutencion')
        trabajas = request.POST.get('trabajas')
        relacionCarrera = request.POST.get('relacionCarrera')
        ingresoFam = request.POST.get('ingresoFam')
        contribuyentes = request.POST.get('contribuyentes')
        dependientesIngresos = request.POST.get('dependientesIngresos')


        _idestudiante = estudiante.idEstudiante
        # Crear los datos socioeconomicos asociados al estudiante encontrado
        datos_socioeconomicos = Socioeconomicos.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            vivienda=vivienda,
            tenencia=tenencia,
            habitaciones=habitaciones,
            vehiculos=vehiculos,
            trabajoPapa=trabajoPapa,
            trabajoextraPapa=trabajoextraPapa,
            trabajoMama=trabajoMama,
            trabajoextraMama=trabajoextraMama,
            manutencion=manutencion,
            trabajas=trabajas,
            relacionCarrera=relacionCarrera,
            ingresoFam=ingresoFam,
            contribuyentes=contribuyentes,
            dependientesIngresos=dependientesIngresos
        )

        
        bachillerato = request.POST.get('bachillerato')
        modalidad = request.POST.get('modalidad')
        duracion = request.POST.get('duracion')
        promedio = request.POST.get('promedio')
        rendimiento = request.POST.get('rendimiento')
        materiasFacil = request.POST.get('materiasFacil')
        materiasDificil = request.POST.get('materiasDificil')
        materiasExtras = request.POST.get('materiasExtras')
        cualesExtras = request.POST.get('cualesExtras')
        repAnio = request.POST.get('repAnio')
        nivelRep = request.POST.get('nivelRep')
        obstaculos = request.POST.get('obstaculos')


        _idestudiante = estudiante.idEstudiante
        # Crear los datos antencedentes academicos asociados al estudiante encontrado
        datos_academicos = AntecedenteAcademico.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            bachillerato=bachillerato,
            modalidad=modalidad,
            duracion=duracion,
            promedio=promedio,
            rendimiento=rendimiento,
            materiasFacil=materiasFacil,
            materiasDificil=materiasDificil,
            materiasExtras=materiasExtras,
            cualesExtras=cualesExtras,
            repAnio=repAnio,
            nivelRep=nivelRep,
            obstaculos=obstaculos
        )

        gustoLectura = request.POST.get('gustoLectura')
        tipoLectura = request.POST.get('tipoLectura')
        sitioLectura = request.POST.get('sitioLectura')
        descripEstudio = request.POST.get('descripEstudio')
        horas = request.POST.get('horas')
        horario = request.POST.get('horario')
        musica = request.POST.get('musica')
        


        _idestudiante = estudiante.idEstudiante
        # Crear los datos habitos de estudio asociados al estudiante encontrado
        datos_estudio = HabitosEstudio.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            gustoLectura=gustoLectura,
            tipoLectura=tipoLectura,
            sitioLectura=sitioLectura,
            descripEstudio=descripEstudio,
            horas=horas,
            horario=horario,
            musica=musica
        )


        tiempoLibre = request.POST.get('tiempoLibre')
        horasLibre = request.POST.get('horasLibre')
   
  
        _idestudiante = estudiante.idEstudiante
        # Crear los datos aficiones asociados al estudiante encontrado
        datos_aficiones = DatosAficiones.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            tiempoLibre=tiempoLibre,
            horasLibre=horasLibre
        )


        estadoSalud = request.POST.get('estadoSalud')
        enfermedadGrave = request.POST.get('enfermedadGrave')
        tipoEnfermedad = request.POST.get('tipoEnfermedad')
        padecimientoCro = request.POST.get('padecimientoCro')
        tipoPadecimiento = request.POST.get('tipoPadecimiento')
        operaciones = request.POST.get('operaciones')
        causaOperacion = request.POST.get('causaOperacion')
        problemaSalud = request.POST.get('problemaSalud')
        condiciones = request.POST.get('condiciones')
        tipoCondiciones = request.POST.get('tipoCondiciones')
        comentario = request.POST.get('comentario')

        _idestudiante = estudiante.idEstudiante
        # Crear los datos aficiones asociados al estudiante encontrado
        datos_salud = DatosSalud.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            estadoSalud=estadoSalud,
            enfermedadGrave=enfermedadGrave,
            tipoEnfermedad=tipoEnfermedad,
            padecimientoCro=padecimientoCro,
            tipoPadecimiento=tipoPadecimiento,
            operaciones=operaciones,
            causaOperacion=causaOperacion,
            problemaSalud=problemaSalud,
            condiciones=condiciones,
            tipoCondiciones=tipoCondiciones,
            comentario=comentario

        )

        colaborasCasa = request.POST.get('colaborasCasa')
        colaboracion = request.POST.get('colaboracion')
        ambienteFamiliar = request.POST.get('ambienteFamiliar')
        hablaFamiliar = request.POST.get('hablaFamiliar')
        comunicacion = request.POST.get('comunicacion')

        _idestudiante = estudiante.idEstudiante
        # Crear los datos personalidad asociados al estudiante encontrado
        datos_personalidad = DatosPersonalidad.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            colaborasCasa=colaborasCasa,
            colaboracion=colaboracion,
            ambienteFamiliar=ambienteFamiliar,
            hablaFamiliar=hablaFamiliar,
            comunicacion=comunicacion,
        )

       
        return redirect('resumenresp', idEstudiante=estudiante.idEstudiante)
    