
from django.contrib import admin
from django.urls import path
from . import views
from . import clear_data

urlpatterns = [
    path('', views.settings, name='settings'),
    path('clear_check_data', clear_data.clearData, name='clear_check_data')
]
