from django.contrib.auth.models import User
from django.db import models


class TipoJurado(object):
    JURADO_TECNICO = 1
    JURADO_NO_TECNICO = 2
    TIPOS_JURADO = ((JURADO_TECNICO, 'JURADO TECNICO'), (JURADO_NO_TECNICO, 'JURADO NO TECNICO'))


class Jurado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=25, null=False)
    tipo = models.SmallIntegerField(choices=TipoJurado.TIPOS_JURADO)

    def __str__(self):
        return self.nombre


class Criterio(models.Model):
    nombre = models.CharField(max_length=12, null=False, blank=False, default='NombreDefault')
    explicacion1 = models.TextField(max_length=150, null=False, default='')
    explicacion2 = models.TextField(max_length=150, null=False, default='')
    explicacion3 = models.TextField(max_length=150, null=False, default='')
    explicacion4 = models.TextField(max_length=150, null=False, default='')
    explicacion5 = models.TextField(max_length=150, null=False, default='')
    tipo_jurado = models.SmallIntegerField(choices=TipoJurado.TIPOS_JURADO)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    nombre = models.CharField(max_length=15, null=False, blank=False)
    puntuacion = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class Participante(models.Model):
    nombre = models.CharField(max_length=25)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Evaluacion(models.Model):
    criterio = models.ForeignKey(Criterio, on_delete=models.DO_NOTHING)
    puntaje = models.SmallIntegerField(null=False, default=0)
    jurado = models.ForeignKey(Jurado, on_delete=models.DO_NOTHING)
    equipo = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING)
