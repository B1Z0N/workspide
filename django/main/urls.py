from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from . import search_views, account_views


def unauthorized_access(func):
    def _(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'alerts/render_base.html', 
            context= {
                'response_error_title' : 'Unauthorized access',
                'response_error_text' : 'Unauthorized access, go login or register',
            })
        else:
            return func(request, *args, **kwargs)
    return _


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    
    path('signup/register/', account_views.register, name='register'),
    path('signup/', include('django.contrib.auth.urls')),
    path('account/', unauthorized_access(account_views.account), name='account'),
    
    path('signup/activate_mail/<str:uidb64>/<str:token>', account_views.activate_mail, name='activate_main'),
    path('account/delete/<str:uidb64>/<str:token>', account_views.delete_account, name='submit_deletion'),
    path('account/password_change/', unauthorized_access(account_views.password_change), name='password_change'),
    # path('account/password_reset/', TemplateView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),

    path('search/<str:_type>/<str:_text>/', search_views.search, name='search_text'),
    path('search/<str:_type>/', search_views.empty_search, name='search_default'),
]
