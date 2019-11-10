""" 
    File with views for handling: 
        1. Registration, 
        2. Account settings
        3. Account activation
        4. Account deletion
        5. Password change
        6. Email change
"""

# generals imports for views
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeForm

# imports for creating email messaging
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings

# handwritten functionality imports
from main.forms import EmailChangeForm, NameChangeForm
from main.email import account_deletion_token, email_change_token, send_mail
from main.models import Ad


User = get_user_model()



def account(request):
    email_success = False
    pass_change = request.method == 'POST' and 'pass_change_btn' in request.POST
    delete_account = request.method == 'POST' and 'delete_account_btn' in request.POST
    email_change = request.method == 'POST' and 'email_change_btn' in request.POST

    name_form = NameChangeForm(instance=request.user)

    if pass_change:
        return redirect('/account/password_change')

    if delete_account:
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(request.user.pk))
        token = account_deletion_token.make_token(request.user)
        send_mail(
            subject='Submit your account deletion',
            message="""
                We are sorry to hear that you are leaving us, 
                but if that's what you wish, let it be. 
                Just click on that link down there.
                """,
            link=f"http://{current_site}/account/delete/{uid}/{token}",
            to_email=[request.user.email]
        )
        
    if email_change:
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(request.user.pk))
        token = email_change_token.make_token(request.user)
        send_mail(
            subject='Submit your email change',
            message="""
                So you want to change email, here is what you need to do.
                First open link below in this letter, that we've sent you 
                to your old(this) mail, then open link in your new mail and 
                we're done! If it's not you, who wants to change mail, we'd
                recommend you to reset password on the site.
                """,
            link=f"http://{current_site}/account/email_change/{uid}/{token}",
            to_email=[request.user.email]
        )

        return render(request, 'alerts/render_base.html', {
            'response_error_title' : 'Email change',
            'response_error_text' : 'We`ve sent email change email to your email =)', 
        })
        

    if request.method == 'POST' and 'name_reset_btn' in request.POST:
        instance = NameChangeForm(
            request.POST, instance=request.user).save(commit=False)
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

    ads = Ad.objects.filter(uid=request.user, is_archived=False)
    # SELECT * FROM Ad WHERE uid_id = request.user.id, is_archived = False
    resumes = ads.filter(ad_type='resume')
    vacancies = ads.filter(ad_type='vacancy')

    return render(request, 'account.html', {
        'name_form': name_form,
        'email_success': email_success,
        'pass_change': pass_change,
        'delete_account': delete_account,

        'resumes' : resumes,
        'vacancies' : vacancies,
    })

def delete_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
        # SELECT * FROM User WHERE id = uid
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not account_deletion_token.check_token(user, token):
        return render(request, 'alerts/render_base.html', {
            'response_error_title': 'Account deletion failure',
            'response_error_text': 'Oops, acc deletion link is invalid',
        })

    if user != request.user:
        return render(request, 'alerts/render_base.html', {
            'response_error_title': 'Account deletion failure',
            'response_error_text': 'You need to be logged in to delete account',
        })

    if request.method == 'POST' and 'account_delete_btn' in request.POST:
        user.delete()
        return render(request, 'alerts/render_base.html', {
            'response_error_title': 'Successfull deletion',
            'response_error_text': 'We`re sorry to see you going, go your way, good luck..',
        })

    return render(request, 'activations/account_deletion.html', {})


def password_change(request):
    if request.method == 'POST':
        if 'change_password_btn' in request.POST:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)

                return render(request, 'alerts/render_base.html', {
                    'response_error_text': 'Successful password change',
                    'response_error_title': 'Success'
                })
        elif 'reset_password_btn' in request.POST:
            redirect('/signup/password_reset')
    else:
        form = PasswordChangeForm(user=request.user,)

    return render(request, 'activations/password_change.html', {'form': form})


def email_change(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
        # SELECT * FROM User WHERE id = uid
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not email_change_token.check_token(user, token):
        return render(request, 'alerts/render_base.html', {
            'response_error_title': 'Email change failure',
            'response_error_text': 'Oops, email change link is invalid',
        })

    if request.user != user:
        return render(request, 'alerts/render_base.html', {
            'response_error_title': 'Email change failure',
            'response_error_text': 'You need to be logged in to change your email',
        })

    if request.method == 'POST':
        if 'email_change_btn' in request.POST:
            form = EmailChangeForm(request.POST)
            if form.is_valid():
                current_site = get_current_site(request)
                emailb64 = urlsafe_base64_encode(force_bytes(form.cleaned_data['email']))
                token = email_change_token.make_token(request.user)
                send_mail(
                    subject='Submit your email change',
                    message="""
                        Someone wants to change their email account to this one,
                        if it is you, just click the link, and we are okay.
                        If no, just ignore this.
                        """,
                    link=f"http://{current_site}/account/email_change_complete/{uidb64}/{emailb64}/{token}",
                    to_email=[form.cleaned_data['email']]
                )
                return render(request, 'alerts/render_base.html', {
                    'response_error_text': 'Check your mailbox on new mail',
                    'response_error_title': 'Submit email change',
                })
        elif 'reset_password_btn' in request.POST:
            redirect('/signup/password_reset')
    else:
        form = EmailChangeForm()

    return render(request, 'activations/email_change.html', {'form': form})


def email_change_complete(request, uidb64, emailb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        email = urlsafe_base64_decode(emailb64).decode("utf-8")
        user = User.objects.get(pk=uid)
        # SELECT * FROM User WHERE id = uid
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not email_change_token.check_token(user, token):
        return render(request, 'alerts/render_base.html', {
            'response_error_title': 'Email change failure',
            'response_error_text': 'Oops, email change link is invalid',
        })

    if request.method == 'POST':
        user.email = email
        user.save()
        return render(request, 'alerts/render_base.html', {
            'response_error_title': 'Successfull email change',
            'response_error_text': f'Successfull email change to {email}',
        })

    return render(request, 'activations/email_change_complete.html', {})
