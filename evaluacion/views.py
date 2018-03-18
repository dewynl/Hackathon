from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import FormView, RedirectView, ListView, DetailView

from Hackathon import settings
from evaluacion.forms.forms import LoginForm
from evaluacion.models import Equipo, Criterio, TipoJurado, Jurado, Evaluacion, EquipoEvaluado, CantidadCriterios

from random import random, shuffle


class RootRedirectView(RedirectView):
    pattern_name = 'equipos-evaluar'


class LoginFormView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/equipos-evaluar'

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(self.request, user=user)

        return super(LoginFormView, self).form_valid(form)


class LogoutView(RedirectView):
    pattern_name = 'iniciar-sesion'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ListaEquiposEvaluar(LoginRequiredMixin, ListView):
    model = Equipo
    template_name = 'equipos_list.html'
    queryset = Equipo.objects.filter(habilitado=True)
    paginate_by = 25
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        qs = Equipo.objects.all()
        jurado = Jurado.objects.filter(user=self.request.user).first()
        equipos_evaluados = [e.equipo.id for e in EquipoEvaluado.objects.filter(jurado=jurado)]
        qs = qs.exclude(id__in=equipos_evaluados)
        qs = qs.filter(habilitado=True)
        return qs


class EvaluarEquipo(LoginRequiredMixin, DetailView):
    model = Equipo
    template_name = 'evaluar-equipo.html'
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(EvaluarEquipo, self).get_context_data(**kwargs)
        jurado = Jurado.objects.filter(user=self.request.user).first()
        context['criterios'] = Criterio.objects.all().filter(tipo_jurado=jurado.tipo)
        return context

    def post(self, request, *args, **kwargs):
        ok = False
        equipo = Equipo.objects.filter(id=request.POST['equipo']).first()
        jurado = Jurado.objects.filter(user=self.request.user).first()
        cant = 0
        for i in request.POST.keys():
            if 'group' in i:
                cant += 1
                c = Criterio.objects.filter(id=int(i.split('-')[1])).first()
                puntuacion = int(request.POST[i])
                e = Evaluacion(criterio=c, jurado=jurado, equipo=equipo, puntaje=puntuacion)
                e.save()
                equipo.puntuacion += puntuacion
                equipo.save()

        if jurado.tipo == TipoJurado.JURADO_TECNICO and cant == CantidadCriterios.CANTIDAD_CRITERIOS_TECNICOS:
            ok = True
        elif jurado.tipo == TipoJurado.JURADO_NO_TECNICO and cant == CantidadCriterios.CANTIDAD_CRITERIOS_NO_TECNICOS:
            ok = True

        if ok:
            EquipoEvaluado(equipo=equipo, jurado=jurado).save()
        return redirect('/')


class ResultadosEquipos(LoginRequiredMixin, ListView):
    model = Equipo
    template_name = 'resultados.html'
    queryset = Equipo.objects.filter(habilitado=True).order_by('-puntuacion')
    paginate_by = 25
    login_url = settings.LOGIN_URL


class DetallePuntos(LoginRequiredMixin, DetailView):
    model = Equipo
    template_name = 'detalle-resultado.html'
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(DetallePuntos, self).get_context_data(**kwargs)
        evaluaciones = Evaluacion.objects.filter(equipo=self.object)
        criterios_no_tecnicos = {}
        criterios_tecnicos = {}

        total_puntos_tecnicos = 0
        total_puntos_no_tecnicos = 0
        for e in evaluaciones:
            if e.criterio.tipo_jurado == TipoJurado.JURADO_NO_TECNICO:
                if e.criterio.nombre in criterios_no_tecnicos:
                    criterios_no_tecnicos[e.criterio.nombre] += e.puntaje
                    total_puntos_no_tecnicos += e.puntaje
                else:
                    criterios_no_tecnicos[e.criterio.nombre] = e.puntaje
                    total_puntos_no_tecnicos += e.puntaje

            elif e.criterio.tipo_jurado == TipoJurado.JURADO_TECNICO:
                if e.criterio.nombre in criterios_tecnicos:
                    criterios_tecnicos[e.criterio.nombre] += e.puntaje
                    total_puntos_tecnicos += e.puntaje
                else:
                    criterios_tecnicos[e.criterio.nombre] = e.puntaje
                    total_puntos_tecnicos += e.puntaje

        context['criterios_no_tecnicos'] = criterios_no_tecnicos
        context['criterios_tecnicos'] = criterios_tecnicos
        context['total_puntos_tecnicos'] = total_puntos_tecnicos
        context['total_puntos_no_tecnicos'] = total_puntos_no_tecnicos
        context['total_final'] = total_puntos_no_tecnicos + total_puntos_tecnicos
        return context


class ShuffledPaginator(Paginator):
    def page(self, number):
        page = super(ShuffledPaginator, self).page(number)
        random.shuffle(page.object_list)
        return page


class PresentacionEquiposList(LoginRequiredMixin, ListView):
    login_url = settings.LOGIN_URL
    model = Equipo
    paginator_class = ShuffledPaginator
    template_name = 'lista-presentacion.html'


def equipos_random(request):
    template = 'lista-presentacion.html'
    if request.method == 'GET':
        equipos = [e for e in Equipo.objects.filter(habilitado=True)]
        shuffle(equipos)
        return render(request=request, template_name=template, context={'equipos': equipos})
