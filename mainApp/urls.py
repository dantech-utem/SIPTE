from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainApp.views import *
from . import views

urlpatterns = [
    path('', inicio.as_view(), name="inicio"),
    path('test/', loginTest.as_view(), name="test"),
    path('Dashboard', canalizacionIndex.as_view(), name="Dashboard"),
    path('Calendario', canalizacionCalendario.as_view(), name="Calendario"),
    path('CompletarSesion', canalizacionCompletarSesion.as_view(), name="CompletarSesion"),
    path('Expediente', canalizacionExpedientes.as_view(), name="Expediente"),
    path('FormBaja', canalizacionBajas.as_view(), name="FormBaja"),
    path("canalizacionBajaAlumno/" , views.canalizacionBajaAlumno,name="canalizacionBajaAlumno"),
    path("canalizacionFormCanalizarAlumno/", views.canalizacionFormCanalizarAlumno, name ="canalizacionFormCanalizarAlumno"),
    path('FormCanalizar', canalizacionFormCanalizar.as_view(), name="FormCanalizar"),
    path('FormCerrarTutorias', canalizacionFormCerrarTutorias.as_view(), name="FormCerrarTutorias"),
    path('Reportes', canalizacionReportes.as_view(), name="Reportes"),
    path('ResultadosCanalizacion', canalizacionResultadosCanalizacion.as_view(), name="ResultadosCanalizacion"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)