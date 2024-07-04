from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from rest_framework import serializers, viewsets
from .models import Usuarios
import jwt
import datetime
from django.conf import settings

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['token']

class TokenViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = TokenSerializer

# Create your views here.
class inicio(View):
   def get(self, request):
        return render(request, 'login.html')

class prueba2(View):
   def get(self, request):
        return render(request, 'test/prueba2.html')
    
def validar_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    return JsonResponse({}, status=400)

def login_sso(request):
    if request.method == 'POST':
        email = request.POST.get('email2')
        password = request.POST.get('pswd')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'Error': 'Correo electrónico no registrado', 'Email': email})

        user_authenticated = authenticate(request, username=user.username, password=password)

        if user_authenticated is not None:
            login(request, user_authenticated)
            
            # Crear token JWT
            payload = {
                'user_id': user_authenticated.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            # Guardar el token en la base de datos
            try:
                usuario = Usuarios.objects.get(User=user_authenticated)
                usuario.token = token
                usuario.save()
            except Usuarios.DoesNotExist:
                return render(request, 'login.html', {'Error': 'Usuario no registrado en la tabla Usuarios', 'Email': email})

            # Establecer una cookie con el token
            response = redirect(reverse('prueba2'))
            response.set_cookie('sso_token', token, httponly=False)  # httponly=False para que sea accesible por JavaScript
            return response
        else:
            return render(request, 'login.html', {'Error': 'Credenciales incorrectas', 'Email': email})

    return render(request, 'login.html')

def logout_view(request):
    # Eliminar el token del localStorage en el cliente (JavaScript)
    response = redirect('inicio')  # Ajusta 'login' a la URL de tu página de inicio de sesión
    response.delete_cookie('sso_token')
    
    # Eliminar el token de la base de datos
    if request.user.is_authenticated:
        try:
            usuario = Usuarios.objects.get(User=request.user)
            usuario.token = None  # O elimina el token de la base de datos según tu modelo
            usuario.save()
        except Usuarios.DoesNotExist:
            pass  # Maneja la excepción según sea necesario
        
    logout(request)
    return response

def validate_token(request):
    if request.method == 'POST':
        token = request.POST.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            exp = payload['exp']

            # Verificar si el usuario y el token existen y son válidos
            try:
                usuario = Usuarios.objects.get(User__id=user_id, token=token)
                # Verificar si el token JWT no ha expirado
                if exp > datetime.datetime.utcnow().timestamp():
                    print("Entro")
                    user_id = payload.get('user_id')
                    user = User.objects.get(pk=user_id)
                    return JsonResponse({'valid': True})
                else:
                    logout(request)
                    return JsonResponse({'valid': False})
            except Usuarios.DoesNotExist:
                logout(request)
                return JsonResponse({'valid': False})

        except jwt.ExpiredSignatureError:
            logout(request)
            return JsonResponse({'valid': False, 'error': 'Token expirado'})
        except jwt.DecodeError:
            logout(request)
            return JsonResponse({'valid': False, 'error': 'Token inválido'})

    return JsonResponse({'error': 'Método no permitido'}, status=405)