from django.views.generic.base import TemplateView
from .forms import UserRegistrationForm, UserLoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth.views import auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import FormView
from .mixin import AjaxRegistrationMixin, AjaxLoginMixin


class HomePageView(TemplateView):
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RegisterView(AjaxRegistrationMixin, FormView):
    form_class = UserRegistrationForm
    template_name = 'registration/registration.html'
    success_url = '/lk/'


class LoginView(AjaxLoginMixin, FormView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    success_url = '/lk/'


class PersonalArea(LoginRequiredMixin,TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def logout_user(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

