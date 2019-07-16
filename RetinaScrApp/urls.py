from django.urls import path, include
from RetinaScrApp import views
from RetinaScrApp.views import requestAjax, compileCode

urlpatterns = [
    path('', views.index, name='index'),
    path('diagnosis', views.diagnosis, name='diagnosis'),
    path('customize_algorithm', views.customize_algorithm, name='customize_algorithm'),
    path('new_algorithm', views.new_algorithm, name='new_algorithm'),
    path('how_it-works', views.how_it_works, name='how_it_works'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('data_ajax_request', requestAjax, name='data_ajax_request'),
    path('code_editor_ajax_request', compileCode, name='code_editor_ajax_request'),
    path('accounts/', include('allauth.urls')),
]
