from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def new_calc(request):
    return render(request, 'calculation/calculation.html')
