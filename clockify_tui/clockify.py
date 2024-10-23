"""Connect to the Clockify API."""

from clockify_api_client.client import ClockifyAPIClient

API_URL = "api.clockify.me/v1"


def get_client(api_key: str) -> ClockifyAPIClient:
    """Get an API client using the specified API key."""
    return ClockifyAPIClient().build(api_key, API_URL)
