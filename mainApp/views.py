from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from flask import Flask, send_file
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
# from openpyxl.styles import Font, PatternFill, Alignment
# from openpyxl.styles.borders import Border, Side, BORDER_THIN
# import requests
from openpyxl.drawing.image import Image
from io import BytesIO
import os
from django.conf import settings
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



def descargarXLSX(request):
    tutor = request.user
    usuario = Usuarios.objects.get(User=tutor)
    periodo_activo = Periodo.objects.filter(estado=True).first()
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


    # Rellenar las filas con los datos de 'actividad'
    row_num = 10
    for idx, atencion in enumerate(actividad, start=1):
        print(f"Procesando registro {idx}: {atencion.tema}, {atencion.objetivos}, {atencion.actividades}, {atencion.recursos}, {atencion.evidencias}")
        if row_num > 18:
            break
        ws.cell(row=row_num, column=2).value = atencion.tema  # Columna Tema
        ws.cell(row=row_num, column=3).value = atencion.objetivos  # Columna Objetivos
        ws.cell(row=row_num, column=4).value = atencion.actividades  # Columna Actividades
        ws.cell(row=row_num, column=5).value = atencion.recursos  # Columna Recursos
        ws.cell(row=row_num, column=6).value = atencion.evidencias  # Columna Evidencias
        row_num += 1
        
    # Crear un objeto BytesIO para guardar el archivo modificado en memoria
    with BytesIO() as in_memory_fp:
        wb.save(in_memory_fp)
        in_memory_fp.seek(0)
        
        # Crear la respuesta HTTP
        response = HttpResponse(in_memory_fp.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=reporte.xlsx'

    return response 

# def descargarXLSX(request):

    # wb = Workbook()
    # ws = wb.active

    # thin_border = Border(left=Side(style='thin'),
    #                      right=Side(style='thin'),
    #                      top=Side(style='thin'),
    #                      bottom=Side(style='thin'))

    # FuenteRemarcada = Font(bold = True)

    # ws['E5'] = 'Ciclo:'
    # ws['E5'].border = thin_border
    # ws['F5'].border = thin_border
    # ws['E5'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

    # Titulo = ['Plan acción tutorial']

    # for row in range(1, 2):
    #     ws[f'E{row}'].value = Titulo[row - 1]
    #     ws[f'E{row}'].border = thin_border
    #     ws[f'E{row}'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    #     ws.merge_cells(start_row=row, start_column=5, end_row=row, end_column=6)



    # Datos = ["Nombre del tutor:", "Grupo tutorado:"]

    # for row in range(4, 6):
    #     ws[f'A{row}'].value = Datos[row - 4]
    #     ws[f'A{row}'].border = thin_border
    #     ws[f'A{row}'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    #     ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)

    # for row in range(4, 6):
    #     ws[f'C{row}'].border = thin_border
    #     ws.merge_cells(start_row=row, start_column=3, end_row=row, end_column=4)


    # Atributos = ["No", "Tema", "Objetivos", "Actividades", "Recursos", "Evidencias"]

    # for col in range(1, 7):
    #     cell = ws.cell(row=8, column=col)
    #     cell.value = Atributos[col - 1]
    #     cell.border = thin_border
    #     cell.fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    #     cell.font = FuenteRemarcada

    # for row in range(9, 19):
    #     ws[f'A{row}'].value = row - 8
    #     ws[f'A{row}'].border = thin_border

    # for col in range(2, 7):
    #     cell = ws.cell(row=9, column=col)
    #     cell.border = thin_border

    # for col in range(2, 7):
    #     cell = ws.cell(row=10, column=col)
    #     cell.border = thin_border

    # for col in range(2, 7):
    #     cell = ws.cell(row=11, column=col)
    #     cell.border = thin_border

    # for col in range(2, 7):
    #     cell = ws.cell(row=12, column=col)
    #     cell.border = thin_border

    # for col in range(2, 7):
    #     cell = ws.cell(row=13, column=col)
    #     cell.border = thin_border

    # for col in range(2, 7):
    #     cell = ws.cell(row=14, column=col)
    #     cell.border = thin_border

    # for col in range(2, 7):
    #     cell = ws.cell(row=15, column=col)
    #     cell.border = thin_border

    # for col in range(2, 7):
    #     cell = ws.cell(row=16, column=col)
    #     cell.border = thin_border

    # for col in range(2, 7):
    #     cell = ws.cell(row=17, column=col)
    #     cell.border = thin_border

    # for col in range(2, 7):
    #     cell = ws.cell(row=18, column=col)
    #     cell.border = thin_border
    
    # response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # response['Content-Disposition'] = 'attachment; filename=Libro.xlsx'
    # wb.save(response)

    # return response


# def descargarXLSX(request):
#     tutor = request.user
#     usuario = Usuarios.objects.get(User=tutor)
#     periodo_activo = Periodo.objects.filter(estado=True).first()
#     actividad = AccionTutorial.objects.filter(tutor=tutor, cicloAccion=periodo_activo)

#     wb = Workbook()
#     ws = wb.active

#     FuenteRemarcada = Font(bold = True)
#     # Estilo de borde
#     bd = Side(border_style='dotted',style='dotted',color='FF0000') 
    
#     ws['E5'] = 'Ciclo:'
#     ws['E5'].font = FuenteRemarcada
    
#     ws['E5'].border = Border(top=bd,bottom=bd,left=bd,right=bd)
    
#     if periodo_activo:
#         ws['F5'] = f"{periodo_activo.periodo} {periodo_activo.anio}"
#     else:
#         ws['F5'] = "No hay periodo activo"
        
# # Combinar celdas y establecer el valor de 'E1'
#     ws.merge_cells('E1:F1')
#     ws['E1'] = 'PLAN DE ACCIÓN TUTORIAL'
#     ws['E1'].alignment = Alignment(horizontal='center', vertical='center')
#     ws['E1'].font = FuenteRemarcada

#     ws.merge_cells('A4:B4')
#     ws['A4'] = 'Nombre del tutor:'
#     ws.merge_cells('C4:E4')
#     ws['C4'] = f"{tutor.first_name} {tutor.last_name}"

#     # Set the group of the logged-in user in cell C5
#     ws.merge_cells('A5:B5')
#     ws['A5'] = 'Grupo tutorado:'
#     ws['C5'] = usuario.grupo
    
#     ws['A4'].font = FuenteRemarcada
#     ws['A5'].font = FuenteRemarcada
    
#     Atributos = ["No", "Tema", "Objetivos", "Actividades", "Recursos", "Evidencias"]

#     for col in range(1, 7):
#         cell = ws.cell(row=8, column=col)
#         cell.value = Atributos[col - 1]
#         cell.font = FuenteRemarcada

#     # Llenar la columna "No" (Columna A)
#     for row_num in range(9, 19):
#         ws.cell(row=row_num, column=1).value = row_num - 8

#     # Continuar llenando dinámicamente si hay más de 10 registros
#     row_num = 9
#     for idx, atencion in enumerate(actividad, start=1):
#         if row_num > 18:
#             break
#         ws.cell(row=row_num, column=2).value = atencion.tema  # Columna Tema
#         ws.cell(row=row_num, column=3).value = atencion.objetivos  # Columna Objetivos
#         ws.cell(row=row_num, column=4).value = atencion.actividades  # Columna Actividades
#         ws.cell(row=row_num, column=5).value = atencion.recursos  # Columna Recursos
#         ws.cell(row=row_num, column=6).value = atencion.evidencias  # Columna Evidencias
#         row_num += 1

#     # Si hay más de 10 registros, continuar desde donde se quedó la numeración inicial
#     if len(actividad) > 10:
#         for idx, atencion in enumerate(actividad[10:], start=11):
#             if row_num > 18:
#                 break
#             ws.cell(row=row_num, column=1).value = idx
#             ws.cell(row=row_num, column=2).value = atencion.tema  # Columna Tema
#             ws.cell(row=row_num, column=3).value = atencion.objetivos  # Columna Objetivos
#             ws.cell(row=row_num, column=4).value = atencion.actividades  # Columna Actividades
#             ws.cell(row=row_num, column=5).value = atencion.recursos  # Columna Recursos
#             ws.cell(row=row_num, column=6).value = atencion.evidencias  # Columna Evidencias
#             row_num += 1
    
#     # Insertar la imagen en la hoja de cálculo
#     image_url = 'https://sic.cultura.gob.mx/images/62119'
#     response = requests.get(image_url)
#     image = Image(BytesIO(response.content))
#     ws.add_image(image, 'A1')
#     image.width = 130  # Ajusta este valor según sea necesario
#     image.height = 60  # Ajusta este valor según sea necesario
    

    
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=Libro.xlsx'
#     wb.save(response)

#     return response

def descargarReporte(request):
    wb = load_workbook(filename='mainApp/data/baseReportePlanAccion.xlsx')
    ws = wb.active
#
    FuenteRemarcada = Font(bold = True)
#
#    hilera1 = ['Programa', 'Realizada', 'Canalizada']
#    for col in range(1, 4):
#        cell = ws.cell(row=6, column=col)
#        cell.value = hilera1[col - 1]
#        cell.alignment = Alignment(horizontal='center', vertical='center', text_rotation=90)

#    AreasCanalizacion = ['Psicologo', 'Pedagogo', 'Becas', 'Enfermeria', 'Incubadora', 'Bolsa de trabajo', 'Asesor Academico']
#    for row in range(7, 15):
#        ws[f'D{row}'].value = AreasCanalizacion[row - 8] 


    hilera1 = ['Programa', 'Realizada', 'Canalizada']

    for col in range(1, 4):
        cell = ws.cell(row=6, column=col)
        cell.value = hilera1[col - 1]
        cell.alignment = Alignment(horizontal='center', vertical='center', text_rotation=90)

    AreasCanalizacion = ['Psicólogo', 'Pedagogo', 'Becas', 'Enfermería', 'Incubadora', 'Bolsa de trabajo', 'Asesor Académico']
    for row in range(7, 15):
        ws[f'D{row}'].value = AreasCanalizacion[row - 8]
        ws[f'D{row}'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

    Motivos = ['No se cumplieron expectativas', 'Reprobación', 'Problemas económicos', 'Dificultades para el transporte', 'Problemas de trabajo', 'Cambio de carrera', 'Incompatibilidad de horario', 'Faltas al reglamento', 'Cambio de residencia', 'Cambio de universidad', 'Problemas familiares', 'Problemas personales', 'Otras']
    for row in range(7, 21):
        ws[f'H{row}'].value = Motivos[row - 8]
        ws[f'H{row}'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
        ws[f'I{row}'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
        ws[f'J{row}'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

#    Motivos = ['No se cumplieron expectativas', 'Reprobacion', 'Problemas economicos', 'Dificultades para el transporte', 'Problemas de trabajo', 'Cambio de carrera', 'Incompatibilidad de horario', 'Faltas al reglamento', 'Cambio de residencia', 'Cambio de universidad', 'Problemas familiares', 'Problemas personales', 'Otras']
#    for row in range(7, 21):
#        ws[f'J{row}'].value = Motivos[row - 8]

#    hilera2 = ['Cantidad', 'Tipo de baja']
#    for col in range(11, 13):
#        cell = ws.cell(row=6, column=col) 
#        cell.value = hilera2[col - 11]
#        cell.alignment = Alignment(horizontal='center', vertical='center', text_rotation=90)

#    ws['A15'] = 'No programada'
#    ws['A15'].alignment = Alignment(vertical='center', text_rotation=90)

#    ws['D6'] = 'Areas de canalizacion'
#    ws['D15'] = 'Asunto de atencion'


    ws['A6'].font = FuenteRemarcada
    ws.column_dimensions['A'].width = 3
    ws['A6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['A15'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

    ws['B6'].font = FuenteRemarcada
    ws['B6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws.column_dimensions['B'].width = 3
    ws['B15'] = 'No programada'
    ws['B15'].alignment = Alignment(horizontal='center', vertical='center', text_rotation=90)
    ws['B15'].font = FuenteRemarcada
    ws['B15'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

#    ws['B15'] = 'Asunto de atencion'

#    ws['C15'] = 'Cantidad'
#    ws['C15'].alignment = Alignment(vertical='center', text_rotation=90)

#    ws['D15'] = 'Observaciones'

#    ws['J21'] = 'Dificultades para ejercer la tutoria'

#    ws['G6'] = 'Cantidad'
#    ws['G6'].alignment = Alignment(vertical='center', text_rotation=90)

#    ws['H6'] = 'Resultado de la canalizacion'

#    ws['I6'] = 'Total'
#    ws['I6'].alignment = Alignment(vertical='center', text_rotation=90)


#   ws['J6'] = 'Motivo de baja'

#    ws['M6'] = 'Observaciones'    


    ws['C6'].font = FuenteRemarcada
    ws['C6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws.column_dimensions['C'].width = 3
    ws['C15'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

    ws.column_dimensions['D'].width = 20
    ws['D6'] = 'Áreas de canalización'
    ws['D6'].font = FuenteRemarcada
    ws['D6'].alignment = Alignment(vertical='center')
    ws['D6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['D15'] = 'Asunto de atención'
    ws['D15'].alignment = Alignment(vertical='center')
    ws['D15'].font = FuenteRemarcada
    ws['D15'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

    ws['E6'] = 'Cantidad'
    ws['E6'].alignment = Alignment(horizontal='center', vertical='center', text_rotation=90)
    ws['E6'].font = FuenteRemarcada
    ws.column_dimensions['E'].width = 3
    ws['E6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['E15'] = 'Cantidad'
    ws['E15'].alignment = Alignment(horizontal='center', vertical='center', text_rotation=90)
    ws['E15'].font = FuenteRemarcada
    ws['E15'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

    ws.column_dimensions['F'].width = 25
    ws['F6'] = 'Resultado de la canalización'
    ws['F6'].alignment = Alignment(vertical='center')
    ws['F6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['F6'].font = FuenteRemarcada
    ws['F15'].alignment = Alignment(vertical='center')
    ws['F15'].font = FuenteRemarcada
    ws['F15'] = 'Observaciones'
    ws['F15'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

    ws['G6'] = 'Total'
    ws['G6'].font = FuenteRemarcada
    ws['G6'].alignment = Alignment(horizontal='center', vertical='center', text_rotation=90)
    ws['G6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['G21'] = 'Dificultades para ejercer la tutoria'
    ws['G21'].alignment = Alignment(vertical='center')
    ws['G21'].font = FuenteRemarcada
    ws['G21'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws.column_dimensions['G'].width = 3

    ws['H6'] = 'Motivo de baja'
    ws['H6'].alignment = Alignment(vertical='center')
    ws['H6'].font = FuenteRemarcada
    ws['H6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['H21'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

    ws['I6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['I21'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

    ws['J6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['J21'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')


    ws['K6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['K21'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws.column_dimensions['K'].width = 3


    ws['L6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['L21'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws.column_dimensions['L'].width = 3

    ws['M6'] = 'Observaciones'
    ws['M6'].alignment = Alignment(vertical='center')

    ws['M6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['M21'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

    ws['N6'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')
    ws['N21'].fill = PatternFill(fill_type='solid', start_color='D9D9D9', end_color='D9D9D9')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Reporte.xlsx'
    wb.save(response)

    return response