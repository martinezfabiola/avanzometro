# Universidad Simon Bolivar
# Ingenieria de Software
# Integrantes:
# 	Abelardo Salazar
# 	Amanda Camacho
# 	Fabiola Martinez
# 	Lautaro Villalon
# 	Maria Bracamonte
# 	Yarima Luciani
# Descripcion: archivo manejador de vistas.
# Ultima modificacion: 2 de noviembre 2017. 

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django import forms
from .forms import *
import csv
from .models import *
from django.http import JsonResponse

from grafico.forms import SignUpForm
import json

# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('../grafico/cargar')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def cargarArchivo(request):
	# SI RECIBIMOS EL ARCHIVO POR POST, LO GUARDAMOS Y VAMOS A FORM

	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/grafico/form')

	# SI ACABAMOS DE ABRIR LA VENTANA, MOSTRAMOS LA CARGA DEL ARCHIVO.

	else:
		form = DocumentForm()

	return render(request, 'cargar.html', {'form':form})


@login_required	
def introducirDatos(request):
	template_name='form.html'

	# SI RECIBIMOS LOS DATOS DEL FORMULARIO:
	
	if request.method == 'POST':
		cohorteQuery = request.POST['cohorteQuery']

		# GUARDAMOS LAS CUATRO COHORTES EN LA SESION

		request.session['cohorteQuery'] = cohorteQuery
		request.session['cohorteQuery2'] = request.POST['cohorteQuery2']
		request.session['cohorteQuery3'] = request.POST['cohorteQuery3']
		request.session['cohorteQuery4'] = request.POST['cohorteQuery4']

		# GUARDAMOS EL NOMBRE DE LA CARRERA EN LA SESION

		request.session['carreraQuery'] = request.POST['carreraQuery'][4:]
		request.session['codCarrera'] = request.POST['carreraQuery'][:4]

		# ENVIAMOS A FORMULARIO DE GRANULARIDAD

		return redirect('/grafico/granularidad')

	# ELIMINAMOS DATOS VIEJOS DE LA BASE DE DATOS

	Cursa.objects.all().delete()
	Asignatura.objects.all().delete()
	Estudiante.objects.all().delete()

	# LEEMOS EL ARCHIVO

	archivo = Documento.objects.latest('id').documento.url[1:]
	lector = csv.DictReader(open(archivo))

	#-- CARGA DE BASE DE DATOS

	for entrada in lector:
		# LLENAR ESTUDIANTE
		carnet = entrada['carnet']
		if int(entrada['carnet'][:2]) > 67:
			cohorte = "19"+entrada['carnet'][:2]
		else:
			cohorte = "20"+entrada['carnet'][:2]

		nombre = entrada['nombre']

		carrera = entrada['carrera']

		if Estudiante.objects.filter(carnet=carnet).count() == 0:
			Estudiante.objects.create(carnet=carnet, cohorte=int(cohorte), carrera=carrera, nombre=nombre)
		# LLENAR ASIGNATURA

		codasig = entrada['codasig']
		nomasig = entrada['nomasig']
		creditos = entrada['creditos']

		if Asignatura.objects.filter(codasig=codasig).count() == 0:
			Asignatura.objects.create(codasig=codasig, nomasig=nomasig, creditos=int(creditos))
		#LLENAR CURSA
		trimestre = entrada['trimestre']
		nota = entrada['nota']
		if nota == 'R':
			nota = '-1'

		if int(nota) < 3:
			estado = "naprobado"

		else:
			estado = "aprobado"

		Cursa.objects.create(carnet=Estudiante.objects.filter(carnet=carnet)[0], codasig=Asignatura.objects.filter(codasig=codasig)[0], trimestre=int(trimestre), estado=estado, nota=int(nota))

	#-- FIN DE CARGA DE BASE DE DATOS

	# MOSTRAMOS FORMULARIO

	return render(request, 'form.html', {})

