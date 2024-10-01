# Clockify TUI

Clockify TUI is an unofficial terminal interface for the [Clockify] time tracking app, written in Python.

While there are [official apps] for a range of platforms, I wanted to make something a bit simpler that can be operated from the terminal. Thankfully, there is a [well-documented public API] we can use. The current plan is to use [`blessed`] for the UI and [`clockify-api-client`] for interactive with the Clockify API.

It is currently under development, but the initial goals of the project are to:

1. Provide a simple terminal UI displaying the current running task and previous tasks
1. Allow for stopping the current task and starting a new one via the keyboard

This will require some additional machinery:

1. A way to select the current workspace ([#4](https://github.com/alexdewar/clockify-tui/issues/4))[^1]
1. A way to obtain a list of projects (required so that the user can start a new task)
1. Some way to store configuration data, such as the API key (a user-configurable TOML file?) ([#3](https://github.com/alexdewar/clockify-tui/issues/3))

I also have some less pressing, nice-to-have features in mind:

1. Allow for opening the web interface from the UI ([#8](https://github.com/alexdewar/clockify-tui/issues/8))
1. Provide a wizard for generating and editing the user config file ([#10](https://github.com/alexdewar/clockify-tui/issues/10))
1. Make the appearance of the app configurable via the config file ([#12](https://github.com/alexdewar/clockify-tui/issues/12))

[Clockify]: https://clockify.me/
[official apps]: https://clockify.me/apps
[well-documented public API]: https://docs.clockify.me/
[`blessed`]: https://pypi.org/project/blessed/
[`clockify-api-client`]: https://pypi.org/project/clockify-api-client/

[^1]: Even if you only ever use one workspace, you still need to tell the Clockify API which workspace that is.

## Getting started

To get started, you will need a Clockify account. You can [sign up for free here].

You will also need to generate an API key so that you can connect to the Clockify API. Once you have created an account and logged in, you can generate a new one in [the advanced tab of the preferences page].

[sign up for free here]: https://app.clockify.me/en/signup
[the advanced tab of the preferences page]: https://app.clockify.me/user/preferences#advanced

## For developers

This is a Python application that uses [poetry](https://python-poetry.org) for packaging
and dependency management. It also provides [pre-commit](https://pre-commit.com/) hooks
for various linters and formatters and automated tests using
[pytest](https://pytest.org/) and [GitHub Actions](https://github.com/features/actions).
Pre-commit hooks are automatically kept updated with a dedicated GitHub Action.

To get started:

1. [Download and install Poetry](https://python-poetry.org/docs/#installation) following the instructions for your OS.
1. Clone this repository and make it your working directory
1. Set up the virtual environment:

   ```bash
   poetry install
   ```

1. Activate the virtual environment (alternatively, ensure any Python-related command is preceded by `poetry run`):

   ```bash
   poetry shell
   ```

1. Install the git hooks:

   ```bash
   pre-commit install
   ```

1. Run the main app:

   ```bash
   python -m clockify_tui
   ```
