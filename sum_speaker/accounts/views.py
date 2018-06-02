from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
from .forms import signupform
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

# Create your views here.


def signup(request):
    if request.method == 'POST' :
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = signupform()
       #messages.success(request,"회원가입이 완료되었습니다.")
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
