from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from flask import Flask, send_file
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import requests
from openpyxl.drawing.image import Image
from io import BytesIO
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
    return redirect('actividadTutorial')

def agregarActividadTutorial(request):
    if request.method == 'POST':
        tema = request.POST.get('tema')
        objetivos = request.POST.get('objetivos')
        actividades = request.POST.get('actividades')
        recursos = request.POST.get('recursos')
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
    periodo_activo = Periodo.objects.filter(estado=True).first()
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudianteAtencion')
        asuntoTratar = request.POST.get('asuntoTratar')
        observaciones = request.POST.get('observaciones')
        
        # Crear la instancia de AtencionIndividual
        AtencionIndividual.objects.create(
            estudiante_id=estudiante_id,
            asuntoTratar=asuntoTratar,
            observaciones=observaciones,
            cicloAccion=periodo_activo
            
        )

        messages.success(request, '¡Atención individual registrada con éxito!')
        return redirect('atencionIndividual')

    # Filtrar estudiantes que pertenecen al grupo del tutor actual y que son de tipo 'estudiante'
    tutor = request.user
    estudiantes = Usuarios.objects.filter(tipo__tipo='estudiante', grupo=tutor.usuarios.grupo)
    
    return render(request, 'registrarAtencion.html', {'estudiantes': estudiantes})


def editarAtencionIndividual(request, id):
    atencion = get_object_or_404(AtencionIndividual, id=id)
    tutor = request.user
    estudiantes = Usuarios.objects.filter(tipo__tipo='estudiante', grupo=tutor.usuarios.grupo)
    
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudianteAtencion')
        atencion.estudiante_id = estudiante_id  
        atencion.asuntoTratar = request.POST.get('asuntoTratar')
        atencion.observaciones = request.POST.get('observaciones')
        atencion.save()

        messages.success(request, '¡Atención individual editada con éxito!')
        return redirect('editarAtencion', id=atencion.id)

    return render(request, 'editarAtencion.html', {'atencion': atencion, 'estudiantes': estudiantes})

def eliminarAtencionIndividual(request, id):
    atencion = get_object_or_404(AtencionIndividual, id=id)
    atencion.delete()
    messages.success(request, '¡Atención individual eliminada con éxito!')
    return redirect('atencionIndividual')




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
     
    periodo_activo = Periodo.objects.filter(estado=True).first()

    if not periodo_activo:
            messages.error(request, 'No hay un período activo disponible.')
            return render(request, 'evaluacionAcTutorial.html')

        # Verificar si el usuario ya ha contestado la encuesta para el período activo
    evaluacion_existente = EvaluacionTutor.objects.filter(
            estudiante=estudiante,
            cicloEvaluacion=periodo_activo
        ).exists()

    if evaluacion_existente:
            messages.error(request, 'Ya has contestado la encuesta previamente.')
            return render(request, 'evaluacionAcTutorial.html', {'nombre_maestro': nombre_maestro})
                   
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
            serviciosApoyo=request.POST.get('serviciosApoyo'),
            cicloEvaluacion=periodo_activo
        )
        if evaluacion_existente:
            messages.error(request, 'Ya has contestado la encuesta previamente.')
            return render(request, 'evaluacionAcTutorial.html', {'nombre_maestro': nombre_maestro})
        else:
            evaluacion.save()


        messages.success(request, '¡Encuesta guardada con éxito!')
        return render(request, 'evaluacionAcTutorial.html', {'nombre_maestro': nombre_maestro})

    # Si es un método GET o cualquier otro, simplemente renderizar el formulario
    return render(request, 'evaluacionAcTutorial.html', {'nombre_maestro': nombre_maestro})

#Codigo orientado a libreria openpyxl

def descargarXLSX(request):
    tutor = request.user
    usuario = Usuarios.objects.get(User=tutor)
    periodo_activo = Periodo.objects.filter(estado=True).first()
    actividad = AccionTutorial.objects.filter(tutor=tutor, cicloAccion=periodo_activo)

    wb = Workbook()
    ws = wb.active

    FuenteRemarcada = Font(bold = True)
    # Estilo de borde
    borde = Border(left=Side(border_style='thin', color='000000'),
                   right=Side(border_style='thin', color='000000'),
                   top=Side(border_style='thin', color='000000'),
                   bottom=Side(border_style='thin', color='000000'))
    
    ws['E5'] = 'Ciclo:'
    ws['E5'].font = FuenteRemarcada
    ws['E5'].border = borde
    if periodo_activo:
        ws['F5'] = f"{periodo_activo.periodo} {periodo_activo.anio}"
    else:
        ws['F5'] = "No hay periodo activo"
        
# Combinar celdas y establecer el valor de 'E1'
    ws.merge_cells('E1:F1')
    ws['E1'] = 'PLAN DE ACCIÓN TUTORIAL'
    ws['E1'].alignment = Alignment(horizontal='center', vertical='center')
    ws['E1'].font = FuenteRemarcada

    ws.merge_cells('A4:B4')
    ws['A4'] = 'Nombre del tutor:'
    ws.merge_cells('C4:E4')
    ws['C4'] = f"{tutor.first_name} {tutor.last_name}"

    # Set the group of the logged-in user in cell C5
    ws.merge_cells('A5:B5')
    ws['A5'] = 'Grupo tutorado:'
    ws['C5'] = usuario.grupo
    
    ws['A4'].font = FuenteRemarcada
    ws['A5'].font = FuenteRemarcada
    
    Atributos = ["No", "Tema", "Objetivos", "Actividades", "Recursos", "Evidencias"]

    for col in range(1, 7):
        cell = ws.cell(row=8, column=col)
        cell.value = Atributos[col - 1]
        cell.font = FuenteRemarcada

    # Llenar la columna "No" (Columna A)
    for row_num in range(9, 19):
        ws.cell(row=row_num, column=1).value = row_num - 8

    # Continuar llenando dinámicamente si hay más de 10 registros
    row_num = 9
    for idx, atencion in enumerate(actividad, start=1):
        if row_num > 18:
            break
        ws.cell(row=row_num, column=2).value = atencion.tema  # Columna Tema
        ws.cell(row=row_num, column=3).value = atencion.objetivos  # Columna Objetivos
        ws.cell(row=row_num, column=4).value = atencion.actividades  # Columna Actividades
        ws.cell(row=row_num, column=5).value = atencion.recursos  # Columna Recursos
        ws.cell(row=row_num, column=6).value = atencion.evidencias  # Columna Evidencias
        row_num += 1

    # Si hay más de 10 registros, continuar desde donde se quedó la numeración inicial
    if len(actividad) > 10:
        for idx, atencion in enumerate(actividad[10:], start=11):
            if row_num > 18:
                break
            ws.cell(row=row_num, column=1).value = idx
            ws.cell(row=row_num, column=2).value = atencion.tema  # Columna Tema
            ws.cell(row=row_num, column=3).value = atencion.objetivos  # Columna Objetivos
            ws.cell(row=row_num, column=4).value = atencion.actividades  # Columna Actividades
            ws.cell(row=row_num, column=5).value = atencion.recursos  # Columna Recursos
            ws.cell(row=row_num, column=6).value = atencion.evidencias  # Columna Evidencias
            row_num += 1
    
    # Insertar la imagen en la hoja de cálculo
    image_url = 'https://sic.cultura.gob.mx/images/62119'
    response = requests.get(image_url)
    image = Image(BytesIO(response.content))
    ws.add_image(image, 'A1')
    image.width = 130  # Ajusta este valor según sea necesario
    image.height = 60  # Ajusta este valor según sea necesario
    

    
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