@login_required
def introducirGranularidad(request):
	template_name='formGranularidad.html'

	# SI RECIBIMOS LOS DATOS DEL FORMULARIO:

	if request.method == "POST":

		cohorte1 = request.session['cohorteQuery']
		cohorte2 = request.session['cohorteQuery2']
		cohorte3 = request.session['cohorteQuery3']
		cohorte4 = request.session['cohorteQuery4']

		carreraQuery = request.session['codCarrera']

		granularidad = int(request.POST['granularidad'])

		# DICCIONARIOS DE LOS 15 QUERIES PARA COHORTE

		resultDic = {}
		resultDic2 = {}
		resultDic3 = {}
		resultDic4 = {}

		# COHORTE 1 (OBLIGATORIA): CARGAMOS UN SUB-DICCIONARIO DEL QUERY POR CADA TRIMESTRE

		for i in range(1, 16):
			resultDic[i] = hacerQuery(cohorte1, str(i), carreraQuery, granularidad)

		# COHORTE 2 (OPCIONAL): CARGAMOS UN SUB-DICCIONARIO DEL QUERY POR CADA TRIMESTRE

		if cohorte2 != "":

			for i in range(1, 16):
				resultDic2[i] = hacerQuery(cohorte2, str(i), carreraQuery, granularidad)

		# COHORTE 3 (OPCIONAL): CARGAMOS UN SUB-DICCIONARIO DEL QUERY POR CADA TRIMESTRE

		if cohorte3 != "":

			for i in range(1, 16):
				resultDic3[i] = hacerQuery(cohorte3, str(i), carreraQuery, granularidad)

		# COHORTE 4 (OPCIONAL): CARGAMOS UN SUB-DICCIONARIO DEL QUERY POR CADA TRIMESTRE

		if cohorte4 != "":

			for i in range(1, 16):
				resultDic4[i] = hacerQuery(cohorte4, str(i), carreraQuery, granularidad)

		# GUARDAMOS LOS CUATRO DICCIONARIOS POR CADA COHORTE EN LA SESION

		request.session['resultDic'] = resultDic
		request.session['resultDic2'] = resultDic2
		request.session['resultDic3'] = resultDic3
		request.session['resultDic4'] = resultDic4

		# HACEMOS LOS LABELS DEL EJE X Y LOS GUARDAMOS EN LA SESION
		labels = hacerLabels(granularidad)

		request.session['labels'] = labels

		# CALCULAMOS LAS CLAVES DE LOS DICCIONARIOS
		claves = hacerClaves(resultDic[1])

		request.session['claves'] = claves

		# REDIRECCIONAMOS AL GRAFICO

		return redirect('/grafico/chart')

	# MOSTRAMOS EL FORMULARIO DE GRANULARIDAD

	return render(request, 'formGranularidad.html', {})

@login_required
def mostrarGrafico(request):
	template_name='chart.html'

	# OBTENEMOS LOS DICCIONARIOS DE DATOS DE LAS CUATRO COHORTES

	carreraQuery = request.session['carreraQuery']

	cohorteQuery = request.session['cohorteQuery']
	cohorteQuery2 = request.session['cohorteQuery2']
	cohorteQuery3 = request.session['cohorteQuery3']
	cohorteQuery4 = request.session['cohorteQuery4']

	# CONVERTIMOS LOS DICCIONARIOS EN STRINGS COMPATIBLES CON VARIABLES JSON DE JavaScript

	jsonDic = json.dumps(request.session['resultDic'])
	jsonDic2 = json.dumps(request.session['resultDic2'])
	jsonDic3 = json.dumps(request.session['resultDic3'])
	jsonDic4 = json.dumps(request.session['resultDic4'])

	# CREAMOS DICCIONARIO A ENVIAR

	labels = request.session['labels']
	claves = request.session['claves']

	print(labels)
	print()
	print(claves)

	diccionario = {'resultDic': jsonDic, 'resultDic2': jsonDic2, 'resultDic3': jsonDic3, 'resultDic4': jsonDic4,
				'carreraQuery': carreraQuery, 'cohorteQuery': cohorteQuery, 'cohorteQuery2': cohorteQuery2,
				'cohorteQuery3': cohorteQuery3, 'cohorteQuery4': cohorteQuery4, 'labels': labels, 'claves': claves}

	# ENVIAMOS TODAS LAS VARIABLES AL GRAFICO

	return render(request, 'chart.html', diccionario)


