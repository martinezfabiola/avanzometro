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
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/grafico/form')

	else:
		form = DocumentForm()

	return render(request, 'cargar.html', {'form':form})


@login_required	
def introducirDatos(request):
	template_name='form.html'
	
	if request.method == 'POST':
		cohorteQuery = request.POST['cohorteQuery']
		carreraQuery = request.POST['carreraQuery'][:4]


		resultDic = {}
		resultDic2 = {}
		resultDic3 = {}
		resultDic4 = {}

		for i in range(1, 16):
			resultDic[i] = hacerQuery(cohorteQuery, str(i), carreraQuery)

		if request.POST['cohorteQuery2'] != "":

			for i in range(1, 16):
				resultDic2[i] = hacerQuery(request.POST['cohorteQuery2'], str(i), carreraQuery)

		if request.POST['cohorteQuery3'] != "":

			for i in range(1, 16):
				resultDic3[i] = hacerQuery(request.POST['cohorteQuery3'], str(i), carreraQuery)

		if request.POST['cohorteQuery4'] != "":

			for i in range(1, 16):
				resultDic4[i] = hacerQuery(request.POST['cohorteQuery4'], str(i), carreraQuery)

		request.session['resultDic'] = resultDic
		request.session['resultDic2'] = resultDic2
		request.session['resultDic3'] = resultDic3
		request.session['resultDic4'] = resultDic4

		request.session['cohorteQuery'] = cohorteQuery
		request.session['cohorteQuery2'] = request.POST['cohorteQuery2']
		request.session['cohorteQuery3'] = request.POST['cohorteQuery3']
		request.session['cohorteQuery4'] = request.POST['cohorteQuery4']

		request.session['carreraQuery'] = request.POST['carreraQuery'][4:]


		return redirect('/grafico/chart')

	Cursa.objects.all().delete()
	Asignatura.objects.all().delete()
	Estudiante.objects.all().delete()

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

	return render(request, 'form.html', {})


@login_required
def mostrarGrafico(request):
	template_name='chart.html'
	carreraQuery = request.session['carreraQuery']

	cohorteQuery = request.session['cohorteQuery']
	cohorteQuery2 = request.session['cohorteQuery2']
	cohorteQuery3 = request.session['cohorteQuery3']
	cohorteQuery4 = request.session['cohorteQuery4']

	print(request.session['resultDic2'])

	jsonDic = json.dumps(request.session['resultDic'])
	jsonDic2 = json.dumps(request.session['resultDic2'])
	jsonDic3 = json.dumps(request.session['resultDic3'])
	jsonDic4 = json.dumps(request.session['resultDic4'])

	return render(request, 'chart.html', {'resultDic': jsonDic, 'resultDic2': jsonDic2, 'resultDic3': jsonDic3, 'resultDic4': jsonDic4, 'carreraQuery': carreraQuery, 'cohorteQuery': cohorteQuery, 'cohorteQuery2': cohorteQuery2, 'cohorteQuery3': cohorteQuery3, 'cohorteQuery4': cohorteQuery4})


# FUNCION PARA QUERY
def hacerQuery(cohorteQuery, trimQuery, carreraQuery):

		query = "SELECT sum(creditos), id, cursa.carnet, estado FROM asignatura, cursa, estudiante WHERE asignatura.codasig = cursa.codasig AND cursa.carnet = estudiante.carnet AND cursa.estado = 'aprobado' AND estudiante.cohorte = "+cohorteQuery+" AND estudiante.carrera = "+carreraQuery+" AND cursa.trimestre <= "+trimQuery+" GROUP BY cursa.carnet, estado, id ORDER BY sum;"

		query0 = "SELECT DISTINCT id, cursa.carnet FROM cursa, estudiante WHERE cursa.carnet = estudiante.carnet AND estudiante.cohorte = "+cohorteQuery+" AND estudiante.carrera = "+carreraQuery+"  AND cursa.trimestre <= "+trimQuery+" GROUP BY cursa.carnet, id;"
		
		resultado = Cursa.objects.raw(query)
		resultado0 = Cursa.objects.raw(query0)

		resultados = []
		for r in resultado:
			resultados.append(int(r.sum))

		i = 0
		resultDic = {}

		while i <= 240:
			resultDic[i] = 0

			while len(resultados) != 0 and resultados[0] <= i:
				resultDic[i] += 1
				resultados.pop(0)

			#if len(resultados) == 0:
			#	break

			i += 16


		for rGeneral in resultado0:
			esta = False
			for rAprobado in resultado:
				if rAprobado.carnet.carnet == rGeneral.carnet.carnet:
					esta = True
					break

			if not esta:
				resultDic[0] += 1

		total = 0
		for key in resultDic:
			total += resultDic[key]

		if total > 0:
			for key in resultDic:
				resultDic[key] = resultDic[key]*100//total

		return resultDic
