from django.shortcuts import render, redirect
from django.views import View
from .models import Aviso


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