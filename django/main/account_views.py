""" 
    File with views for handling: 
        1. Registration, 
        2. Login
        3. Account settings
        4. Account activation
        5. Account deletion
        6. Password change
        7. Email change
"""

# generals imports for views
from django.contrib.auth import get_user_model, login, authenticate, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect

# imports for creating email messaging
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage

# handwritten functionality imports
from .forms import UserCreationForm as RegisterForm, EmailChangeForm, NameChangeForm
from .tokens import account_activation_token, account_deletion_token, password_change_token


User = get_user_model()


def account(request):
    email_success = False
    pass_reset = request.method == 'POST' and 'pass_reset_btn' in request.POST
    delete_account = request.method == 'POST' and 'delete_account_btn' in request.POST
    email_form = EmailChangeForm(instance=request.user)
    name_form = NameChangeForm(instance=request.user)

    if delete_account:
            mail_subject = 'Delete your account.'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(request.user.pk))
            token = account_deletion_token.make_token(request.user)
            activation_link = f"{current_site}/account/delete/{uid}/{token}"
            message = "Hello from WorkSpide, go here to delete account: \n {0}".format(activation_link)
            to_email = request.user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

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
            user.save()

            # Send an email to the user with the token:
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = f"{current_site}/signup/activate_mail/{uid}/{token}"
            message = "Hello from WorkSpide, activate your account: \n {0}".format(activation_link)
            to_email = form.cleaned_data['email']
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
        
            return render(request, 'alerts/render_base.html', { 
                'response_error_text' : 'Please confirm your email address to complete the registration',
                'response_error_title' : 'Email confirmation'
            })
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})


def activate_mail(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # activate user and login:
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'alerts/render_base.html', {
            'response_error_title' : 'Successful confirmation',
            'response_error_text' : 
                'You are now registered with {}, <a href="/">account page</a>'.format(user.email),
        })
    else:
        return render(request, 'alerts/render_base.html', {
            'response_error_title' : 'Confirmation failure',
            'response_error_text' : 'Oops, activation link is invalid',
        })


def delete_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None:
        return render(request, 'alerts/render_base.html', {
                'response_error_title' : 'Deletion failure',
                'response_error_text' : 'Oops, acc deletion link is invalid',
            })

    if request.method == 'POST' and 'account_delete_btn' in request.POST:
        user.delete()
        return render(request, 'alerts/render_base.html', {
            'response_error_title' : 'Successfull deletion',
            'response_error_text' : 'We`re sorry to see you going, go your way, good luck..',
        })
    
    if request.method == 'GET':
        if user is not None and account_deletion_token.check_token(user, token):
            # activate user and login:
            return render(request, 'alerts/account_deletion.html', {
                'response_error_title' : '',
                'response_error_text' : 
                    'You are now registered with {}, <a href="/">account page</a>'.format(user.email),
            })

