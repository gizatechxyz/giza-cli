from unittest.mock import patch

from pydantic import ValidationError

from giza.client import UsersClient
from tests.conftest import invoke_cli_runner


def test_users_create():
    # `input` for invoke was stuck on pytest, better to directly patch the prompt
    with patch.object(UsersClient, "create") as mock_create, patch(
        "rich.prompt.Prompt.ask",
        side_effect=["gizabrain", "gizapassword", "giza@gizatech.xyz"],
    ):
        result = invoke_cli_runner(["users", "create"])

    assert result.exit_code == 0
    mock_create.assert_called_once()
    assert "User created" in result.stdout


def test_users_create_empty_email():
    # `input` for invoke was stuck on pytest, better to directly patch the prompt
    with patch(
        "rich.prompt.Prompt.ask", side_effect=["gizabrain", "gizapassword", None]
    ):
        result = invoke_cli_runner(["users", "create"], expected_error=True)

    assert result.exit_code == 1
    assert "Review the provided information" in result.stdout
    assert "none is not an allowed value" in result.stdout


def test_users_create_invalid_email():
    # `input` for invoke was stuck on pytest, better to directly patch the prompt
    with patch(
        "rich.prompt.Prompt.ask",
        side_effect=["gizabrain", "gizapassword", "notanemail"],
    ):
        result = invoke_cli_runner(["users", "create"], expected_error=True)

    assert result.exit_code == 1
    assert "Review the provided information" in result.stdout
    assert "value is not a valid email address" in result.stdout


def test_users_create_invalid_email_debug():
    # `input` for invoke was stuck on pytest, better to directly patch the prompt
    with patch(
        "rich.prompt.Prompt.ask",
        side_effect=["gizabrain", "gizapassword", "notanemail"],
    ):
        result = invoke_cli_runner(["users", "create", "--debug"], expected_error=True)

    assert result.exit_code == 1
    assert "Review the provided information" in result.stdout
    assert "Debugging mode is on" in result.stdout
    assert isinstance(result.exception, ValidationError)
