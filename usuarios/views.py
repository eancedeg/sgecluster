from django.views.generic import TemplateView, View, FormView
from django.contrib.auth import login, logout
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .forms import LoginForm
from django.contrib import messages
from paramiko import SSHClient

# Create your views here.


class LoginView(FormView):
    form_class = LoginForm

    template_name = "login.html"
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(request, messages.ERROR, 'Incorrect User or Password')
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


# class StartPageView(LoginRequiredMixin, TemplateView):
#     template_name = 'index.html'
#
#     def get_context_data(self, **kwargs):
#         data = super(StartPageView, self).get_context_data(**kwargs)
#         user = self.request.user
#         return data


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)


def startpage(request):
    return render(request, 'index.html')
