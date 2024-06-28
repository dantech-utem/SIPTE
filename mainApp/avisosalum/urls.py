from django.urls import path
from . import views

urlpatterns = [
    path ('aviso/',views.aviso, name="aviso"),
    path ('formulario/',views.formulario, name="formulario"),
    path ('resumenresp/',views.resumenresp, name="resumenresp"),
]
