from django.urls import path, include
from RetinaScrApp import views
from RetinaScrApp.views import requestAjax, compileCode

urlpatterns = [
    path('', views.index, name='index'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('register', views.user_registration, name='user_registration'),
    path('diagnosis', views.diagnosis, name='diagnosis'),
    path('customize_algorithm', views.customize_algorithm, name='customize_algorithm'),
    path('new_algorithm', views.new_algorithm, name='new_algorithm'),
    path('how_it-works', views.how_it_works, name='how_it_works'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('data_ajax_request', requestAjax, name='data_ajax_request'),
    path('code_editor_ajax_request', compileCode, name='code_editor_ajax_request'),
    path('accounts/', include('django.contrib.auth.urls')),
]
