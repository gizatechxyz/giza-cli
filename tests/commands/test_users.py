from unittest.mock import patch

from pydantic import ValidationError
from requests import HTTPError

from giza.client import UsersClient
from giza.schemas.users import UserResponse
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
    assert "value is not a valid email address" in result.stdout


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


def test_users_create_invalid_response():
    # `input` for invoke was stuck on pytest, better to directly patch the prompt
    with patch(
        "rich.prompt.Prompt.ask",
        side_effect=["gizabrain", "gizapassword", "giza@gizatech.xyz"],
    ), patch.object(UsersClient, "create", side_effect=HTTPError), patch(
        "giza.commands.users.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(["users", "create", "--debug"], expected_error=True)

    assert result.exit_code == 1
    assert "Could not create the user" in result.stdout
    assert "Debugging mode is on" in result.stdout
    assert isinstance(result.exception, HTTPError)


def test_users_login_successfully():
    with patch("giza.client.UsersClient.retrieve_token") as mock_login, patch(
        "rich.prompt.Prompt.ask",
        side_effect=["gizabrain", "gizapassword"],
    ):
        result = invoke_cli_runner(["users", "login"], expected_error=True)

    mock_login.assert_called_once()
    assert result.exit_code == 0


def test_users_login_no_auth():
    with patch(
        "giza.client.UsersClient.retrieve_token", side_effect=HTTPError
    ) as mock_login, patch(
        "rich.prompt.Prompt.ask",
        side_effect=["gizabrain", "gizapassword"],
    ), patch(
        "giza.commands.users.get_response_info", return_value={}
    ) as mock_info:
        result = invoke_cli_runner(["users", "login"], expected_error=True)

    mock_login.assert_called_once()
    mock_info.assert_called_once()
    assert result.exit_code == 1
    assert "Could not authorize the user" in result.stdout


def test_users_login_no_auth_debug():
    with patch(
        "giza.client.UsersClient.retrieve_token", side_effect=HTTPError
    ) as mock_login, patch(
        "rich.prompt.Prompt.ask",
        side_effect=["gizabrain", "gizapassword"],
    ), patch(
        "giza.commands.users.get_response_info", return_value={}
    ) as mock_info:
        result = invoke_cli_runner(["users", "login", "--debug"], expected_error=True)

    mock_login.assert_called_once()
    mock_info.assert_called_once()
    assert result.exit_code == 1
    assert "Could not authorize the user" in result.stdout
    assert "Debugging mode is on" in result.stdout
    assert isinstance(result.exception, HTTPError)


def test_users_me():
    user_response = UserResponse(
        username="giza", email="giza@gizatech.xyz", is_active=True
    )
    with patch("giza.client.UsersClient.me", return_value=user_response) as mock_me:
        result = invoke_cli_runner(["users", "me"])

    mock_me.assert_called_once()
    assert result.exit_code == 0
    assert "Retrieving information about me" in result.stdout
