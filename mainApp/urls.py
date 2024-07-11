from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainApp.views import *
from . import views

urlpatterns = [
    path('', inicio.as_view(), name="inicio"),
    path('test/', loginTest.as_view(), name="test"),
    path('aviso/', aviso.as_view(), name="aviso"), #Url de aviso alumno
    path('formulario/', formulario.as_view(), name="formulario"),
    path('resumenresp/', resumenresp.as_view(), name="resumenresp"),
    path('index/', index.as_view(), name="index"), #Url de aviso admin
    path('registro/', registro.as_view(), name="registro"),
    path('informe/', informe.as_view(), name="informe"),
    path('registrarAviso/', views.registrarAviso, name="registrarAviso"),
    path('edicionAviso/<int:idAvisos>', views.edicionAviso, name="edicionAviso"),
    path('editarAviso/', views.editarAviso),
    path('eliminarAviso/<int:idAvisos>', views.eliminarAviso, name="eliminarAviso"),
  
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)