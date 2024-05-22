import requests
import semver

from giza.cli import __version__
from giza.cli.utils.echo import Echo


# TODO: Make sure that this works offline, currently it doesn't
def check_version():
    """
    Check if there is a new version available of the cli in pypi to suggest upgrade
    """
    current_version = semver.Version.parse(__version__)
    response = requests.get("https://pypi.org/pypi/giza-cli/json")
    latest_version = semver.Version.parse(response.json()["info"]["version"])

    if latest_version > current_version:
        echo = Echo()
        echo.warning(f"Current version of Giza CLI: {current_version}")
        echo.warning(
            f"A new version ({latest_version}) is available. Please upgrade :bell:"
        )
