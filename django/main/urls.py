from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from main.views import signup_views, account_views, ad_views, pide_views, search_views


# function that denies unauthorized access to view
def unauthorized_access(view):
    def _(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'alerts/render_base.html',
            context={
                'response_error_title': 'Unauthorized access',
                'response_error_text': 'Unauthorized access, go login or register',
            })
        else:
            return view(request, *args, **kwargs)
    return _


urlpatterns = [
     # site base view
     path('', TemplateView.as_view(template_name='index.html'), name='index'),


     # register/login/activate views
     path('signup/register/', signup_views.register, name='register'),
     path('signup/activate_mail/<str:uidb64>/<str:token>',
         signup_views.activate_mail, name='activate_mail'),
     # mainly here for password reset
     path('signup/', include('django.contrib.auth.urls')),


     # account views
     path('account/', unauthorized_access(account_views.account), name='account'),
     path('account/delete/<str:uidb64>/<str:token>',
         unauthorized_access(account_views.delete_account), name='submit_deletion'),
     path('account/email_change_complete/<str:uidb64>/<str:emailb64>/<str:token>',
         unauthorized_access(account_views.email_change_complete), name='submit_deletion'),
     path('account/password_change/',
         unauthorized_access(account_views.password_change), name='password_change'),
     path('account/email_change/<str:uidb64>/<str:token>',
         unauthorized_access(account_views.email_change), name='email_change'),
     path('account/password_reset/',
        auth_views.PasswordResetView.as_view(
            subject_template_name='emails/password_reset_subject.txt',
            html_email_template_name='emails/password_reset.html',
        )
    ),


     # ad create/delete/edit views
     path('show_ad/<int:ad_id>/', ad_views.show_ad, name='show_ad'),
     path('account/add_resume/',
         unauthorized_access(ad_views.add_ad("resume")), name="add_resume"),
     path('account/add_vacancy/',
         unauthorized_access(ad_views.add_ad("vacancy")), name="add_vacancy"),
     path('account/delete_ad/<int:ad_id>/',
         unauthorized_access(ad_views.delete_ad), name='delete_ad'),
     path('account/edit_resume/<int:ad_id>/',
         unauthorized_access(ad_views.edit_ad('resume')), name='edit_resume'),
     path('account/edit_vacancy/<int:ad_id>/',
         unauthorized_access(ad_views.edit_ad('vacancy')), name='edit_vacancy'),


     # pide(deal) views
     path('pide/<int:ad_id>/', pide_views.pide, name='pide'),
     path('pide_confirm/<int:pide_id>/',
         unauthorized_access(pide_views.pide_confirm), name='pide_confirm'),
     path('feed/', unauthorized_access(pide_views.feed), name='feed'),


     # one big filter search view
     path(
        '/'.join([
            'search',
            'type_<str:_type>',
            'text_<str:_text>',
            '_'.join([
                'salary',
                '<str:_salary_from>',
                '<str:_salary_to>',
                '<str:_currency>',
            ]),
            'without_salary_<str:_without_salary>',
            '_'.join([
                'experience',
                '<str:_experience_from>',
                '<str:_experience_to>',
                '<str:_experience_type>',
            ]),
            'without_experience_<str:_without_experience>',
            'city_<str:_city>',
            'order_by_<str:_order_by>/',
            ]), search_views.search, name = 'filtered_search'),

     # text search
     path('search/type_<str:_type>/text_<str:_text>/', search_views.search, name="text_search"),
]
