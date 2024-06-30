from django.shortcuts import render, get_object_or_404, redirect
from .models import Canalizacion, BajaAlumnos,Canalizar
from django.views import View
from django.views.decorators.http import require_http_methods

# Create your views here.
class inicio(View):
   def get(self, request):
        return render(request, 'login.html')
     
class loginTest(View):
   def get(self, request):
      return render(request,'test/prueba.html')
   
class canalizacionIndex(View):
   def get(self, request):
      return render(request,'Canalizacion/index.html')

class canalizacionCalendario(View):
   def get(self, request):
      return render(request,'Canalizacion/calendario.html')
   
class canalizacionCompletarSesion(View):
   def get(self, request):
      return render(request,'Canalizacion/completarSesion.html')
   
class canalizacionExpedientes(View):
   def get(self, request):
      return render(request,'Canalizacion/expediente.html')
   
   #CRUD BAJAS CANALIZACION
class canalizacionBajas(View):
   def get(self, request):
      return render(request,'Canalizacion/formBaja.html')
   
def canalizacionBajaAlumno(request):
   if request.method == "POST":
      tipo = request.POST['tipo']
      observaciones = request.POST['observaciones']
      motivo = request.POST['motivo']
      # Crear un nuevo registro en la base de datos
      Baja  = BajaAlumnos.objects.create(tipo=tipo, observaciones=observaciones, motivo=motivo)
      Baja.save()
      # Redirigir a una página de éxito o de lista después de la creación
      return redirect('Dashboard')
   #TERMINA CRUD BAJAS CANALIZACION
   
   #CRUD CANALIZAR CANALIZACION
class canalizacionFormCanalizar(View):
   def get(self, request):
      return render(request,'Canalizacion/formCanalizar.html')
   
def canalizacionFormCanalizarAlumno(request):
   if request.method == "POST":
      area = request.POST['area']
      observaciones = request.POST['observaciones']
      motivo = request.POST['motivo']
      # Crear un nuevo registro en la base de datos
      canalizacion  = Canalizar.objects.create(area=area, observaciones=observaciones, motivo=motivo)
      canalizacion.save()
      # Redirigir a una página de éxito o de lista después de la creación
      return redirect('Dashboard')
   #TERMINA CRUD CANALIZAR CANALIZACION
   
class canalizacionFormCerrarTutorias(View):
   def get(self, request):
      return render(request,'Canalizacion/formCerrarTutorias.html')
   
class canalizacionReportes(View):
   def get(self, request):
      return render(request,'Canalizacion/reportes.html')
   
class canalizacionResultadosCanalizacion(View):
   def get(self, request):
      return render(request,'Canalizacion/resultadosCanalizacion.html')