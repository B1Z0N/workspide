from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm as DefaultUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetForm

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .models import Ad, Skill, PetProject, Responsibility, Pide


User = get_user_model()
validate = URLValidator()


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


from django_summernote.widgets import SummernoteWidget


class AdModelForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('ad_type', 'title', 'city', 'text', 
            'salary', 'currency', 'experience', 'experience_type', 'pub_dtime')
    
    def __init__(self, text_widget_attrs=None, *args, **kwargs):
        super(AdModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = SummernoteWidget(attrs={
            'summernote' : text_widget_attrs if text_widget_attrs is not None else {}
        })


class SKillModelForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('text', )


class ResponsibilityModelForm(forms.ModelForm):
    class Meta:
        model = Responsibility
        fields = ('text', )


class PetProjectModelForm(forms.ModelForm):
    class Meta:
        model = PetProject
        fields = ('text', 'link', )

    def clean_link(self):
        link = self.cleaned_data['link']
        try:
            validate(link)
        except ValidationError:
            self.add_error('link', 'Link is invalid')
        return link


class PideModelForm(forms.ModelForm):
    ad_from = forms.ModelChoiceField(
        queryset=Ad.objects.none(), 
        empty_label='Choose your ad',
        required=False,
    )
    class Meta:
        model = Pide
        widgets = {
            'comment': SummernoteWidget(),
        }
        fields = ('ad_from', 'comment', 'pub_dtime', )
    
    def __init__(self, user=None, ad_type=None, 
                text_widget_attrs=None, *args, **kwargs):
        super(PideModelForm, self).__init__(*args, **kwargs)
        if user is not None and ad_type is not None:
            self.fields['ad_from'].queryset = Ad.objects.filter(uid=user, ad_type=ad_type) 
        else:
            self.fields['ad_from'] = None

        self.fields['comment'].widget = SummernoteWidget(attrs={
            'summernote' : text_widget_attrs if text_widget_attrs is not None else {}
        })


class FiltersForm(forms.Form):
    salary_from = forms.IntegerField()
    salary_to = forms.IntegerField()
    
    CURRENCY = [
        ('USD', 'USD'),
        ('UAH', 'UAH'),
        ('EUR', 'EUR'),
    ]
    currency = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, 
        choices=CURRENCY,
    )

    # experience_from = forms.IntegerField()
    # experience_to = forms.IntegerField()
    
    # EXP_TYPE =[
    #     ('months', 'months'),
    #     ('years', 'years'),
    # ]
    # experience_type = forms.MultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple, 
    #     choices=EXP_TYPE,
    # )
    