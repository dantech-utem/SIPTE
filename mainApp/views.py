from django.shortcuts import render, get_object_or_404, redirect
from .models import Canalizacion, BajaAlumnos, AccionTutorial,Usuarios,AtencionIndividual
from django.views import View
from django.views.decorators.http import require_http_methods
from datetime import datetime

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
      #sacar area del usuario
      canalizaciones = Canalizacion.objects.filter(FechaInicio__isnull=False, FechaFinal__isnull=False)
      canalizaciones_mes = Canalizacion.objects.filter(
            FechaInicio__isnull=False, 
            FechaFinal__isnull=False,
            FechaInicio__gte=datetime.now().date()
        ).order_by("FechaInicio")
      
      lista_canalizaciones = []
      # start: '2020-09-16T16:00:00'
      for canalizacion in canalizaciones:
         lista_canalizaciones.append({   
               "atencionIndividual": canalizacion.atencionIndividual,
               "observaciones": canalizacion.observaciones,
               "motivo": canalizacion.motivo,
               "detalles": canalizacion.detalles,
               "fecha": canalizacion.fecha,
               "FechaInicio": canalizacion.FechaInicio.strftime("%Y-%m-%dT%H:%M:%S"),
               "FechaFinal": canalizacion.FechaFinal.strftime("%Y-%m-%dT%H:%M:%S")
            }
         )
        
      context = {"canalizaciones": lista_canalizaciones,"canalizaciones_mes": canalizaciones_mes}
      return render(request,'Canalizacion/calendario.html', context)
   
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
      Baja  = BajaAlumnos.objects.create(tipo=tipo, observaciones=observaciones, motivo=motivo)
      Baja.save()
      return redirect('Dashboard')
   
class canalizacionFormCanalizar(View):
   def get(self, request):
      return render(request,'Canalizacion/formCanalizar.html')
   
def canalizacionFormCanalizarAlumno(request):
   if request.method == "POST":
      area = request.POST['area']
      observaciones = request.POST['observaciones']
      motivo = request.POST['motivo']
      Canalizar  = Canalizacion.objects.create(area=area, observaciones=observaciones, motivo=motivo)
      Canalizar.save()
      return redirect('Dashboard')
   
class canalizacionFormCerrarTutorias(View):
   def get(self, request):
      return render(request,'Canalizacion/formCerrarTutorias.html')
   
def cerrarTurorias(request):
   if request.method == "POST":
      cierreTutorias = request.POST['cierreTutorias']
      cierre  = AccionTutorial.objects.create(cierreTutorias=cierreTutorias)
      cierre.save()
      return redirect('Dashboard')
     
     
class canalizacionReportes(View):
   def get(self, request):
      return render(request,'Canalizacion/reportes.html')
   
class canalizacionResultadosCanalizacion(View):
   def get(self, request):
      return render(request,'Canalizacion/resultadosCanalizacion.html')

class canalizacion_view(View):
   def get(request):
      TablaDashboard = Usuarios.objects.all()
      context = {
         'TablaDashboard': TablaDashboard
      } 
      return render(request, 'Dashboard', context)