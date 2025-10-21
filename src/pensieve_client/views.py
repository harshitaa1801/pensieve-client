# src/pensieve_client/views.py

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from pensieve_client.utils import fetch_dashboard_data_from_pensieve_api

@staff_member_required
def dashboard_view(request):
    """The main dashboard view for the client."""
    error_data = fetch_dashboard_data_from_pensieve_api("errors")
    metric_data = fetch_dashboard_data_from_pensieve_api("metrics")

    context = {
        'title': 'Pensieve Dashboard',
        'error_data': error_data,
        'metric_data': metric_data,
    }
    return render(request, 'pensieve_client/dashboard.html', context)