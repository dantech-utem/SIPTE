from audioop import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Aviso
from .models import Estudiante
from .models import *
from django.db import IntegrityError
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
     
class loginTest(View):
   def get(self, request): 
      return render(request,'test/prueba.html')
   
class aviso(View):
   def get(self, request):
      return render(request,'entrevistas/alumno/aviso.html')
   
class formulario(View):
   def get(self, request):
      return render(request,'entrevistas/alumno/formulario.html')
   
class resumenresp(View):
   def get(self, request):
      return render(request,'entrevistas/alumno/resumenresp.html')
   
class index(View):
   def get(self, request):
      avisos = Aviso.objects.all()
      return render(request,'entrevistas/administrador/index.html', {'avisos': avisos})
   
class registro(View):
   def get(self, request):
      return render(request,'entrevistas/administrador/registro.html')
   
class informe(View):
   def get(self, request):
      return render(request,'entrevistas/administrador/informe.html')
   
class ver(View):
   def get(self, request):
      return render(request,'entrevistas/administrador/ver.html')

#ENTREVISTAS
#ADMINISTRADOR
def registrarAviso(request):
   titulo=request.POST['titulo']
   descripcion=request.POST['descripcion']
   fechaInicio=request.POST['fechaInicio']
   fechaFin=request.POST['fechaFin']

   aviso = Aviso.objects.create(titulo=titulo, descripcion=descripcion, fechaInicio=fechaInicio,fechaFin=fechaFin)
   return redirect('index')

def edicionAviso(request, idAvisos):
    aviso = Aviso.objects.get(idAvisos=idAvisos)
    return render(request, "entrevistas/administrador/editar.html", {"aviso": aviso})

def editarAviso(request):
   idAvisos=request.POST['idAvisos']
   titulo = request.POST['titulo']
   descripcion=request.POST['descripcion']
   fechaInicio=request.POST['fechaInicio']
   fechaFin=request.POST['fechaFin']

   aviso = Aviso.objects.get(idAvisos = idAvisos)
   aviso.titulo = titulo
   aviso.descripcion = descripcion
   aviso.fechaInicio = fechaInicio
   aviso.fechaFin = fechaFin
   aviso.save()
   return redirect('index')

def eliminarAviso(request, idAvisos):
    aviso = Aviso.objects.get(idAvisos=idAvisos)
    aviso.delete()
    return redirect('index')

#ALUMNO
class aviso(View):
    def get(self, request):
        avisos = Aviso.objects.all()
        return render(request, "entrevistas/alumno/aviso.html", {'avisos': avisos})

class informe(View):
    def get(self, request):
        estudiantes = Estudiante.objects.all()
        return render(request, 'entrevistas/administrador/informe.html', {'estudiantes': estudiantes})

class resumenresp(View):
    def get(self, request, idEstudiante):
        estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
        datos_familiares = get_object_or_404(DatosFamiliares, idEstudiante=estudiante)
        datos_socioeconomicos = get_object_or_404(Socioeconomicos, idEstudiante=estudiante)
        datos_academicos = get_object_or_404(AntecedenteAcademico, idEstudiante=estudiante)
        datos_estudio = get_object_or_404(HabitosEstudio, idEstudiante=estudiante)
        datos_aficiones = get_object_or_404(DatosAficiones,idEstudiante=estudiante)
        datos_personalidad = get_object_or_404(DatosPersonalidad,idEstudiante=estudiante)
        datos_salud = get_object_or_404(DatosSalud,idEstudiante=estudiante)
        
        context = {
            'estudiante': estudiante,
            'datos_familiares': datos_familiares,
            'datos_socioeconomicos': datos_socioeconomicos,
            'datos_academicos': datos_academicos,
            'datos_estudio': datos_estudio,
            'datos_aficiones':datos_aficiones,
            'datos_personalidad':datos_personalidad,
            'datos_salud':datos_salud
        }
   
        return render(request, 'entrevistas/alumno/resumenresp.html', context)   


