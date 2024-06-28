from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def aviso (request):
    return render(request,'aviso.html')

def formulario (request):
    return render(request,'formulario.html')

def resumenresp (request):
    return render(request,'resumenresp.html')