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

def logout_view(request):
    logout(request)
    return render(request, 'login.html')
     
class loginTest(View):
   def get(self, request):
    

    return render(request,'test/prueba.html')
   
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
            user = authenticate(request, username=user, password=password)
            if user is not None:
                login(request, user)  # Iniciar sesión para el usuario autenticado
                username = request.user.first_name
                print(username)
                # Ejemplo de redirección después de iniciar sesión  
                return redirect(reverse('test'))
            else:
                error_message = 'Contraseña incorrectos.'
                return render(request, 'login.html', {'Error': error_message, 'Email': email})
        
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
