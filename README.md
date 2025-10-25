# pensieve-client 🚀

[![PyPI Version](https://img.shields.io/pypi/v/pensieve.svg)](https://pypi.org/project/pensieve/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, Django-first APM and error-tracking client for the **Pensieve** observability platform.

This package is a client library designed to be installed in any Django project. It automatically monitors your application's performance and tracks exceptions.

Its main feature is a **fully integrated Django Admin dashboard**—it adds a "Performance Insights" page directly to your project's *own* admin panel, allowing you to see your site's health without ever leaving your workspace.

## Features ✨

* **📈 Integrated Admin Dashboard:** View error and performance charts directly in your site's `/admin/`.
* **🐛 Automatic Exception Tracking:** Captures and groups unhandled exceptions with full stack traces.
* **⏱️ Performance Monitoring:** Tracks request/response times for all your views.
* **📊 Interactive Charts:** Provides a "Top 5 Slowest Endpoints" summary and interactive, filterable line charts for drilling down into a specific URL's performance history.
* **⚙️ Lightweight & Configurable:** Designed to be low-overhead. Automatically excludes its own dashboard URLs from being monitored.

## Installation


1.  Install the package using pip:
    ```bash
    pip install pensieve
    ```

2.  Add `pensieve_client` to your `INSTALLED_APPS` in `settings.py`.
    ```python
    # settings.py

    INSTALLED_APPS = [
        # ... other apps
        'django.contrib.admin',
        'django.contrib.auth',
        # ...
        'pensieve_client',
    ]
    ```

3.  Add the Pensieve middleware to your `settings.py`. It's recommended to place it at the **bottom** of the list to ensure it correctly wraps your views.
    ```python
    # settings.py

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        # ... other middleware
        'pensieve_client.middleware.PensieveMiddleware', # <-- Add this
    ]
    ```

## Configuration

Add the following settings to your project's `settings.py` file:

```python
# settings.py

# Your unique project API key from your Pensieve server dashboard
PENSIEVE_API_KEY = "your-project-api-key-from-pensieve"

# This is the exact url you have to mention in settings.py to get the metrics
PENSIEVE_URL = "[https://pensieve.harshitanjn.tech/api](https://pensieve.harshitajn.tech/api)" 

# (Optional) A list of URL paths to exclude from performance tracking.
# It's a good idea to exclude the admin panel to reduce noise.
PENSIEVEGRID_EXCLUDE_URLS = [
    '/admin/',
    '/__debug__/',
]
```


## How to Use 📊

Once the package is installed and configured:

1.  Run your Django project.

2.  Log in to your project's admin panel (e.g., `http://127.0.0.1:8000/admin/`).

3.  In the admin homepage, you will see a new section (likely "AUTHENTICATION AND AUTHORIZATION") with a link named "Pensieve Dashboards".

4.  Click this link to view your project's performance and error data, which is displayed directly within your own admin.


## License
This project is licensed under the MIT License. See the LICENSE file for details.