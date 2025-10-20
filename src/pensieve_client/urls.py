# src/pensieve_client/urls.py

from django.urls import path
from . import views

app_name = 'pensieve_client'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
]