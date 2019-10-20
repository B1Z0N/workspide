from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as logout_user
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import Http404

from .forms import UserCreationForm as RegisterForm, CustomUserChangeForm, \
            EmailChangeForm, NameChangeForm, UserChangeForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def account(request):
    if request.method == 'POST' and 'email_btn' in request.POST:
        email_form = EmailChangeForm(request.POST, instance=request.user)
        if email_form.is_valid():
            email_form.save()
        elif not email_form.data['email']:
            email_form = EmailChangeForm(instance=request.user)
            email_form.save()
    else:
        email_form = EmailChangeForm()
    if request.method == 'POST' and 'name_btn' in request.POST:
        name_form = NameChangeForm(request.POST, instance=request.user)
        if name_form.is_valid():
            name_form.save()
        elif not name_form.data['email']:
            name_form = NameChangeForm(instance=request.user)
            name_form.save()
    else:
        name_form = NameChangeForm()

    return render(request, 'account.html', {
        'email_form' : email_form,
        'name_form' : name_form,
    })


# def account(request):
#     if request.method == 'POST':
#         form = CustomUserChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             initial_email = form.initial['email']
#             initial_first_name = form.initial['first_name']
#             initial_last_name = form.initial['last_name']
#             raise Http404(' '.join[initial_email, initial_first_name, initial_last_name])

#             instance = form.save(commit=False)

#             if not form.cleaned_data['email']:
#                 instance.email = initial_email
#             if not form.cleaned_data['first_name']:
#                 instance.first_name = initial_first_name
#             if not form.cleaned_data['last_name']:
#                 instance.last_name = initial_last_name
#             instance.save()
#     else:
#         form = CustomUserChangeForm()
    
#     return render(request, 'account.html', {
#         'form' : form,
#     })
