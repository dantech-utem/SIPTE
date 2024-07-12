from django.views import View
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from rest_framework import serializers, viewsets
from .models import Usuarios
import jwt
import datetime
from django.conf import settings
from .models import Canalizacion, BajaAlumnos, AccionTutorial,Usuarios,AtencionIndividual,Periodo,CierreTutorias
from django.views import View
from django.views.decorators.http import require_http_methods
from django.db.models import Count, F, Value
from django.utils.timezone import make_aware
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

   
class canalizacionIndex(View):
   def get(self, request):
      return render(request,'Canalizacion/index.html')

class canalizacionCalendario(View):

   def get(self, request):
      #sacar area del usuario
        tipo = request.user.usuarios.tipo.tipo
        canalizaciones = 0
        canalizaciones_mes = 0

       
        end_of_today = make_aware(datetime.datetime.now()).replace(hour=23, minute=59, second=59, microsecond=999999)
        # Realizar el filtro con el rango de fechas
        #añadir filtro por grupo si es tutor
        if(tipo == 'tutor'):
            canalizaciones = Canalizacion.objects.filter(FechaInicio__isnull=False, FechaFinal__isnull=False)
            canalizaciones_mes = Canalizacion.objects.filter(
                FechaInicio__isnull=False, 
                FechaFinal__isnull=False,
                FechaInicio__lte=end_of_today
            ).order_by("FechaInicio")
        else:
            canalizaciones = Canalizacion.objects.filter(FechaInicio__isnull=False, FechaFinal__isnull=False,area=tipo)
            canalizaciones_mes = Canalizacion.objects.filter(
                FechaInicio__isnull=False, 
                FechaFinal__isnull=False,
                FechaInicio__lte=end_of_today,
                area=tipo
            ).order_by("FechaInicio")
        
        lista_canalizaciones = []
        # start: '2020-09-16T16:00:00'
        for canalizacion in canalizaciones:
            lista_canalizaciones.append({   
                'estudiante': {
                    'id': canalizacion.atencionIndividual.estudiante.User_id,
                    'nombre': canalizacion.atencionIndividual.estudiante.User.first_name,
                    'apellido': canalizacion.atencionIndividual.estudiante.User.last_name,
                    'correo': canalizacion.atencionIndividual.estudiante.User.email
                },
                'title': canalizacion.atencionIndividual.estudiante.User.first_name,
                'observaciones':canalizacion.observaciones,
                'motivo': canalizacion.motivo,
                'detalles': canalizacion.detalles,
                'fecha': canalizacion.fecha.strftime("%Y-%m-%dT%H:%M:%S"),
                'start': canalizacion.FechaInicio.strftime("%Y-%m-%dT%H:%M:%S"),
                'end': canalizacion.FechaFinal.strftime("%Y-%m-%dT%H:%M:%S")
                }
            )
        context = {'canalizaciones': lista_canalizaciones,'canalizaciones_mes': canalizaciones_mes}
        return render(request,'Canalizacion/calendario.html', context)
   
class canalizacionCompletarSesion(View):
   def get(self, request, id):
      
      context = {
          'id': id,
          'datos': Canalizacion.objects.get(id = id)
      }

      return render(request,'Canalizacion/completarSesion.html', context)
   
def canalizacionFormCompletarSesion(request, id):
    if request.method == "POST":
      
      datos = Canalizacion.objects.get(id = id)

      datos.detalles = request.POST['detalles']
      datos.estadoCanalizados = 3
      datos.save()

      return redirect('ResultadosCanalizacion')
    
class viewCanalizar(View):
    def get(self, request, id):
        context = {
          'id': id,
          'datos': Canalizacion.objects.get(id = id)
       }
        
        return render(request,'Canalizacion/viewCanalizar.html', context)
   
class formCalendario(View):
   def get(self, request, id):
      return render(request,'Canalizacion/formCalendario.html', {'id': id})

def canalizacionFormCalendario(request, id):
   if request.method == "POST":
      
      datos = Canalizacion.objects.get(id = id)

      datos.titulo = request.POST['titulo']
      datos.descripcion = request.POST['descripcion']
      datos.FechaInicio = request.POST['fechaInicio']
      datos.FechaFinal = request.POST['fechaFinal']
      datos.estadoCanalizados = 2
      datos.save()

      return redirect('ResultadosCanalizacion')
   
class canalizacionBajas(View):
   def get(self, request):
      return render(request,'Canalizacion/formBaja.html')
   
def canalizacionBajaAlumno(request):
   if request.method == "POST":
      tipo = request.POST['tipo']
      observaciones = request.POST['observaciones']
      motivo = request.POST['motivo']
      cicloActual = Periodo.objects.filter(estado = True)
      Baja  = BajaAlumnos.objects.create(tipo=tipo, observaciones=observaciones, motivo=motivo, cicloAccion=cicloActual)
      Baja.save()
      return redirect('Dashboard')
   
class canalizacionFormCanalizar(View):
   def get(self, request):
      return render(request,'Canalizacion/formCanalizar.html')
   
