from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainApp.views import *
from . import views

urlpatterns = [
    path('', inicio.as_view(), name="inicio"),
    path('test/', loginTest.as_view(), name="test"),
    path('aviso/', aviso.as_view(), name="aviso"),
    path('formulario/', formulario.as_view(), name="formulario"),
    path('resumenresp/', resumenresp.as_view(), name="resumenresp"),
    path('index/', index.as_view(), name="index"),
    path('registro/', registro.as_view(), name="registro"),
    path('editar/', editar.as_view(), name="editar"),
    path('informe/', informe.as_view(), name="informe"),
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)