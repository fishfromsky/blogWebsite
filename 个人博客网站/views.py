from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate
from django.contrib import auth
from .forms import LoginForm, RegForm
from django.urls import reverse
from django.contrib.auth.models import User


def home(request):
    context = {}
    return render_to_response('home.html', context)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('from', reverse('home')))
            else:
                login_form.add_error(None, '用户名或密码错误')
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)

