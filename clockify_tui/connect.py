"""Connect to the Clockify API."""

from clockify_api_client.client import ClockifyAPIClient

API_KEY = "YOUR_API_KEY"
API_URL = "api.clockify.me/v1"

client = ClockifyAPIClient().build(API_KEY, API_URL)
