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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'errors/<str:group_hash>/',
                self.admin_site.admin_view(self.error_detail_view),
                name='pensieve-error-detail',
            ),
        ]
        return custom_urls + urls


    def error_detail_view(self, request, group_hash):
        """The view for our error detail page."""
        from django.conf import settings
        from datetime import datetime
        
        api_key = getattr(settings, "PENSIEVE_API_KEY", None)
        
        # Fetch data for this specific error
        error_data = fetch_dashboard_data_from_pensieve_api(
            f"errors/{group_hash}"
        )
        
        # Format dates if they exist
        if error_data:
            for date_field in ['first_seen', 'last_seen']:
                if date_field in error_data and error_data[date_field]:
                    try:
                        # Try parsing ISO format datetime string
                        dt = datetime.fromisoformat(error_data[date_field].replace('Z', '+00:00'))
                        error_data[date_field] = dt.strftime('%B %d, %Y, %I:%M %p')
                    except (ValueError, AttributeError):
                        # If parsing fails, keep the original value
                        pass
        
        context = {
            **self.get_model_perms(request),
            'title': 'Error Details',
            'error_data': error_data,
            'has_view_permission': self.has_view_permission(request)
        }
        return render(request, 'pensieve_client/error_detail.html', context)
    
    def changelist_view(self, request, extra_context=None):
        """This is the main dashboard view for the client."""
        from datetime import datetime

        # 1. Get the URL filter from the request's GET parameters
        url_filter = request.GET.get('url_filter', '')
        
        error_data = fetch_dashboard_data_from_pensieve_api("errors")
        
        # Format dates in error_data
        if error_data and isinstance(error_data, list):
            for error in error_data:
                for date_field in ['first_seen', 'last_seen']:
                    if date_field in error and error[date_field]:
                        try:
                            # Try parsing ISO format datetime string
                            dt = datetime.fromisoformat(error[date_field].replace('Z', '+00:00'))
                            error[date_field] = dt.strftime('%B %d, %Y, %I:%M %p')
                        except (ValueError, AttributeError):
                            # If parsing fails, keep the original value
                            pass

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