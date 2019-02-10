
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.update, name='update'),
    path('settings/', views.settings, name='settings'),
    path('docs/', views.docs, name='docs')
]
