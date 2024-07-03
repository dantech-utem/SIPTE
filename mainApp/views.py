from django.shortcuts import render
from django.views import View

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
      return render(request,'entrevistas/administrador/index.html')
   
class registro(View):
   def get(self, request):
      return render(request,'entrevistas/administrador/registro.html')
   
class editar(View):
   def get(self, request):
      return render(request,'entrevistas/administrador/editar.html')
   
class informe(View):
   def get(self, request):
      return render(request,'entrevistas/administrador/informe.html')
