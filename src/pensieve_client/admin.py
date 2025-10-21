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

        # 1. Get the URL filter from the request's GET parameters
        url_filter = request.GET.get('url_filter', '')
        
        error_data = fetch_dashboard_data_from_pensieve_api("errors")

        metric_data = []
        top_slow_endpoints = []

        # 2. Prepare the filter dictionary for the API call
        if url_filter:
            metric_filters = {'url': url_filter}
            metric_data = fetch_dashboard_data_from_pensieve_api("metrics", metric_filters)
        else:
            top_slow_endpoints = fetch_dashboard_data_from_pensieve_api("metrics/top-endpoints")

        context = {
            **self.get_model_perms(request),
            'title': 'Pensieve Dashboard',
            'error_data': error_data,
            'metric_data': metric_data,
            'top_slow_endpoints': top_slow_endpoints,
            'current_url_filter': url_filter,
            'has_view_permission': self.has_view_permission(request)
        }
        return render(request, 'pensieve_client/dashboard.html', context)