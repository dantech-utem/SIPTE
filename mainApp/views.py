from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from flask import Flask, send_file
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.drawing.image import Image
from io import BytesIO
import os
from django.conf import settings
from .models import Periodo, AccionTutorial, AtencionIndividual, Usuarios, EvaluacionTutor, Canalizacion
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
    tutor = request.user
    usuario = Usuarios.objects.get(User=tutor)
    grupo= usuario.grupo
    atenciones = AtencionIndividual.objects.filter(cicloAccion__estado=True, estudiante__grupo=grupo)
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



def descargarXLSX(request):
    tutor = request.user
    usuario = Usuarios.objects.get(User=tutor)
    periodo_activo = Periodo.objects.filter(estado=True).first()
    grupo= usuario.grupo
    atenciones= AtencionIndividual.objects.filter(cicloAccion__estado=True, estudiante__grupo=grupo) 
    actividad = AccionTutorial.objects.filter(tutor=tutor, cicloAccion=periodo_activo)
# Cargar el archivo base
    path_archivo_base = os.path.join(settings.BASE_DIR, 'mainApp', 'data', 'basePlanAccion.xlsx')
    # Cargar el archivo base
    wb = load_workbook(filename=path_archivo_base, read_only=False)
    ws = wb.active
    
    if periodo_activo:
        ws['F6'] = f"{periodo_activo.periodo} {periodo_activo.anio}"
    else:
        ws['F6'] = "No hay periodo activo"
        
    ws['C5'] = f"{tutor.first_name} {tutor.last_name}"
    ws['C6'] = usuario.grupo

    thin_border = Border(left=Side(style='thin'),
                        right=Side(style='thin'),
                        top=Side(style='thin'),
                        bottom=Side(style='thin'))

    # Estilo de fuente
    calibri_10_font = Font(name='Calibri', size=10)
    calibri_10_font_bold = Font(name='Calibri', size=10, bold=True)
    gray_fill = PatternFill(start_color='D8D8D8', end_color='D8D8D8', fill_type='solid')
    
    # Rellenar las filas con los datos de 'actividad'
    row_num = 10
    inserted_rows_count = 0
    for idx, act in enumerate(actividad, start=1):
        inserted_rows_count += 1
        num_cell = ws.cell(row=row_num, column=1)
        num_cell.value = idx
        num_cell.font = calibri_10_font_bold
        num_cell.border = thin_border

        # Llenado de datos en las columnas
        ws.cell(row=row_num, column=2).value = act.tema
        ws.cell(row=row_num, column=3).value = act.objetivos
        ws.cell(row=row_num, column=4).value = act.actividades
        ws.cell(row=row_num, column=5).value = act.recursos
        ws.cell(row=row_num, column=6).value = act.evidencias
        
        # Aplicar bordes y fuente a cada celda en la fila actual
        for col in range(2, 7):
            cell = ws.cell(row=row_num, column=col)
            cell.border = thin_border
            cell.font = calibri_10_font
        
        row_num += 1
        

        # Calcular alumnos_atencion_row y atencion_start_row
    alumnos_atencion_row = max(row_num, 24) + inserted_rows_count -10
    atencion_start_row = alumnos_atencion_row + 1

        # Insertar y combinar la celda "Alumnos a atención individual" dos filas antes de alumnos_atencion_row
    merge_start_row = alumnos_atencion_row - 1
    ws.merge_cells(start_row=merge_start_row, start_column=1, end_row=merge_start_row, end_column=3)
    merged_cell = ws.cell(row=merge_start_row, column=1)
    merged_cell.value = "Alumnos a atención individual"
    merged_cell.font = calibri_10_font_bold
    merged_cell.fill = gray_fill  # Aplicar fondo gris
    merged_cell.border = thin_border  # Aplicar bordes a la celda combinada

