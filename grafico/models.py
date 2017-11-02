from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Asignatura(models.Model):
    codasig = models.CharField(primary_key=True, max_length=6)
    nomasig = models.CharField(max_length=50)
    creditos = models.DecimalField(max_digits=2, decimal_places=0)

    class Meta:
        db_table = 'asignatura'

class Cursa(models.Model):
    id = models.AutoField(primary_key=True, default = -1)
    carnet = models.ForeignKey('Estudiante', models.CASCADE, db_column='carnet')
    codasig = models.ForeignKey('Asignatura', models.CASCADE, db_column='codasig')
    trimestre = models.DecimalField(max_digits=1, decimal_places=0)
    anio = models.DecimalField(max_digits=4, decimal_places=0)
    estado = models.CharField(max_length=10)
    nota = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)

    class Meta:
        db_table = 'cursa'
        unique_together = (('carnet', 'codasig', 'trimestre', 'anio'))


class Estudiante(models.Model):
    carnet = models.CharField(primary_key=True, max_length=7)
    cohorte = models.DecimalField(max_digits=4, decimal_places=0)
    nombre = models.CharField(max_length=60)

    class Meta:
        db_table = 'estudiante'


class Documento(models.Model):
    documento = models.FileField()
    fecha = models.DateTimeField(auto_now_add=True)