# src/pensieve_client/admin.py

from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render
from django.utils.html import format_html

from pensieve_client.utils import fetch_dashboard_data_from_pensieve_api
from .models import MonitoredProject

@admin.register(MonitoredProject)
class MonitoredProjectAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # This is a proxy model, so users can't add new ones.
        return False

    def changelist_view(self, request, extra_context=None):
        """This is the main dashboard view for the client."""

        error_data = fetch_dashboard_data_from_pensieve_api("errors")

        context = {
            **self.get_model_perms(request),
            'title': 'Pensieve Dashboard',
            'error_data': error_data,
            'has_view_permission': self.has_view_permission(request)
        }
        return render(request, 'pensieve_client/dashboard.html', context)