from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainApp.views import *
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', inicio.as_view(), name="inicio"),
    path('test/', login_required(loginTest.as_view()), name="test"),
    path('validar_email/', views.validar_email, name='validar_email'),
    path('login_sso/', loginSSO.as_view(), name='login_sso'),
    path('logout/', views.logout_view, name='logout'),
    path('prueba2/', login_required(prueba2.as_view()), name='prueba2'),
    path('check-auth/', login_required(check_authentication), name='check_auth'),


    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)