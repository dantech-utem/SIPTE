from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from openpyxl import Workbook, load_workbook
from flask import Flask, send_file
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

from .models import Periodo, AccionTutorial, AtencionIndividual, Usuarios, EvaluacionTutor
from django.contrib import messages #Importamos para presentar mensajes
# Create your views here.
class inicio(View):
   def get(self, request):
        return render(request, 'login.html')
     
class loginTest(View):
   def get(self, request):
      return render(request,'test/prueba.html')
   
def actividadTutorial(request):
    actividades = AccionTutorial.objects.filter(cicloAccion__estado=True, tutor=request.user)
    messages.success(request, '¡Datos cargados!')
    return render(request, 'actividadTutorial.html', {"actividades":actividades})   


def eliminarActividadTutorial(request,id):
    actividad = get_object_or_404(AccionTutorial, id=id)
    actividad.delete()
    messages.success(request, '¡Actividad eliminada!')
    return render(request, 'actividadTutorial.html')  

def agregarActividadTutorial(request):
    if request.method == 'POST':
        tema = request.POST.get('tema')
        objetivos = request.POST.get('objetivos')
        actividades = request.POST.get('actividades')
        recursos = request.POST.get('recursos')
        cierreTutorias = request.POST.get('cierreTutorias')
        evidencias = request.POST.get('evidencias')

        # Obtén el único Periodo con estado=True
        try:
            cicloAccion = Periodo.objects.get(estado=True)
        except Periodo.DoesNotExist:
            return HttpResponse("Error: No hay un periodo activo.")

        # Obtén el usuario logueado como tutor
        tutor = request.user

        # Crea una nueva instancia de AccionTutorial y guárdala
        nueva_accion = AccionTutorial(
            tema=tema,
            objetivos=objetivos,
            actividades=actividades,
            recursos=recursos,
            cierreTutorias=cierreTutorias,
            cicloAccion=cicloAccion,
            evidencias = evidencias,
            tutor = tutor
        )
        nueva_accion.save()
        messages.success(request, '¡Guardado con éxito!')
        return redirect('actividadTutorial')  # Redirige a la página de actividades después de guardar

    return render(request, 'agregarActividad.html')  

def editarActividadTutorial(request, id):
    actividad = get_object_or_404(AccionTutorial, id=id)

    if request.method == 'POST':
        # Procesar el formulario enviado
        actividad.tema = request.POST.get('tema')
        actividad.objetivos = request.POST.get('objetivos')
        actividad.recursos = request.POST.get('recursos')
        actividad.actividades = request.POST.get('actividades')
        actividad.evidencias = request.POST.get('evidencias')
        actividad.save()

        messages.success(request, '¡Guardado con éxito!')
        return redirect('editarActividad', id=actividad.id)

    # Si es un GET, simplemente renderiza el formulario
    return render(request, 'editarActividad.html', {'actividad': actividad})

def infoActividadTutorial(request, id):
    actividad = get_object_or_404(AccionTutorial, cicloAccion__estado=True, tutor=request.user, id=id)
    return render(request,'infoActividad.html', {"actividad":actividad})   

def infoatencionIndividual(request):
    atenciones = AtencionIndividual.objects.all()
    messages.success(request, '¡Datos cargados!')
    return render(request, 'atencionIndividual.html', {"atenciones": atenciones})

def agregarAtencionIndividual(request):
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante')
        asuntoTratar = request.POST.get('asuntoTratar')
        observaciones = request.POST.get('observaciones')
        

        # Crear la instancia de AtencionIndividual
        AtencionIndividual.objects.create(
            estudiante_id=estudiante_id,
            asuntoTratar=asuntoTratar,
            observaciones=observaciones,
        )

        messages.success(request, '¡Atención individual registrada con éxito!')
        return redirect('atencionIndividual')

    estudiantes = Usuarios.objects.all()
    return render(request, 'registrarAtencion.html', {'estudiantes': estudiantes})


def editarAtencionIndividual(request, id):
    atencion = get_object_or_404(AtencionIndividual, id=id)

    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante')
        atencion.estudiante_id = estudiante_id  
        atencion.asuntoTratar = request.POST.get('asuntoTratar')
        atencion.observaciones = request.POST.get('observaciones')
        atencion.save()

        messages.success(request, '¡Atención individual editada con éxito!')
        return redirect('editarAtencion', id=atencion.id)

    estudiantes = Usuarios.objects.all()
    return render(request, 'editarAtencion.html', {'atencion': atencion, 'estudiantes': estudiantes})

def eliminarAtencionIndividual(request, id):
    atencion = get_object_or_404(AtencionIndividual, id=id)
    atencion.delete()
    messages.success(request, '¡Atención individual eliminada con éxito!')
    return render(request, 'atencionIndividual.html')




def infoeditarAtencion(request):
    return render (request,'editarAtencion.html')

def inforegistrarAtencion(request):
    return render (request, 'registrarAtencion.html')

def informePlanAccion(request):
    return render (request, 'informePlanAccion.html')

