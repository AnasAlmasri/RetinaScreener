from django.urls import path
from RetinaScrApp import views

urlpatterns = [
    path('', views.index, name='index'),
]