def crearEstudiante(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        carrera = request.POST.get('carrera')
        tutor = request.POST.get('tutor')
        grupo = request.POST.get('grupo')
        fechaR = request.POST.get('fechaR')
        nombre = request.POST.get('nombre')
        noControl = request.POST.get('noControl')
        telCasa = request.POST.get('telCasa')
        correo = request.POST.get('correo')
        telCelular = request.POST.get('telCelular')
        edad = request.POST.get('edad')


        # Crear el estudiante
        estudiante = Estudiante.objects.create(
            carrera=carrera,
            tutor=tutor,
            grupo=grupo,
            fechaR=fechaR,
            nombre=nombre,
            noControl=noControl,
            telCasa=telCasa,
            correo=correo,
            telCelular=telCelular,
            edad=edad
        )
        # Obtener los datos del familiares
        conviveCon = request.POST.get('conviveCon')
        otra_situacion = request.POST.get('otra_situacion')
        huerfano = request.POST.get('huerfano')
        huerfanoQuien = request.POST.get('huerfanoQuien')
        totalHermanos = request.POST.get('totalHermanos')
        lugarHermano = request.POST.get('lugarHermano')
        estadoCivil = request.POST.get('estadoCivil')

        _idestudiante = estudiante.idEstudiante
        # Crear los datos familiares asociados al estudiante encontrado
        datos_familiares = DatosFamiliares.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            conviveCon=conviveCon,
            otra_situacion=otra_situacion,
            huerfano=huerfano,
            huerfanoQuien=huerfanoQuien,
            totalHermanos=totalHermanos,
            lugarHermano=lugarHermano,
            estadoCivil=estadoCivil
        )

         # Obtener los datos socioeconomicos
        vivienda = request.POST.get('vivienda')
        tenencia = request.POST.get('tenencia')
        habitaciones = request.POST.get('habitaciones')
        vehiculos = request.POST.get('vehiculos')
        trabajoPapa = request.POST.get('trabajoPapa')
        trabajoextraPapa = request.POST.get('trabajoextraPapa')
        trabajoMama = request.POST.get('trabajoMama')
        trabajoextraMama = request.POST.get('trabajoextraMama')
        manutencion = request.POST.get('manutencion')
        trabajas = request.POST.get('trabajas')
        relacionCarrera = request.POST.get('relacionCarrera')
        ingresoFam = request.POST.get('ingresoFam')
        contribuyentes = request.POST.get('contribuyentes')
        dependientesIngresos = request.POST.get('dependientesIngresos')


        _idestudiante = estudiante.idEstudiante
        # Crear los datos socioeconomicos asociados al estudiante encontrado
        datos_socioeconomicos = Socioeconomicos.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            vivienda=vivienda,
            tenencia=tenencia,
            habitaciones=habitaciones,
            vehiculos=vehiculos,
            trabajoPapa=trabajoPapa,
            trabajoextraPapa=trabajoextraPapa,
            trabajoMama=trabajoMama,
            trabajoextraMama=trabajoextraMama,
            manutencion=manutencion,
            trabajas=trabajas,
            relacionCarrera=relacionCarrera,
            ingresoFam=ingresoFam,
            contribuyentes=contribuyentes,
            dependientesIngresos=dependientesIngresos
        )

         # Obtener los datos academicos
        bachillerato = request.POST.get('bachillerato')
        modalidad = request.POST.get('modalidad')
        duracion = request.POST.get('duracion')
        promedio = request.POST.get('promedio')
        rendimiento = request.POST.get('rendimiento')
        materiasFacil = request.POST.get('materiasFacil')
        materiasDificil = request.POST.get('materiasDificil')
        materiasExtras = request.POST.get('materiasExtras')
        cualesExtras = request.POST.get('cualesExtras')
        repAnio = request.POST.get('repAnio')
        nivelRep = request.POST.get('nivelRep')
        obstaculos = request.POST.get('obstaculos')


        _idestudiante = estudiante.idEstudiante
        # Crear los datos antencedentes academicos asociados al estudiante encontrado
        datos_academicos = AntecedenteAcademico.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            bachillerato=bachillerato,
            modalidad=modalidad,
            duracion=duracion,
            promedio=promedio,
            rendimiento=rendimiento,
            materiasFacil=materiasFacil,
            materiasDificil=materiasDificil,
            materiasExtras=materiasExtras,
            cualesExtras=cualesExtras,
            repAnio=repAnio,
            nivelRep=nivelRep,
            obstaculos=obstaculos
        )
         # Obtener los datos estudio
        gustoLectura = request.POST.get('gustoLectura')
        tipoLectura = request.POST.get('tipoLectura')
        sitioLectura = request.POST.get('sitioLectura')
        descripEstudio = request.POST.get('descripEstudio')
        horas = request.POST.get('horas')
        horario = request.POST.get('horario')
        musica = request.POST.get('musica')
        


        _idestudiante = estudiante.idEstudiante
        # Crear los datos habitos de estudio asociados al estudiante encontrado
        datos_estudio = HabitosEstudio.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            gustoLectura=gustoLectura,
            tipoLectura=tipoLectura,
            sitioLectura=sitioLectura,
            descripEstudio=descripEstudio,
            horas=horas,
            horario=horario,
            musica=musica
        )

         # Obtener los datos aficiones
        tiempoLibre = request.POST.get('tiempoLibre')
        horasLibre = request.POST.get('horasLibre')
   
  
        _idestudiante = estudiante.idEstudiante
        # Crear los datos aficiones asociados al estudiante encontrado
        datos_aficiones = DatosAficiones.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            tiempoLibre=tiempoLibre,
            horasLibre=horasLibre
        )

         # Obtener los datos salud
        estadoSalud = request.POST.get('estadoSalud')
        enfermedadGrave = request.POST.get('enfermedadGrave')
        tipoEnfermedad = request.POST.get('tipoEnfermedad')
        padecimientoCro = request.POST.get('padecimientoCro')
        tipoPadecimiento = request.POST.get('tipoPadecimiento')
        operaciones = request.POST.get('operaciones')
        causaOperacion = request.POST.get('causaOperacion')
        problemaSalud = request.POST.get('problemaSalud')
        condiciones = request.POST.get('condiciones')
        tipoCondiciones = request.POST.get('tipoCondiciones')
        comentario = request.POST.get('comentario')

        _idestudiante = estudiante.idEstudiante
        # Crear los datos salud asociados al estudiante encontrado
        datos_salud = DatosSalud.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            estadoSalud=estadoSalud,
            enfermedadGrave=enfermedadGrave,
            tipoEnfermedad=tipoEnfermedad,
            padecimientoCro=padecimientoCro,
            tipoPadecimiento=tipoPadecimiento,
            operaciones=operaciones,
            causaOperacion=causaOperacion,
            problemaSalud=problemaSalud,
            condiciones=condiciones,
            tipoCondiciones=tipoCondiciones,
            comentario=comentario

        )
         # Obtener los datos personalidad
        colaborasCasa = request.POST.get('colaborasCasa')
        colaboracion = request.POST.get('colaboracion')
        ambienteFamiliar = request.POST.get('ambienteFamiliar')
        hablaFamiliar = request.POST.get('hablaFamiliar')
        comunicacion = request.POST.get('comunicacion')

        _idestudiante = estudiante.idEstudiante
        # Crear los datos personalidad asociados al estudiante encontrado
        datos_personalidad = DatosPersonalidad.objects.create(
            idEstudiante= Estudiante.objects.get(idEstudiante = estudiante.idEstudiante),
            colaborasCasa=colaborasCasa,
            colaboracion=colaboracion,
            ambienteFamiliar=ambienteFamiliar,
            hablaFamiliar=hablaFamiliar,
            comunicacion=comunicacion,
        )

        return redirect('resumenresp', idEstudiante=estudiante.idEstudiante)
    

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
        try:
            canalizacion = Canalizacion.objects.filter(atencionIndividual__estudiante__User__id=id).order_by('-fecha').first()
            
            context = {
                'id': id,
                'datos': canalizacion
            }
        except Canalizacion.DoesNotExist:
            context = {
                'id': id,
            }
        
        return render(request, 'Canalizacion/completarSesion.html', context)

