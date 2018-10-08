from django.views.generic import View, FormView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.conf import settings
from .forms import LoginForm
from django.contrib import messages
from django.http import JsonResponse
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


@login_required
def startpage(request):
    user = request.user.get_username()
    return render(request, 'home.html', {'user': user})


@login_required
def calculation(request):
    data = {'users': 3, 'total': 5, 'scenario': 12}
    return JsonResponse(data)
