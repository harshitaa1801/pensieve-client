import requests
from django.conf import settings


def fetch_dashboard_data_from_pensieve_api(resource):
    """
    Fetches real data from the main Pensieve server API.
    """
    # Get the base URL from the user's settings.py
    base_url = getattr(settings, "PENSIEVE_URL", "").replace('/ingest/', '')
    api_key = getattr(settings, "PENSIEVE_API_KEY", None)

    if not api_key or not base_url:
        return []

    headers = {"X-API-KEY": api_key}
    api_url = f"{base_url}/{resource}/" # e.g., http://.../api/errors/

    try:
        response = requests.get(api_url, headers=headers, timeout=3.0)
        response.raise_for_status()  # Raises an exception for 4xx/5xx errors
        return response.json()
    except requests.RequestException:
        # If the API call fails, return an empty list to prevent crashing
        return []    
