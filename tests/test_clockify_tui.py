"""Tests for the main module."""

from clockify_tui import __version__


def test_version():
    """Check that the version is acceptable."""
    assert __version__ == "0.1.0"
