from django.shortcuts import render

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, login

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from main.email import account_activation_token, account_deletion_token, \
    email_change_token, send_mail

from main.forms import UserCreationForm as RegisterForm

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create an inactive user with no password:
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send an email to the user with the token:
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            send_mail(
                subject='Activate your account',
                message="""
                We are happy to see you aboard!
                Click on the link down, so we can start doing our job.
                And you will find yours!
                """,
                link=f"http://{current_site}/signup/activate_mail/{uid}/{token}",
                to_email=[form.cleaned_data['email']],
            )

            return render(request, 'alerts/render_base.html', {
                'response_error_text': 'Please confirm your email address to complete the registration',
                'response_error_title': 'Email confirmation'
            })
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})



def activate_mail(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
        # SELECT * FROM User WHERE id = uid
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # activate user and login:
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'alerts/render_base.html', {
            'response_error_title': 'Successful confirmation',
            'response_error_text':
                'You are now registered with email: {}'.format(user.email),
        })
    else:
        return render(request, 'alerts/render_base.html', {
            'response_error_title': 'Confirmation failure',
            'response_error_text': 'Oops, activation link is invalid',
        })
