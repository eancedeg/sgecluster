from django.views.generic import View, FormView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from .forms import LoginForm
from django.contrib import messages
from django.http import JsonResponse
import paramiko
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth.models import User


# Create your views here.

def loginView(request):
    error_login = ''
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            log_user = form.get_user()
            user = request.POST['username']
            passwd = request.POST['password']

            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
                client.connect(settings.CLUSTERIP, 22, 'eancede', 'Insondable.21')
                #entrada, salida, error = client.exec_command('ls')
                login(request, log_user)
            except paramiko.ssh_exception.AuthenticationException:
                error_login = 'Invalid user or password at DFQM Cluster'

            return HttpResponseRedirect(reverse('inicio'))
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'errors': error_login})


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
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
            client.connect(settings.CLUSTERIP, 22, form.get_user())
            login(self.request, form.get_user())
        except paramiko.ssh_exception.AuthenticationException:
            pass

        return super(LoginView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)


@login_required
def startpage(request):
    user = request.user.get_username()
    return render(request, 'home.html', {'user': user})


@login_required
def calculation(request):
    data = {'users': 3, 'total': 5, 'scenario': 12}
    return JsonResponse(data)
