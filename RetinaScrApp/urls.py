from django.urls import path
from RetinaScrApp import views
from RetinaScrApp.views import requestAjax

urlpatterns = [
    path('', views.index, name='index'),
    path('diagnosis', views.diagnosis, name='diagnosis'),
    path('data_ajax_request', requestAjax, name='data_ajax_request'),
]
