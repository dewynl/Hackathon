from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, RedirectView, ListView, DetailView

from Hackathon import settings
from evaluacion.forms.forms import LoginForm
from evaluacion.models import Equipo, Criterio, TipoJurado, Jurado


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
    queryset = Equipo.objects.all()
    paginate_by = 25
    login_url = settings.LOGIN_URL


class EvaluarEquipo(DetailView):
    model = Equipo
    template_name = 'evaluar-equipo.html'

    def get_context_data(self, **kwargs):
        context = super(EvaluarEquipo, self).get_context_data(**kwargs)
        jurado = Jurado.objects.filter(user=self.request.user).first()
        context['criterios'] = Criterio.objects.all().filter(tipo_jurado=jurado.tipo)
        print(context['criterios'])
        return context
