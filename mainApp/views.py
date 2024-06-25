from django.shortcuts import render
from django.views import View

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
   
class canalizacionBajas(View):
   def get(self, request):
      return render(request,'Canalizacion/formBaja.html')
   
class canalizacionFormCanalizar(View):
   def get(self, request):
      return render(request,'Canalizacion/formCanalizar.html')
   
class canalizacionFormCerrarTutorias(View):
   def get(self, request):
      return render(request,'Canalizacion/formCerrarTutorias.html')
   
class canalizacionReportes(View):
   def get(self, request):
      return render(request,'Canalizacion/reportes.html')
   
class canalizacionResultadosCanalizacion(View):
   def get(self, request):
      return render(request,'Canalizacion/resultadosCanalizacion.html')