# FUNCION PARA QUERY
def hacerQuery(cohorteQuery, trimQuery, carreraQuery, granularidad):

		# QUERY ESPECIFICO POR COHORTE, TRIMESTRE Y CARRERA

		query = "SELECT sum(creditos), id, cursa.carnet, estado FROM asignatura, cursa, estudiante WHERE asignatura.codasig = cursa.codasig AND cursa.carnet = estudiante.carnet AND cursa.estado = 'aprobado' AND estudiante.cohorte = "+cohorteQuery+" AND estudiante.carrera = "+carreraQuery+" AND cursa.trimestre <= "+trimQuery+" GROUP BY cursa.carnet, estado, id ORDER BY sum;"

		# QUERY GENERICO PARA CALCULAR LA CANTIDAD QUE TIENE 0 CREDITOS APROBADOS

		query0 = "SELECT DISTINCT id, cursa.carnet FROM cursa, estudiante WHERE cursa.carnet = estudiante.carnet AND estudiante.cohorte = "+cohorteQuery+" AND estudiante.carrera = "+carreraQuery+"  AND cursa.trimestre <= "+trimQuery+" GROUP BY cursa.carnet, id;"
		
		# REALIZAMOS EL QUERY

		resultado = Cursa.objects.raw(query)
		resultado0 = Cursa.objects.raw(query0)

		#-- GUARDAR DATOS ORDENADOS

		resultados = []
		for r in resultado:
			resultados.append(int(r.sum))

		i = 0
		resultDic = {}

		#-- FIN DE GUARDAR DATOS ORDENADOS

		#-- CALCULAMOS LA CANTIDAD DE ESTUDIANTES POR CREDITOS A PARTIR DE LOS DATOS Y CREAMOS DICCIONARIO DE TRIMESTRE
		maximo = 240 - (240%granularidad) + granularidad

		while i <= maximo:
			resultDic[i] = 0

			if (i>240):
				while len(resultados) != 0:
					resultDic[i] += 1
					resultados.pop(0)	
			else:
				while len(resultados) != 0 and resultados[0] <= i:
					resultDic[i] += 1
					resultados.pop(0)

			#if len(resultados) == 0:
			#	break

			i += granularidad

		#-- FIN DE CALCULO DE CANTIDAD DE ESTUDIANTES

		#-- VERIFICAMOS LA EXISTENCIA Y CANTIDAD DE ESTUDIANTES CON 0 CREDITOS APROBADOS

		for rGeneral in resultado0:
			esta = False
			for rAprobado in resultado:
				if rAprobado.carnet.carnet == rGeneral.carnet.carnet:
					esta = True
					break

			if not esta:
				resultDic[0] += 1

		#-- FIN DE VERIFICACION DE EXISTENCIA Y CANTIDAD DE ESTUDIANTES

		#-- CALCULO DE PORCENTAJE DE ESTUDIANTES

		total = 0
		for key in resultDic:
			total += resultDic[key]

		if total > 0:
			for key in resultDic:
				resultDic[key] = resultDic[key]*100//total

		#-- FIN DE CALCULO DE PORCENTAJE DE ESTUDIANTES

		# DEVOLVEMOS DICCIONARIO CON EL PORCENTAJE DE CANTIDAD DE ESTUDIANTES CON CIERTA
		# CANTIDAD DE CREDITOS APROBADOS (DESDE 0 HASTA 241 O MAS CON GRANULARIDAD DE 16)

		return resultDic

# FUNCION PARA LABEL DEL EJE X
def hacerLabels(granularidad):

	granulos = ["0"]
	tope = granularidad

	while tope <= 240:
		intervalo = str(tope-(granularidad-1)) + " - " + str(tope)
		granulos.append(intervalo)
		tope += granularidad

	ultimo = tope-granularidad
	granulos.append(str(ultimo) + " - ...")

	return granulos

# FUNCION PARA CALCULAR LAS CLAVES DEL DICCIONARIO DE QUERY
def hacerClaves(resultDic):
	claves = []

	for key in resultDic:
		claves.append(key)

	claves.sort(key=lambda clave: int(clave))

	return claves

