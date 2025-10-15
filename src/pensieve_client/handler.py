import traceback

def format_exception_data(exc, context):
    """Formats an exception into a dictionary for our API."""

    # traceback.format_exc() gives us the full, formatted stack trace string.
    formatted_traceback = "".join(traceback.format_exception(exc.__class__, exc, exc.__traceback__))

    payload = {
        "error_type": exc.__class__.__name__,
        "error_message": str(exc),
        "traceback": formatted_traceback,
    }
    return payload