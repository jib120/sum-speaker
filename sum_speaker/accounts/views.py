from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
from .forms import signupform
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def signup(request):
    if request.method == 'POST' :
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = signupform()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')