from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import login
from . import search_views, account_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    
    path('signup/register/', account_views.register),
    # path('logout/', ),
    path('signup/', include('django.contrib.auth.urls')),
    path('account/', TemplateView.as_view(template_name='account.html')),

    path('search/<str:_type>/<str:_text>/', search_views.search),
    path('search/<str:_type>/', search_views.empty_search),
]
