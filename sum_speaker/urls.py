from django.conf.urls import include, url
from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('index.html', views.index, name='index'),
    path('search/view.html', views.search, name='search_view'),
]
