from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainApp.views import *
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tokens', TokenViewSet, basename='token')

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
    path('crearEstudiante/', views.crearEstudiante, name="crearEstudiante"),
    path('resumenresp/<int:idEstudiante>/',resumenresp.as_view(), name='resumenresp'),

    
    path('test/', inicio.as_view(), name="test"),
    path('prueba2/', login_required(prueba2.as_view()), name='prueba2'),
    path('api/', include(router.urls)),  # Incluir las URLs del router aquí
    path('validar_email/', views.validar_email, name='validar_email'),
    path('login_sso/', views.login_sso, name='login_sso'),
    path('logout/', logout_view, name='logout'),  # No necesitas `views.` aquí
    path('validate_token/', views.validate_token, name='validate_token'),  # Nueva ruta para validar el token

    path('Dashboard', canalizacionIndex.as_view(), name="Dashboard"),
    path('Calendario', canalizacionCalendario.as_view(), name="Calendario"),
    path('CompletarSesion/<int:id>/', canalizacionCompletarSesion.as_view(), name="CompletarSesion"),
    path("canalizacionFormCompletarSesion/<int:id>", views.canalizacionFormCompletarSesion, name ="canalizacionFormCompletarSesion"),
    path('viewCanalizar/<int:id>/', viewCanalizar.as_view(), name="viewCanalizar"),
    path('formCalendario/<int:id>/', formCalendario.as_view(), name="formCalendario"),
    path("canalizacionFormCalendario/<int:id>", views.canalizacionFormCalendario, name ="canalizacionFormCalendario"),
    path('Expediente/<int:id>/', canalizacionExpedientes.as_view(), name="Expediente"),
    path('FormBaja', canalizacionBajas.as_view(), name="FormBaja"),
    path("canalizacionBajaAlumno/" , views.canalizacionBajaAlumno,name="canalizacionBajaAlumno"),
    path("canalizacionFormCanalizarAlumno/", views.canalizacionFormCanalizarAlumno, name ="canalizacionFormCanalizarAlumno"),
    path('FormCanalizar', canalizacionFormCanalizar.as_view(), name="FormCanalizar"),
    path('FormCerrarTutorias', canalizacionFormCerrarTutorias.as_view(), name="FormCerrarTutorias"),
    path('Reportes/<int:id>/', canalizacionReportes.as_view(), name="Reportes"),
    path('ResultadosCanalizacion', canalizacionResultadosCanalizacion.as_view(), name="ResultadosCanalizacion"),
    path("cerrarTurorias/" , views.cerrarTurorias,name="cerrarTurorias"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)