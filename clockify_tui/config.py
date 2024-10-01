"""Code for loading and parsing the config file."""

import os
import platform
import subprocess as sp
import tomllib
from collections.abc import Sequence
from importlib import resources
from pathlib import Path
from shutil import copyfile

from platformdirs import user_config_path
from pydantic import BaseModel, ConfigDict, field_validator


class Clockify(BaseModel):
    """The clockify section of the configuration file."""

    api_key: str

    @field_validator("api_key")
    @classmethod
    def api_key_must_not_be_empty(cls, v: str) -> str:
        """Ensure that the user has not provided an empty API key."""
        if not v:
            raise ValueError("API key cannot be empty")
        return v


class Config(BaseModel):
    """The program configuration."""

    model_config = ConfigDict(from_attributes=True)
    clockify: Clockify


def _get_config_template_path() -> Path:
    """Get the path to the config template file."""
    return (
        Path(str(resources.files("clockify_tui").joinpath()))
        / "data"
        / "config_template.toml"
    )


def _get_or_create_config_file_path() -> Path:
    """Get the path to the config file, creating it if it doesn't exist.

    The data/config_template.toml file will be used as a template.
    """
    path = user_config_path("clockify-tui", ensure_exists=True) / "config.toml"
    if not path.exists():
        template_path = _get_config_template_path()
        copyfile(template_path, path)
    return path


def read_config() -> Config:
    """Read the program's configuration file from the default location.

    If the file does not exist, a default one will be created.
    """
    with _get_or_create_config_file_path().open("rb") as file:
        config = tomllib.load(file)

    return Config.model_validate(config)


def _get_platform_open_command() -> Sequence[str]:
    """Get the command used to open a file with the default app on this platform."""
    match platform.system():
        case "Windows":
            return ("cmd", "/C", "start")
        case "Darwin":
            return ("open",)
        case _:
            return ("xdg-open",)


def _try_get_editor_from_env() -> Sequence[str] | None:
    """Try to get the preferred editor from the EDITOR environment variable.

    If this variable is not set, return None.
    """
    try:
        return os.environ["EDITOR"].split(" ")
    except KeyError:
        return None


def edit_config() -> None:
    """Edit the configuration file."""
    # Ensure that config file exists
    config_path = _get_or_create_config_file_path()
    print(f"Config file is at {config_path}")

    # Figure out what command to use to edit the file
    editor_command = _try_get_editor_from_env() or _get_platform_open_command()

    # Run the editor
    sp.run((*editor_command, config_path), check=True)
