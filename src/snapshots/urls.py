from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.repos, name='repos'),
    path('<str:absolPath>/', views.snapshots, name='snapshots')
]
