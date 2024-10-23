"""Connect to the Clockify API."""

from clockify_api_client.client import ClockifyAPIClient

from .config import try_read_config

config = try_read_config()

if config is None:
    raise ValueError("Config file not found.")

API_KEY = config.clockify.api_key
API_URL = "api.clockify.me/v1"

client = ClockifyAPIClient().build(API_KEY, API_URL)
