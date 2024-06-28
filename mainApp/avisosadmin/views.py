from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
def index (request):
    return render(request,'index.html')

def registro (request):
    return render(request,'registro.html')

def editar (request):
    return render(request,'editar.html')

def informe(request):
    return render (request,'informe.html')