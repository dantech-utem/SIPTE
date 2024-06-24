from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

# Create your views here.
class inicio(View):
   def get(self, request):
        return render(request, 'login.html')
     
class loginTest(View):
   def get(self, request):
      return render(request,'test/prueba.html')
   
def actividadTutorial(request):
    return render(request, 'actividadTutorial.html')   

def agregarActividadTutorial(request):
    return render(request, 'agregarActividad.html')   

def editarActividadTutorial(request):
    return render(request, 'editarActividad.html')   

def infoActividadTutorial(request):
    return render(request, 'infoActividad.html')  

def infoEvaluarTutor(request):
    return render(request, 'evaluarTutor.html') 

def infoatencionIndividual(request):
    return render (request, 'atencionIndividual.html')

def infoeditarAtencion(request):
    return render (request,'editarAtencion.html')

def inforegistrarAtencion(request):
    return render (request, 'registrarAtencion.html')

def reportePlanAccion(request):
    return render (request, 'reporteAccion.html')
