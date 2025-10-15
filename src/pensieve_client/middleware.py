# src/pulsegrid_client/middleware.py

import time
import requests

from django.conf import settings

class PulseGridMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start the timer just before the view is called
        start_time = time.time()

        # Process the request and get the response
        response = self.get_response(request)

        # Stop the timer after the response is generated
        end_time = time.time()

        # Calculate duration in milliseconds
        duration_ms = (end_time - start_time) * 1000

        # Get config from the host project's settings.py
        api_key = getattr(settings, "PULSEGRID_API_KEY", None)
        ingest_url = getattr(settings, "PULSEGRID_URL", None)

        if not api_key or not ingest_url:
            print("api key or ingest url not provided")
            # Silently fail if not configured, to avoid crashing the host app
            return response

        # Prepare the data payload
        payload = {
            "type": "performance",
            "payload": {
                "url": request.path,
                "method": request.method,
                "status_code": response.status_code,
                "duration_ms": int(duration_ms)
            }
        }

        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

        try:
            # Send the data to the server.
            # A timeout is crucial to prevent the host app from hanging.
            requests.post(ingest_url, json=payload, headers=headers, timeout=1.0)
        except requests.RequestException as e:
            # If the server is down, we should not crash the host application.
            # In a real version, you might add logging here.
            pass

        return response
