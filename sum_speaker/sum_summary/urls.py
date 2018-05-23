
from django.urls import path
from . import views

urlpatterns = [
    path('index.html', views.index, name='index'),
    path('search/view.html', views.search, name='search_view'),
]
