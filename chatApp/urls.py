from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('',views.login),
    path('login',views.login,name='login-page'),
    path('user_login',views.login,name='login-user'),
    path('home',views.home,name='home-page'),
    path('logout',views.logout,name='logout'),
    path('send_message',views.send_message,name='send_message'),
    path('load_more',views.load_more,name='load_more'),
    path('load_more/<int:pk>',views.load_more),
]
