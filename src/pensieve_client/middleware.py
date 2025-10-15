# src/pensieve_client/middleware.py

import time
import requests
from django.conf import settings
from .handler import format_exception_data

class PensieveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_key = getattr(settings, "PENSIEVE_API_KEY", None)
        self.ingest_url = getattr(settings, "PENSIEVE_URL", None)

    def __call__(self, request):
        # Start the timer just before the view is called
        start_time = time.time()
                
        # Process the request and get the response
        response = self.get_response(request)

        duration_ms = (time.time() - start_time) * 1000
        
        performance_payload = {
            "url": request.path,
            "method": request.method,
            "status_code": response.status_code,
            "duration_ms": int(duration_ms)
        }
        self.send_data("performance", performance_payload)

        return response

    def process_exception(self, request, exception):
        """
        This method is called by Django when a view raises an exception.
        """

        if self.api_key and self.ingest_url:
            error_payload = format_exception_data(exception, None)
            error_payload.update({
                "url": request.path,
                "method": request.method,
            })
            self.send_data("error", error_payload)
        
        # Return None to allow Django's default exception handling to continue
        # (e.g., show the debug page).
        return None


    def send_data(self, payload_type, payload_data):
        """A helper method to send data to the ingest server."""
        payload = {
            "type": payload_type,
            "payload": payload_data
        }
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        try:
            requests.post(self.ingest_url, json=payload, headers=headers, timeout=1.0)
        except requests.RequestException as e:
            print(f"Failed to send data to Pensieve: {e}")
            pass