from django.contrib.auth.models import User
from django.db import models


class TipoJurado(object):
    TIPOS_JURADO = ((1, 'JURADO TECNICO'), (2, 'JURADO NO TECNICO'))


class Jurado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=25, null=False)
    tipo = models.SmallIntegerField(choices=TipoJurado.TIPOS_JURADO)

    def __str__(self):
        return self.nombre


class Criterio(models.Model):
    explicacion = models.TextField(max_length=70, null=False)
    tipo_jurado = models.SmallIntegerField(choices=TipoJurado.TIPOS_JURADO)

    def __str__(self):
        return 'Criterio :' + self.pk


class Equipo(models.Model):
    nombre = models.CharField(max_length=15, null=False, blank=False)
    puntuacion = models.IntegerField(default=0)

    # participante1 = models.CharField(max_length=25, null=False, blank=False)
    # participante2 = models.CharField(max_length=25, null=False, blank=False)
    # participante3 = models.CharField(max_length=25, null=False, blank=False)

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
