from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as logout_user
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import Http404, HttpResponseRedirect

from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from .forms import UserCreationForm as RegisterForm, EmailChangeForm, NameChangeForm

from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token


User = get_user_model()


# def register(request):
#     form = RegisterForm()
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=raw_password)
#             login(request, user)
#             return redirect('/')

#     return render(request, 'registration/register.html', {'form': form})


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


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create an inactive user with no password:
            user = form.save(commit=False)
            user.is_active = False
            user.set_unusable_password()
            user.save()

            # Send an email to the user with the token:
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
            message = "Hi, activate your account: \n {0}".format(activation_link)
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
        
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)

            form = PasswordChangeForm(request.user)
            return render(request, 'activation.html', {'form': form})

        else:
            return HttpResponse('Activation link is invalid!')
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Important, to update the session with the new password
            return HttpResponse('Password changed successfully')