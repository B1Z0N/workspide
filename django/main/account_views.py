from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as logout_user
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import Http404, HttpResponseRedirect

from .forms import UserCreationForm as RegisterForm, EmailChangeForm, NameChangeForm
from .models import User


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('/')

    return render(request, 'registration/register.html', {'form': form})


def account(request):
    email_success = False
    pass_reset = request.method == 'POST' and 'pass_reset_btn' in request.POST
    delete_account = request.method == 'POST' and 'delete_account_btn' in request.POST
    email_form = EmailChangeForm(instance=request.user)
    name_form = NameChangeForm(instance=request.user)

    if request.method == 'POST' and 'email_btn' in request.POST:
        email_form = EmailChangeForm(request.POST, instance=request.user)
        if email_form.is_valid():
            email_form.save()
            email_success = True

    if request.method == 'POST' and 'name_reset_btn' in request.POST:
        instance = NameChangeForm(request.POST, instance=request.user).save(commit=False)
        instance.first_name = instance.last_name = None
        instance.save()

    if request.method == 'POST' and 'name_btn' in request.POST:
        name_form = NameChangeForm(request.POST, instance=request.user)
        if name_form.is_valid():
            instance = name_form.save(commit=False)
            if not instance.first_name:
                instance.first_name = name_form.initial['first_name']
            if not instance.last_name:
                instance.last_name = name_form.initial['last_name']
            instance.save()
            name_form = NameChangeForm(instance=instance)

    return render(request, 'account.html', {
        'email_form' : email_form,
        'name_form' : name_form,
        'email_success' : email_success,
        'pass_reset' : pass_reset,
        'delete_account' : delete_account,
    })

