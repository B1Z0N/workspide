from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import login
from . import search_views, account_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    
    path('signup/register/', account_views.register, name='register'),
    path('signup/activate_mail/<str:uidb64>/<str:token>', account_views.activate_mail, name='activate'),
    path('account/delete/<str:uidb64>/<str:token>', account_views.delete_account, name='activate'),
    path('signup/', include('django.contrib.auth.urls')),
    path('account/', account_views.account),

    path('search/<str:_type>/<str:_text>/', search_views.search),
    path('search/<str:_type>/', search_views.empty_search),
]
