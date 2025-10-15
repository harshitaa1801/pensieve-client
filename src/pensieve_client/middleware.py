# src/pulsegrid_client/middleware.py

import time

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

        # For now, we will just print the result to the console.
        # In the next step, we will replace this with a real API call.
        print(f"INFO: Request to {request.path} took {duration_ms:.2f}ms")

        return response
