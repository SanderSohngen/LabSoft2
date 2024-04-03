from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Consulta(models.Model):
    data = models.DateTimeField(default=timezone.now)
    info_consulta = models.TextField()

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=20)
    peso = models.FloatField()
    altura = models.FloatField()
    restricoes_alimentares = models.TextField()
    observacoes = models.TextField()
    consultas = models.ForeignKey(Consulta, on_delete=models.CASCADE)




