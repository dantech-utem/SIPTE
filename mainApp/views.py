from django.shortcuts import render, redirect
from django.views import View
from .models import Aviso
from .models import Estudiante
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
    
def formularioEstudiante(request):
    if request.method == 'POST':
        noControl = request.POST.get('noControl')
        nombre = request.POST.get('nombre')
        carrera = request.POST.get('carrera')
        tutor = request.POST.get('tutor')
        grupo = request.POST.get('grupo')
        fechaR = request.POST.get('fechaR')
        telCasa = request.POST.get('telCasa')
        correo = request.POST.get('correo')
        telCelular = request.POST.get('telCelular')
        edad = request.POST.get('edad')

        try:
            estudiante = Estudiante.objects.create(
                noControl=noControl,
                nombre=nombre,
                carrera=carrera,
                tutor=tutor,
                grupo=grupo,
                fechaR=fechaR,
                telCasa=telCasa,
                correo=correo,
                telCelular=telCelular,
                edad=edad
            )
            estudiante.save()
            # Redireccionar a alguna página de éxito
            return redirect('resumenresp')
        except IntegrityError:
            # Manejar el error de unicidad
            return render(request, "entrevistas/alumno/formulario.html", {
                'error_message': 'El correo ya está registrado. Por favor, use otro correo.'
            })

    return render(request, "entrevistas/alumno/formulario.html") 

