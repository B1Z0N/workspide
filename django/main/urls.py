from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
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
    path('signup/activate_mail/<str:uidb64>/<str:token>', account_views.activate_mail, name='activate_mail'),
    path('signup/', include('django.contrib.auth.urls')), # mainly here for password reset
    
    path('account/', unauthorized_access(account_views.account), name='account'),
    path('account/delete/<str:uidb64>/<str:token>',unauthorized_access(account_views.delete_account), name='submit_deletion'),
    path('account/email_change_complete/<str:uidb64>/<str:emailb64>/<str:token>', unauthorized_access(account_views.email_change_complete), name='submit_deletion'),
    path('account/password_change/', unauthorized_access(account_views.password_change), name='password_change'),
    path('account/email_change/<str:uidb64>/<str:token>', unauthorized_access(account_views.email_change), name='email_change'),
    path('account/password_reset/', unauthorized_access(
        auth_views.PasswordResetView.as_view(
            subject_template_name='emails/password_reset_subject.txt',
            html_email_template_name='emails/password_reset.html',
        ))
    ),

    path('account/add_resume/', unauthorized_access(search_views.add_ad("resume")), name="add_resume"),
    path('account/add_vacancy/', unauthorized_access(search_views.add_ad("vacancy")), name="add_vacancy"),
    path('account/delete_ad/<int:ad_id>/', unauthorized_access(search_views.delete_ad), name='delete_ad'),
    path('account/edit_resume/<int:ad_id>/', unauthorized_access(search_views.edit_ad('resume')), name='edit_resume'),
    path('account/edit_vacancy/<int:ad_id>/', unauthorized_access(search_views.edit_ad('vacancy')), name='edit_vacancy'),
    path('show_ad/<int:ad_id>/', search_views.show_ad, name='show_ad'),

    path('search/<str:_type>/<str:_text>/', search_views.search, name='search_text'),
    path('search/<str:_type>/', search_views.empty_search, name='search_default'),

]
