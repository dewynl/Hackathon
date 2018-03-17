from django.contrib.auth.models import User
from django.db import models


class TipoJurado(object):
    JURADO_TECNICO = 1
    JURADO_NO_TECNICO = 2
    TIPOS_JURADO = ((JURADO_TECNICO, 'JURADO TECNICO'), (JURADO_NO_TECNICO, 'JURADO NO TECNICO'))


class Jurado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    tipo = models.SmallIntegerField(choices=TipoJurado.TIPOS_JURADO)

    class Meta:
        unique_together = ('user', 'tipo')

    def __str__(self):
        return self.user.first_name


class Criterio(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False, default='')
    explicacion1 = models.TextField(max_length=250, null=False, default='')
    explicacion2 = models.TextField(max_length=250, null=False, default='')
    explicacion3 = models.TextField(max_length=250, null=False, default='')
    explicacion4 = models.TextField(max_length=250, null=False, default='')
    explicacion5 = models.TextField(max_length=250, null=False, default='')
    tipo_jurado = models.SmallIntegerField(choices=TipoJurado.TIPOS_JURADO)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    nombre = models.CharField(max_length=15, null=False, blank=False)
    puntuacion = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class Participante(models.Model):
    nombre = models.CharField(max_length=50)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Evaluacion(models.Model):
    criterio = models.ForeignKey(Criterio, on_delete=models.DO_NOTHING)
    puntaje = models.SmallIntegerField(null=False, default=0)
    jurado = models.ForeignKey(Jurado, on_delete=models.DO_NOTHING)
    equipo = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING)

    def __str__(self):
        return 'Equipo: ' + self.equipo.nombre + ', Criterio: ' + self.criterio.nombre + \
               ', Jurado: ' + self.jurado.user.first_name + ', Puntaje: ' + str(self.puntaje)


class EquipoEvaluado(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING)
    jurado = models.ForeignKey(Jurado, on_delete=models.DO_NOTHING)

    def __str__(self):
        return 'Evaluado equipo: ' + self.equipo.nombre + ' por jurado ' + self.jurado.user.first_name
