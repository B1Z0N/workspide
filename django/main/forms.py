from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm as DefaultUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetForm

from .models import Ad, Skill, PetProject, Responsibility


User = get_user_model()


##################################################
# Account management forms
##################################################

class UserCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already exists')
            return self.fields['email'].initial
        return email


class UserChangeForm(DefaultUserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']


class EmailChangeForm(forms.Form):
    email = forms.EmailField(label="Email")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            error = f'Email "{email}" is already in use.'
            self.add_error('email', error)
        return email


class NameChangeForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", max_length=30, required=False)
    last_name = forms.CharField(label="Last name", max_length=30, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', )


##################################################
# Ad forms
##################################################


from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class AdModelForm(forms.ModelForm):
    class Meta:
        model = Ad
        widgets = {
            'text': SummernoteWidget(),
        }
        fields = ('ad_type', 'title', 'text', 'salary', 'currency', 'experience_months', )