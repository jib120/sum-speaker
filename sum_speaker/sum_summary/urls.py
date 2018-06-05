from django.conf.urls import include, url
from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', views.index, name='index'),
    path('search/view.html', views.search, name='search_view'),
    url(r'^search/view', views.bookmark_register, name="bookmark_register"),
    url(r'^search/bookmark_view$', views.bookmark_view, name='bookmark_view'),
    url(r'^search/bookmark_list$', views.bookmark_list, name='bookmark_list'),
    url(r'^search/bookmark_list/remove$', views.bookmark_remove, name='bookmark_remove'),
    ### for debug ############################################
    path('debug/cleardb', views.cleardb, name='search_view'),
]