from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from .forms import *
import csv
from .models import *

# Create your views here.

"""
class cargarArchivo(TemplateView):
	template_name = 'cargar.html'

	@staticmethod
	def post(request):
		if request.method == 'POST':
			print(request.FILES['Archivo'])
			return render(request, 'cargar.html', {})
		


"""
def cargarArchivo(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('form.html')

	else:
		form = DocumentForm()

	return render(request, 'cargar.html', {'form':form})
	
def introducirDatos(request):
	template_name='form.html'

	#if request.method == 'POST':


	archivo = Documento.objects.latest('id').documento.url[1:]
	lector = csv.DictReader(open(archivo))

	for entrada in lector:
		# LLENAR ESTUDIANTE
		carnet = entrada['carnet']
		if int(entrada['carnet'][:2]) > 67:
			cohorte = "19"+entrada['carnet'][:2]
		else:
			cohorte = "20"+entrada['carnet'][:2]

		nombre = entrada['nombre']

		if Estudiante.objects.filter(carnet=carnet).count() == 0:
			Estudiante.objects.create(carnet=carnet, cohorte=int(cohorte), nombre=nombre)
		# LLENAR ASIGNATURA

		codasig = entrada['codasig']
		nomasig = entrada['nomasig']
		creditos = entrada['creditos']

		if Asignatura.objects.filter(codasig=codasig).count() == 0:
			Asignatura.objects.create(codasig=codasig, nomasig=nomasig, creditos=int(creditos))
		#LLENAR CURSA
		trimestre = entrada['trimestre']
		anio = entrada['anio']
		nota = entrada['nota']
		if nota == 'R':
			nota = '-1'

		if int(nota) < 3:
			estado = "no aprobado"

		else:
			estado = "aprobado"

		Cursa.objects.create(carnet=Estudiante.objects.filter(carnet=carnet)[0], codasig=Asignatura.objects.filter(codasig=codasig)[0], trimestre=int(trimestre), anio=int(anio), estado=estado, nota=int(nota))

	return render(request, 'form.html', {})


