from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from openpyxl import Workbook, load_workbook
from flask import Flask, send_file
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Create your views here.
class inicio(View):
   def get(self, request):
        return render(request, 'login.html')
     
class loginTest(View):
   def get(self, request):
      return render(request,'test/prueba.html')
   
def actividadTutorial(request):
    return render(request, 'actividadTutorial.html')   

def agregarActividadTutorial(request):
    return render(request, 'agregarActividad.html')   

def editarActividadTutorial(request):
    return render(request, 'editarActividad.html')   

def infoActividadTutorial(request):
    return render(request, 'infoActividad.html')  

def infoEvaluarTutor(request):
    return render(request, 'evaluarTutor.html') 

def infoatencionIndividual(request):
    return render (request, 'atencionIndividual.html')

def infoeditarAtencion(request):
    return render (request,'editarAtencion.html')

def inforegistrarAtencion(request):
    return render (request, 'registrarAtencion.html')

def informePlanAccion(request):
    return render (request, 'informePlanAccion.html')

def reportePlanAccion(request):
    return render (request, 'reportePlanAccion.html')


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