class viewCanalizacionCompletarSesion(View):
    def get(self, request, id):
        datos = get_object_or_404(Canalizacion, id=id)
        
        context = {
            'id': id,
            'datos': datos
        }
        
        return render(request, 'Canalizacion/viewCompletarSesion.html', context)
   
def canalizacionFormCompletarSesion(request, id):
    if request.method == "POST":
        datos = get_object_or_404(Canalizacion, id=id)
        
        if datos:

            datos.detalles = request.POST['detalles']
            datos.estadoCanalizados = 3
            datos.save()

            estudiante_id = datos.atencionIndividual.estudiante.User.id
            usuario = Usuarios.objects.get(User_id=estudiante_id)
            usuario.estado = 1
            usuario.save()

            return redirect('ResultadosCanalizacion')

    
class viewCanalizar(View):
    def get(self, request, id):
        datos = get_object_or_404(Canalizacion, id=id)
        
        context = {
            'id': id,
            'datos': datos
        }
        
        return render(request, 'Canalizacion/viewCanalizar.html', context)
   
class formCalendario(View):
   def get(self, request, id):
      return render(request,'Canalizacion/formCalendario.html', {'id': id})

def canalizacionFormCalendario(request, id):
    if request.method == "POST":
        datos = Canalizacion.objects.filter(id=id).first()

        datos.titulo = request.POST.get('titulo', datos.titulo)
        datos.descripcion = request.POST.get('descripcion', datos.descripcion)
        datos.FechaInicio = request.POST.get('fechaInicio', datos.FechaInicio)
        datos.FechaFinal = request.POST.get('fechaFinal', datos.FechaFinal)
        datos.estadoCanalizados = 2
        datos.save()

        return redirect('ResultadosCanalizacion')
   
