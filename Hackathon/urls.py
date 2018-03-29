"""Hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from evaluacion.views import LoginFormView, ListaEquiposEvaluar, RootRedirectView, EvaluarEquipo, ResultadosEquipos, \
    DetallePuntos, PresentacionEquiposList, equipos_random, DetallePuntosReporte

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RootRedirectView.as_view(), name='root'),
    path('login/', LoginFormView.as_view(), name='iniciar-sesion'),
    path('logout/', LoginFormView.as_view(), name='cerrar-sesion'),
    path('equipos-evaluar/', ListaEquiposEvaluar.as_view(), name='equipos-evaluar'),
    path('equipos-evaluar/equipo/<int:pk>', EvaluarEquipo.as_view(), name='equipos-evaluar'),
    path('resultados', ResultadosEquipos.as_view(), name='resultados'),
    path('detalle-puntos/<int:pk>', DetallePuntos.as_view(), name='detalle-puntos'),
    path('detalle-puntos-reporte/<int:pk>', DetallePuntosReporte.as_view(), name='detalle-puntos'),
    path('presentacion-equipos', equipos_random, name='equipos-puntuacion'),
]
