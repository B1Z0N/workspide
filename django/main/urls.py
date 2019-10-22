from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from . import search_views, account_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    
    path('signup/register/', account_views.register, name='register'),
    path('signup/', include('django.contrib.auth.urls')),
    path('account/', account_views.account, name='account'),

    path('signup/activate_mail/<str:uidb64>/<str:token>', account_views.activate_mail, name='activate_main'),
    path('account/delete/<str:uidb64>/<str:token>', account_views.delete_account, name='submit_deletion'),

    path('search/<str:_type>/<str:_text>/', search_views.search, name='search_text'),
    path('search/<str:_type>/', search_views.empty_search, name='search_default'),
]