class canalizacionBajas(View):
    def get(self, request, id):
        try:
            baja = BajaAlumnos.objects.get(estudiante__id=id)
            estudiante = Usuarios.objects.get(User__id=id)
            context = {
                'id': id,
                'baja': baja,
                'estudiante': estudiante
            }
        except BajaAlumnos.DoesNotExist:
            context = {
                'id': id,
            }
        
        return render(request, 'Canalizacion/formBaja.html', context)
   
def canalizacionBajaAlumno(request, id):
   if request.method == "POST":
      datos = Usuarios.objects.get(id = id)
      tipo = request.POST['tipo']
      observaciones = request.POST['observaciones']
      motivo = request.POST['motivo']
      cicloActual = Periodo.objects.filter(estado = True).first()

      Baja  = BajaAlumnos.objects.create(tipo=tipo, observaciones=observaciones, motivo=motivo, cicloAccion=cicloActual, estudiante=datos.User)

      datos.estado = 3
      datos.save()

      return redirect('Dashboard')
   
class canalizacionFormCanalizar(View):
    def get(self, request, id):
        try:
            atencion_individual = AtencionIndividual.objects.filter(estudiante__User__id=id).order_by('-fecha').first()

            canalizacion = Canalizacion.objects.filter(atencionIndividual=atencion_individual).first()
            
            context = {
                'id': id,
                'canalizacion': canalizacion,
                'atencion_individual': atencion_individual
            }
        except (AtencionIndividual.DoesNotExist, Canalizacion.DoesNotExist):
            context = {
                'id': id,
            }
        
        return render(request, 'Canalizacion/formCanalizar.html', context)
   
