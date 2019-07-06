from django.urls import path
from RetinaScrApp import views
from RetinaScrApp.views import requestAjax, compileCode

urlpatterns = [
    path('', views.index, name='index'),
    path('diagnosis', views.diagnosis, name='diagnosis'),
    path('new_algorithm', views.new_algorithm, name='new_algorithm'),
    path('data_ajax_request', requestAjax, name='data_ajax_request'),
    path('code_editor_ajax_request', compileCode, name='code_editor_ajax_request'),
]
