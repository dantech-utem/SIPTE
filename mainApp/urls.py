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
    path('test/', inicio.as_view(), name="test"),
    path('prueba2/', login_required(prueba2.as_view()), name='prueba2'),
    path('api/', include(router.urls)),  # Incluir las URLs del router aquí
    path('validar_email/', views.validar_email, name='validar_email'),
    path('login_sso/', views.login_sso, name='login_sso'),
    path('logout/', logout_view, name='logout'),  # No necesitas `views.` aquí
    path('validate_token/', views.validate_token, name='validate_token'),  # Nueva ruta para validar el token


    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)