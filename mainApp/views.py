from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.
class inicio(View):
   def get(self, request):
        return render(request, 'login.html')

class prueba2(View):
   def get(self, request):
        return render(request, 'test/prueba2.html')
    
def check_authentication(request):
    sso_token = request.COOKIES.get('sso_token')
    if sso_token and sso_token == request.user.get_session_auth_hash():
        return JsonResponse({'authenticated': True, 'username': request.user.first_name})
    else:
        return JsonResponse({'authenticated': False})
    
def logout_view(request):
    logout(request)
    return render(request, 'login.html')
     
class loginTest(View):
    def get(self, request):
        sso_token = request.COOKIES.get('sso_token')
        if sso_token and request.user.is_authenticated:
            return render(request, 'test/prueba.html', {'username': request.user.first_name})
        else:
            return redirect(reverse('login'))
   
def validar_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        try:
            user = User.objects.get(email=email)
            request.session['sso_email'] = email  # Guarda el email en la sesión
            return JsonResponse({'exists': True})
        except User.DoesNotExist:
            return JsonResponse({'exists': False})
    return JsonResponse({}, status=400)

class loginSSO(View):
    def post(self, request):
        try:
            email = request.POST.get('email')
            password = request.POST.get('pswd')
            user = User.objects.get(email=email)
            # Autenticar usuario usando correo electrónico
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)  # Iniciar sesión para el usuario autenticado
                username = request.user.first_name
                # Configurar una cookie para SSO
                response = redirect(reverse('test'))
                response.set_cookie('sso_token', user.get_session_auth_hash(), httponly=True)
                return response
            else:
                error_message = 'Contraseña incorrecta.'
                return render(request, 'login.html', {'Error': error_message, 'Email': email})
        except User.DoesNotExist:
            error_message = 'El correo electrónico no existe.'
            return render(request, 'login.html', {'Error': error_message})
        
        except Exception as e:
            # Imprimir excepción en consola para depuración
            print(f"Error de inicio de sesión: {str(e)}")
            # Devolver respuesta de error genérico al usuario
            return JsonResponse({'success': False, 'error': 'Error en el inicio de sesión.'})
        # if request.method == 'POST':
        #     email = request.POST.get('email', None)
        #     password = request.POST.get('pswd', None)
        #     user = User.objects.get(email=email)
        #     if user.check_password(password):
        #         # Aquí podrías implementar la lógica de inicio de sesión SSO
        #         # Guardar sesión, tokens, etc.
        #         return render(request,'test/prueba.html')
        #     else:
        #         return JsonResponse({'success': False, 'error': 'Contraseña incorrecta'})
        # return JsonResponse({}, status=400)