# Aplicar el borde a cada celda dentro de la región combinada
    for col in range(1, 4):
        cell = ws.cell(row=merge_start_row, column=col)
        cell.border = thin_border
    
    num_cell = ws.cell(row=alumnos_atencion_row, column=1)
    num_cell.value = "No."
    num_cell.font = calibri_10_font_bold
    num_cell.border = thin_border
    num_cell.fill = gray_fill

    ws.merge_cells(start_row=alumnos_atencion_row, start_column=2, end_row=alumnos_atencion_row, end_column=3)
    cell = ws.cell(row=alumnos_atencion_row, column=2)
    cell.value =  "Nombre"
    cell.font = calibri_10_font_bold
    cell.border = thin_border
    cell.fill = gray_fill

    asunto_cell = ws.cell(row=alumnos_atencion_row, column=4)
    asunto_cell.value = "Asunto a tratar"
    asunto_cell.font = calibri_10_font_bold
    asunto_cell.border = thin_border
    asunto_cell.fill = gray_fill

    ws.merge_cells(start_row=alumnos_atencion_row, start_column=5, end_row=alumnos_atencion_row, end_column=6)

    # Obtener la celda combinada
    merged_cell = ws.cell(row=alumnos_atencion_row, column=5)

    # Configurar el contenido y estilo de la celda combinada
    merged_cell.value = "Observaciones"
    merged_cell.font = calibri_10_font_bold
    merged_cell.fill = gray_fill  # Aplicar fondo gris
    merged_cell.border = thin_border  # Aplicar bordes a la celda combinada

    # Aplicar el borde a cada celda dentro de la región combinada
    for col in range(5, 7):
        cell = ws.cell(row=alumnos_atencion_row, column=col)
        cell.border = thin_border
            
        # Rellenar las filas con los datos de 'atenciones'
    for idx, atencion in enumerate(atenciones, start=1):
            # Numeración continua en la columna 1
            num_cell = ws.cell(row=atencion_start_row, column=1)
            num_cell.value = idx
            num_cell.font = calibri_10_font_bold
            num_cell.border = thin_border

            # Combinar columnas 2 y 3
            ws.merge_cells(start_row=atencion_start_row, start_column=2, end_row=atencion_start_row, end_column=3)
            cell = ws.cell(row=atencion_start_row, column=2)
            cell.value =  f"{atencion.estudiante.User.first_name} {atencion.estudiante.User.last_name}"
            cell.font = calibri_10_font
            cell.border = thin_border

            # Aplicar el borde a la celda combinada
            for col in range(2, 4):
                merged_cell = ws.cell(row=atencion_start_row, column=col)
                merged_cell.border = thin_border
            
            # Llenar datos en las columnas restantes
            asunto_cell = ws.cell(row=atencion_start_row, column=4)
            asunto_cell.value = atencion.asuntoTratar
            asunto_cell.font = calibri_10_font
            asunto_cell.border = thin_border

            ws.merge_cells(start_row=atencion_start_row, start_column=5, end_row=atencion_start_row, end_column=6)
            observaciones_cell = ws.cell(row=atencion_start_row, column=5)
            observaciones_cell.value = atencion.observaciones
            observaciones_cell.font = calibri_10_font
            observaciones_cell.border = thin_border

            # Aplicar el borde a la celda combinada (observaciones)
            for col in range(5, 7):
                merged_cell = ws.cell(row=atencion_start_row, column=col)
                merged_cell.border = thin_border

            atencion_start_row += 1
            
    ws.insert_rows(atencion_start_row + 2)

    # Encabezados en la fila insertada
    headers = ["No.", "Temas no vistos", "Motivo", "Observaciones"]

    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=atencion_start_row + 2, column=col_idx)
        cell.value = header
        cell.font = calibri_10_font_bold
        cell.border = thin_border
        cell.fill = gray_fill

    # Insertar tres filas adicionales
    for i in range(1, 4):
        ws.insert_rows(atencion_start_row + 3 + i)

        # Llenar celdas en las nuevas filas
        num_cell = ws.cell(row=atencion_start_row + 2 + i, column=1)
        num_cell.value = i
        num_cell.font = calibri_10_font_bold
        num_cell.border = thin_border

        tema_cell = ws.cell(row=atencion_start_row + 2 + i, column=2)
        tema_cell.border = thin_border

        motivo_cell = ws.cell(row=atencion_start_row + 2 + i, column=3)
        motivo_cell.border = thin_border

        ob_cell = ws.cell(row=atencion_start_row + 2 + i, column=4)
        ob_cell.border = thin_border
    
    # Crear un objeto BytesIO para guardar el archivo modificado en memoria
    with BytesIO() as in_memory_fp:
        wb.save(in_memory_fp)
        in_memory_fp.seek(0)
        
        # Crear la respuesta HTTP
        response = HttpResponse(in_memory_fp.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=8.- FOR-06-01-B_r1 Plan de Accion Tutorial.xlsx'

    return response 


def descargarReporte(request):

    wb = load_workbook(filename='mainApp/data/baseReportePlanAccion.xlsx')
    ws = wb.active

    tutor = request.user
    periodo_activo = Periodo.objects.filter(estado=True).first()

    area_P = "pedagogía"
    motivos = Canalizacion.objects.filter(area=area_P, cicloAccion=periodo_activo).values_list('motivo', flat=True)
    count_pedagogia = Canalizacion.objects.filter(area=area_P).count()

    area_Psi = "Psicología"
    motivo_psi = Canalizacion.objects.filter(area=area_Psi, cicloAccion=periodo_activo).values_list('motivo', flat=True)
    count_Psicología = Canalizacion.objects.filter(area=area_Psi).count()

    area_B = "Becas"
    motivo_B = Canalizacion.objects.filter(area=area_B, cicloAccion=periodo_activo).values_list('motivo', flat=True)
    count_Becas = Canalizacion.objects.filter(area=area_B).count()

    area_E = "Enfermería"
    motivo_E = Canalizacion.objects.filter(area=area_E, cicloAccion=periodo_activo).values_list('motivo', flat=True)
    count_Enfermería = Canalizacion.objects.filter(area=area_E).count()

    area_I = "Incubadora"
    motivo_I = Canalizacion.objects.filter(area=area_I, cicloAccion=periodo_activo).values_list('motivo', flat=True)
    count_Incubadora = Canalizacion.objects.filter(area=area_I).count()

    area_BT = "Bolsa de Trabajo"
    motivo_BT = Canalizacion.objects.filter(area=area_BT, cicloAccion=periodo_activo).values_list('motivo', flat=True)
    count_BT = Canalizacion.objects.filter(area=area_BT).count()

    area_AA = "Asesor Académico"
    motivo_AA = Canalizacion.objects.filter(area=area_AA, cicloAccion=periodo_activo).values_list('motivo', flat=True)
    count_AA = Canalizacion.objects.filter(area=area_AA).count()

    Estado_Realizadas = 1
    Estado_Canalizadas = 2
    Estado_Programadas = 0

    count_EstadoP = Canalizacion.objects.filter(estadoCanalizados = Estado_Programadas).count()
    count_EstadoR = Canalizacion.objects.filter(estadoCanalizados = Estado_Realizadas).count()
    count_EstadoC = Canalizacion.objects.filter(estadoCanalizados = Estado_Canalizadas).count()


    def convert_to_string(motivos_list):
        return ', '.join(motivos_list) if motivos_list else ''

    # Set each variable in a specific cell
    ws['F9'] = convert_to_string(motivo_psi)
    ws['F10'] = convert_to_string(motivos)
    ws['F11'] = convert_to_string(motivo_B)
    ws['F12'] = convert_to_string(motivo_E)
    ws['F13'] = convert_to_string(motivo_I)
    ws['F14'] = convert_to_string(motivo_BT)
    ws['F15'] = convert_to_string(motivo_AA)

    ws['E9'] = count_Psicología
    ws['E10'] = count_pedagogia
    ws['E11'] = count_Becas
    ws['E12'] = count_Enfermería
    ws['E13'] = count_Incubadora
    ws['E14'] = count_BT
    ws['E15'] = count_AA

    ws['A9'] = count_EstadoP
    ws['B9'] = count_EstadoR
    ws['C9'] = count_EstadoC

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Reporte.xlsx'
    wb.save(response)

    return response