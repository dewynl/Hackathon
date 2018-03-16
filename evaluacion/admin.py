from django.contrib import admin

from evaluacion.models import Jurado, Criterio, Equipo, Evaluacion, Participante, EquipoEvaluado


class JuradoAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo')


class CriterioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_jurado')


class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puntuacion')


class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'equipo')


class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('criterio', 'puntaje', 'jurado', 'equipo')


class EquipoEvaluadoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'jurado')


admin.site.register(Jurado, JuradoAdmin)
admin.site.register(Criterio, CriterioAdmin)
admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Participante, ParticipanteAdmin)
admin.site.register(Evaluacion, EvaluacionAdmin)
admin.site.register(EquipoEvaluado, EquipoEvaluadoAdmin)