def reportePlanAccion(request):
    return render (request, 'reportePlanAccion.html')

def evaluacionAcTutorial(request):
    nombre_maestro = None  # Inicializar la variable nombre_maestro
    estudiante = request.user
    grupo_estudiante = estudiante.usuarios.grupo

    maestro = Usuarios.objects.filter(
                tipo__tipo='tutor',  # Ajusta según tu modelo TipoUsuario
                grupo=grupo_estudiante
            ).first()

    if maestro:
                nombre_maestro = maestro.User.get_full_name()
    else:
                nombre_maestro = "Tutor no encontrado"  # Manejo de caso sin maestro
                
    if request.method == 'POST':
        # Guardar la evaluación del tutor
        evaluacion = EvaluacionTutor(
            estudiante=estudiante,
            puntualidad=request.POST.get('puntualidad'),
            proposito=request.POST.get('proposito'),
            planTrabajo=request.POST.get('planTrabajo'),
            temasPrevistos=request.POST.get('temasPrevistos'),
            temasInteres=request.POST.get('temasInteres'),
            disposicionTutor=request.POST.get('disposicionTutor'),
            cordialidad=request.POST.get('cordialidad'),
            orientacion=request.POST.get('orientacion'),
            dominio=request.POST.get('dominio'),
            impacto=request.POST.get('impacto'),
            serviciosApoyo=request.POST.get('serviciosApoyo')
            
        )
        evaluacion.save()


        messages.success(request, '¡Encuesta guardada con éxito!')
        return render(request, 'evaluacionAcTutorial.html', {'nombre_maestro': nombre_maestro})

    # Si es un método GET o cualquier otro, simplemente renderizar el formulario
    return render(request, 'evaluacionAcTutorial.html', {'nombre_maestro': nombre_maestro})

#Codigo orientado a libreria openpyxl

def descargarXLSX(request):

    wb = Workbook()
    ws = wb.active

    FuenteRemarcada = Font(bold = True)

    ws['E5'] = 'Ciclo:'
    ws['E1'] = 'Plan accion tutorial'
    
    Datos = ["Nombre del tutor:", "Grupo tutorado:"]

    for row in range(4, 6):
        ws[f'A{row}'].value = Datos[row - 4]    

    Atributos = ["No", "Tema", "Objetivos", "Actividades", "Recursos", "Evidencias"]

    for col in range(1, 7):
        cell = ws.cell(row=8, column=col)
        cell.value = Atributos[col - 1]
        cell.font = FuenteRemarcada

    for row in range(9, 19):
        ws[f'A{row}'].value = row - 8
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Libro.xlsx'
    wb.save(response)

    return response

def descargarReporte(request):
    wb = Workbook()
    ws = wb.active

    FuenteRemarcada = Font(bold = True)

    hilera1 = ['Programa', 'Realizada', 'Canalizada']
    for col in range(1, 4):
        cell = ws.cell(row=6, column=col)
        cell.value = hilera1[col - 1]
        cell.alignment = Alignment(horizontal='center', vertical='center', text_rotation=90)

    AreasCanalizacion = ['Psicologo', 'Pedagogo', 'Becas', 'Enfermeria', 'Incubadora', 'Bolsa de trabajo', 'Asesor Academico']
    for row in range(7, 15):
        ws[f'D{row}'].value = AreasCanalizacion[row - 8] 

    Motivos = ['No se cumplieron expectativas', 'Reprobacion', 'Problemas economicos', 'Dificultades para el transporte', 'Problemas de trabajo', 'Cambio de carrera', 'Incompatibilidad de horario', 'Faltas al reglamento', 'Cambio de residencia', 'Cambio de universidad', 'Problemas familiares', 'Problemas personales', 'Otras']
    for row in range(7, 21):
        ws[f'J{row}'].value = Motivos[row - 8]

    hilera2 = ['Cantidad', 'Tipo de baja']
    for col in range(11, 13):
        cell = ws.cell(row=6, column=col) 
        cell.value = hilera2[col - 11]
        cell.alignment = Alignment(horizontal='center', vertical='center', text_rotation=90)

    ws['A15'] = 'No programada'
    ws['A15'].alignment = Alignment(vertical='center', text_rotation=90)

    ws['D6'] = 'Areas de canalizacion'
    ws['D15'] = 'Asunto de atencion'

    ws['B15'] = 'Asunto de atencion'

    ws['C15'] = 'Cantidad'
    ws['C15'].alignment = Alignment(vertical='center', text_rotation=90)

    ws['D15'] = 'Observaciones'

    ws['J21'] = 'Dificultades para ejercer la tutoria'

    ws['G6'] = 'Cantidad'
    ws['G6'].alignment = Alignment(vertical='center', text_rotation=90)

    ws['H6'] = 'Resultado de la canalizacion'

    ws['I6'] = 'Total'
    ws['I6'].alignment = Alignment(vertical='center', text_rotation=90)


    ws['J6'] = 'Motivo de baja'

    ws['M6'] = 'Observaciones'    



    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Reporte.xlsx'
    wb.save(response)

    return response