def canalizacionFormCanalizarAlumno(request, id):
    if request.method == "POST":
        
        atencion_individual = AtencionIndividual.objects.filter(estudiante__User__id=id).order_by('-fecha').first()

        area = request.POST.get('area')
        observaciones = request.POST.get('observaciones')
        motivo = request.POST.get('motivo')
        ciclo_actual = Periodo.objects.filter(estado=True).first()
        Canalizar = Canalizacion.objects.create(
            area=area,
            observaciones=observaciones,
            motivo=motivo,
            cicloAccion=ciclo_actual,
            atencionIndividual=atencion_individual,
            estadoCanalizados=1
        )
        
        usuario = atencion_individual.estudiante
        usuario.estado = 4
        usuario.save()
        
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
    def get(self, request, id):
        if request.GET.get('periodo_id'):
            return self.get_ajax_response(request, id)
        else:
            return self.get_page_response(request, id)

    def get_page_response(self, request, id):
        periodos = Periodo.objects.all().order_by('-id')
        alumno = Usuarios.objects.select_related('User').get(User_id=id)
        canalizaciones = Canalizacion.objects.filter(atencionIndividual__estudiante_id=id).select_related('atencionIndividual', 'atencionIndividual__estudiante')
        
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
        
        context = {
            'reportes_data': reportes_data,
            'periodos': periodos,
            'alumno': alumno,
            'alumno_id': id
        }
        
        return render(request, 'Canalizacion/reportes.html', context)
    
    def get_ajax_response(self, request, id):
        periodo_id = request.GET.get('periodo_id')
        
        if periodo_id:
            canalizaciones = Canalizacion.objects.filter(cicloAccion_id=periodo_id, atencionIndividual__estudiante_id=id).values(
                'area',
                'atencionIndividual__estudiante__User__first_name',
                'atencionIndividual__estudiante__User__last_name',
                'atencionIndividual__estudiante__noControl',
                'motivo',
                'observaciones',
                'detalles',
                'atencionIndividual__fecha'
            )
            
            reportes_data = list(canalizaciones)
            data = {'reportes_data': reportes_data}
            return JsonResponse(data)
        
        return JsonResponse({'error': 'Periodo no válido'}, status=400)
   
class canalizacionIndex(View):
   def get(self, request):
      tutor = request.user
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

    def get_page_response(self, request, id):
        periodos = Periodo.objects.all().order_by('-id')
        alumno = id
        
        # Obtener todas las atenciones individuales del alumno
        atencion_ids = AtencionIndividual.objects.filter(estudiante_id=alumno).values_list('id', flat=True)
        
        # Obtener todas las canalizaciones asociadas a esas atenciones individuales
        TablaExpedientes = Canalizacion.objects.filter(atencionIndividual_id__in=atencion_ids).annotate(
            observacionesIndividual=F('atencionIndividual__observaciones'),
            asuntoTratarIndividual=F('atencionIndividual__asuntoTratar'),
            fechaIndividual=F('atencionIndividual__fecha'),
        )
        
        # Obtener información del alumno
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
        periodo_id = request.GET.get('periodo_id')
        
        # Obtener todas las atenciones individuales del alumno para el periodo seleccionado
        atencion_ids = AtencionIndividual.objects.filter(estudiante_id=alumno).values_list('id', flat=True)
        
        # Filtrar las canalizaciones para el periodo y las atenciones individuales específicas
        if periodo_id:
            atenciones_individuales = Canalizacion.objects.filter(
                cicloAccion_id=periodo_id,
                atencionIndividual_id__in=atencion_ids
            ).values(
                'area',
                'atencionIndividual__observaciones',
                'atencionIndividual__asuntoTratar',
                'atencionIndividual__fecha'
            )
            
            canalizaciones = Canalizacion.objects.filter(
                cicloAccion_id=periodo_id,
                atencionIndividual_id__in=atencion_ids
            ).values(
                'area',
                'detalles',
                'fecha'
            )
            
            data = {
                'atenciones_individuales': list(atenciones_individuales),
                'canalizaciones': list(canalizaciones),
                'id': id
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
