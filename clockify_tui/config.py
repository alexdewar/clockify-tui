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


def _get_config_file_path() -> Path:
    """Get the path to the config file.

    If the config directory doesn't exist, it will be created (though not the file
    itself).
    """
    return user_config_path("clockify-tui", ensure_exists=True) / "config.toml"


def _try_get_or_create_config_path() -> Path | None:
    """Try to get the path to the config file.

    If the path exists or the user opts to create it, the path will be returned. If not,
    return None.
    """
    config_path = _get_config_file_path()
    if config_path.exists():
        return config_path

    while True:
        choice = input(
            "Config file doesn't exist. Would you like to create it now? (y/n): "
        )
        match choice.lower():
            case "y":
                edit_config(config_path)
                return config_path
            case "n":
                return None


def _create_config_file_from_template(config_path: Path) -> None:
    """Create a new config file by copying over the template file."""
    template_path = _get_config_template_path()
    copyfile(template_path, config_path)


def try_read_config() -> Config | None:
    """Try to read the program's configuration file from the default location.

    If the file does not exist, the user will be prompted to create it.

    Returns the Config object or None if the user cancels.
    """
    config_path = _try_get_or_create_config_path()
    if not config_path:
        return None

    with config_path.open("rb") as file:
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


def edit_config(config_path: Path | None = None) -> None:
    """Edit the configuration file."""
    if not config_path:
        config_path = _get_config_file_path()

    print(f"Config file is at {config_path}")

    if not config_path.exists():
        _create_config_file_from_template(config_path)

    # Figure out what command to use to edit the file
    editor_command = _try_get_editor_from_env() or _get_platform_open_command()

    # Run the editor
    sp.run((*editor_command, config_path), check=True)
