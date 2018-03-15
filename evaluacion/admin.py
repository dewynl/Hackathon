from django.contrib import admin

from evaluacion.entidades import Jurado, Criterio, Equipo, Evaluacion


class JuradoAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre', 'tipo')


class CriterioAdmin(admin.ModelAdmin):
    list_display = ('explicacion', 'tipo_jurado')


class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'participante1', 'participante2', 'participante3', 'puntuacion')


class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('criterio', 'puntaje', 'jurado', 'equipo')


admin.site.register(Jurado, JuradoAdmin)
admin.site.register(Criterio, CriterioAdmin)
admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Evaluacion, EvaluacionAdmin)
