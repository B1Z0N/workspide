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
from djmoney.forms.widgets import MoneyWidget

class CustomMoneyWidget(MoneyWidget):
    template_name = 'widgets/money.html'

class AdModelForm(forms.ModelForm):
    class Meta:
        model = Ad
        widgets = {
            'salary' : CustomMoneyWidget
        }
        fields = ('ad_type', 'title', 'city', 'text', 
            'salary', 'experience', 'experience_type', 'pub_dtime')
    
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


from djmoney.forms import MoneyField, MoneyWidget
from djmoney.money import Money

class FiltersForm(forms.Form):
    salary_from = MoneyField(widget=CustomMoneyWidget, default_currency='USD', default_amount=0.0)
    salary_to = forms.FloatField()
    without_salary = forms.BooleanField()

    def clean_salary_from(self):
        if not self.cleaned_data['salary_from']:
            self.cleaned_data['salary_from'] = Money(0.0, 'USD')
        return self.cleaned_data['salary_from']


    experience_from = forms.IntegerField(widget=forms.NumberInput(attrs={'min' : '0'}))
    experience_to = forms.IntegerField(widget=forms.NumberInput(attrs={'min' : '0'}))
    without_experience = forms.BooleanField()

    EXP_TYPE = [
        ('months', 'months'),
        ('years', 'years'),
    ]
    experience_type = forms.ChoiceField(choices=EXP_TYPE)

    ORDER_BY_TYPE = [
        ('pub_dtime', 'date(older first)'),
        ('-pub_dtime', 'date(newer first)'),
        ('salary', 'salary(lowest first)'),
        ('-salary', 'salary(highest first)'),
        ('experience', 'experience(smallest first)'),
        ('-experience', 'experience(biggest first)'),
    ]
    order_by = forms.ChoiceField(choices=ORDER_BY_TYPE)

    city = forms.CharField(max_length=20)

    
    def __init__(self, _salary_from=None, *args, **kwargs):
        super(FiltersForm, self).__init__(*args, **kwargs)
        self.fields['city'].required = False
        self.fields['salary_from'].required = False
        self.fields['salary_to'].required = False
        self.fields['experience_from'].required = False
        self.fields['experience_to'].required = False
        self.fields['without_experience'].required = False
        self.fields['without_salary'].required = False

        self.fields['salary_from'].initial = _salary_from if _salary_from is not None else Money(0.0, 'USD')
