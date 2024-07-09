from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainApp.views import *
from . import views

urlpatterns = [
    path('', inicio.as_view(), name="inicio"),
    path('test/', loginTest.as_view(), name="test"),
    path('actividadTutorial', views.actividadTutorial, name="actividadTutorial"),
    path('agregarActividad', views.agregarActividadTutorial, name='agregarActividad'),
    path('editarActividad/<int:id>/', views.editarActividadTutorial, name='editarActividad'),
    path('infoActividad/<int:id>/', views.infoActividadTutorial, name='infoActividad'),
    path('eliminarActividad/<int:id>/', views.eliminarActividadTutorial, name='eliminarActividad'),
    path('atencionIndividual/', views.infoatencionIndividual, name='atencionIndividual'),
    path('atencionIndividual/agregar/', views.agregarAtencionIndividual, name='registrarAtencion'),
    path('atencionIndividual/editar/<int:id>/', views.editarAtencionIndividual, name='editarAtencion'),
    path('atencionIndividual/eliminar/<int:id>/', views.eliminarAtencionIndividual, name='eliminarAtencionIndividual'),
    path('reportePlanAccion', views.reportePlanAccion, name='reportePlanAccion'),
    path('informePlanAccion', views.informePlanAccion, name='informePlanAccion'),
    path('descarga', views.descargarXLSX, name='descarga'),
    path('XLSXReportePlanAccion', views.descargarReporte, name='XLSXReporte'),
    path('evaluacionAcTutorial', views.evaluacionAcTutorial, name='Evaluacion')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
