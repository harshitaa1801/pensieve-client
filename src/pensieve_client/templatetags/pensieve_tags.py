# src/pensieve_client/templatetags/pensieve_tags.py
from django import template
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

register = template.Library()

@register.filter
def b64encode(value):
    """Base64 encodes a string to be URL-safe."""
    return urlsafe_base64_encode(force_bytes(value))