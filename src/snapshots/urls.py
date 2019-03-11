from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.snapshot, name='snapshot'),
    path('<str:absolPath>/', views.snapshots, name='snapshots'),
    path('<str:absolPath>/restore/<str:snapID>', views.restore, name='restore'),
    path('<str:absolPath>/delete/<str:snapID>', views.delete, name='delete')
]