def canalizacionFormCanalizarAlumno(request):
   if request.method == "POST":
      area = request.POST['area']
      observaciones = request.POST['observaciones']
      motivo = request.POST['motivo']
      cicloActual = Periodo.objects.filter(estado = True)
      Canalizar  = Canalizacion.objects.create(area=area, observaciones=observaciones, motivo=motivo, cicloAccion=cicloActual)
      Canalizar.save()
      return redirect('Dashboard')
   
class canalizacionFormCerrarTutorias(View):
   def get(self, request):
      return render(request,'Canalizacion/formCerrarTutorias.html')

def cerrarTurorias(request):
   if request.method == "POST":
      cierreTutorias = request.POST['cierreTutorias']
      cicloActual = Periodo.objects.filter(estado = True)
      userActual = request.user
      cierre  = CierreTutorias.objects.create(cierreTutorias=cierreTutorias, cicloAccion=cicloActual[0], tutor=userActual)
      cierre.save()
      return redirect('Dashboard')
     
     
class canalizacionReportes(View):
    def get(self, request):
        canalizaciones = Canalizacion.objects.all().select_related('atencionIndividual', 'atencionIndividual__estudiante')
        
        reportes_data = []
        for canalizacion in canalizaciones:
            reportes_data.append({
                'area': canalizacion.area,
                'nombre': canalizacion.atencionIndividual.estudiante.User.first_name,
                'apellidos': canalizacion.atencionIndividual.estudiante.User.last_name,
                'no_control': canalizacion.atencionIndividual.estudiante.noControl,
                'asunto_atencion': canalizacion.motivo,
                'observaciones': canalizacion.observaciones,
                'detalles': canalizacion.detalles,
                'fecha': canalizacion.atencionIndividual.fecha,
            })
        
        context = {'reportes_data': reportes_data}
        
        return render(request, 'Canalizacion/reportes.html', context)
   
class canalizacionIndex(View):
   def get(self, request):
      tutor = request.user
      print("datos del tutor",tutor)
      estudiantes = Usuarios.objects.filter(tipo__tipo='estudiante', grupo=tutor.usuarios.grupo)
      periodo = Periodo.objects.filter(estado=1)
      context = {
         'TablaViews': estudiantes,
         'Periodo': periodo

      } 
      return render(request, 'Canalizacion/index.html', context)
   
  
class canalizacionExpedientes(View):
    def get(self, request, id):
        if request.GET.get('periodo_id'):
            return self.get_ajax_response(request, id)
        else:
            return self.get_page_response(request, id)
        # if request.GET.get('alumno'):
            
        # else:
        #     return redirect('Dashboard')
    def get_page_response(self, request, id):
        periodos = Periodo.objects.all().order_by('-id')
        alumno = id
        #filtro por que manu te envia el usuario pero tu tienes que obtener mediante la atencion individual
        atencion_ids = AtencionIndividual.objects.filter(estudiante_id=alumno).values_list('id', flat=True).first()
        TablaExpedientes = Canalizacion.objects.filter(atencionIndividual_id=atencion_ids).annotate(
            observacionesIndividual = F('atencionIndividual__observaciones'),
            asuntoTratarIndividual = F('atencionIndividual__asuntoTratar'),
            fechaIndividual = F('atencionIndividual__fecha'),
            
        )
        alumno_exp = Usuarios.objects.filter(User_id=alumno)
        context = {
            'periodos': periodos,
            'TablaExpedientes': TablaExpedientes,
            'alumno': alumno_exp,
            'alumno_id': alumno,
            'id': id
        }
        return render(request, 'Canalizacion/expediente.html', context)
    
    def get_ajax_response(self, request, id):
        alumno = request.GET.get('alumno')
        periodo_id = request.GET.get('periodo_id')  # Obtener el periodo_id del formulario
        atencion_ids = AtencionIndividual.objects.filter(estudiante_id=alumno).values_list('id', flat=True).first()
        if periodo_id:
            atenciones_individuales = Canalizacion.objects.filter(cicloAccion_id=periodo_id,atencionIndividual_id=atencion_ids).values(
                'area', 
                'atencionIndividual__observaciones', 
                'atencionIndividual__asuntoTratar', 
                'atencionIndividual__fecha'
            )
            canalizaciones = Canalizacion.objects.filter(cicloAccion_id=periodo_id,atencionIndividual_id=atencion_ids).values(
                'area', 
                'detalles', 
                'fecha'
            )
            data = {
                'atenciones_individuales': list(atenciones_individuales),
                'canalizaciones': list(canalizaciones),
                'id':id
            }
            return JsonResponse(data)
        
        return JsonResponse({'error': 'Periodo no válido'}, status=400)

class canalizacionResultadosCanalizacion(View):
   def get(self, request):
      user = request.user.usuarios.tipo.tipo

      areas = {'psicologo':'Psicólogia', 'pedagogo':'Pedagogía', 'becas':'Becas', 'enfermeria':'Enfermería', 'incubadora':'Incubadora', 'bolsadetrabajo':'Bolsa de trabajo', 'asesoracademico':'Asesor académico'}

      print('test: ', areas[user])

      tabla = Canalizacion.objects.select_related('atencionIndividual').filter(area=areas[user])
      context = {
         'TablaResultados': tabla,
      }
      return render(request,'Canalizacion/resultadosCanalizacion.html', context)