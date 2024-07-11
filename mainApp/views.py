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


def crearEstudiante(request):
    print("antes del POST")
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

        print("Estamos imprimiendo una variable :" + carrera)

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

        print(estudiante)
        #id_estudiante = Estudiante.objects.get(id=estudiante.id)


        # Redirigir a la vista 'crearDatosFamiliares' con el idEstudiante como parámetro en la URL
        #return HttpResponseRedirect(reverse(crearDatosFamiliares,idEstudiante=estudiante.id))
        #return render(request,'crearDatosFamiliares/',idEstudiante=estudiante.id)
        return redirect('aviso')



def crearDatosFamiliares(request, _idEstudiante):
    if request.method == 'POST':
        idEstudiante = _idEstudiante
        conviveCon = request.POST.get('conviveCon')
        otra_situacion = request.POST.get('otra_situacion')
        huerfano = request.POST.get('huerfano')
        huerfanoQuien = request.POST.get('huerfanoQuien')
        totalHermanos = request.POST.get('totalHermanos')
        lugarHermano = request.POST.get('lugarHermano')
        estadoCivil = request.POST.get('estadoCivil')

        # Crear los datos familiares asociados al estudiante encontrado
        datos_familiares = DatosFamiliares.objects.create(
            idEstudiante=idEstudiante,
            conviveCon=conviveCon,
            otra_situacion=otra_situacion,
            huerfano=huerfano,
            huerfanoQuien=huerfanoQuien,
            totalHermanos=totalHermanos,
            lugarHermano=lugarHermano,
            estadoCivil=estadoCivil
        )

        # Redireccionar a la vista de resumen o donde corresponda
        return redirect('resumenresp')

    