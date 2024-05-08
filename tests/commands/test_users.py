from unittest.mock import patch

from email_validator import EmailNotValidError
from pydantic import ValidationError
from requests import HTTPError

from giza.client import UsersClient
from giza.schemas.users import UserResponse
from tests.conftest import invoke_cli_runner


def test_users_create():
    # `input` for invoke was stuck on pytest, better to directly patch the prompt
    with patch.object(UsersClient, "create") as mock_create, patch(
        "typer.prompt",
        side_effect=[
            "gizabrain",
            "Gizapassword1",
            "Gizapassword1",
            "giza@gizatech.xyz",
        ],
    ):
        result = invoke_cli_runner(["users", "create"])

    assert result.exit_code == 0
    mock_create.assert_called_once()
    assert "User created" in result.stdout


def test_users_create_different_passwords():
    # `input` for invoke was stuck on pytest, better to directly patch the prompt
    with patch(
        "typer.prompt",
        side_effect=[
            "gizabrain",
            "12345678aA",
            "12345678aB",
            None,
        ],
    ):
        result = invoke_cli_runner(["users", "create"], expected_error=True)

    assert result.exit_code == 1
    assert "Passwords do not match" in result.stdout


def test_users_create_invalid_password():
    with patch(
        "typer.prompt",
        side_effect=[
            "gizabrain",
            "1234567",
            "1234567",
            None,
        ],
    ):
        result = invoke_cli_runner(["users", "create"], expected_error=True)

    assert result.exit_code == 1
    assert "Password must be at least 8 characters long" in result.stdout


def test_users_create_empty_email():
    # `input` for invoke was stuck on pytest, better to directly patch the prompt
    with patch(
        "typer.prompt",
        side_effect=["gizabrain", "Gizapassword1", "Gizapassword1", None],
    ):
        result = invoke_cli_runner(["users", "create"], expected_error=True)

    assert result.exit_code == 1
    assert "Review the provided information" in result.stdout
    assert "Input should be a valid string" in result.stdout


def test_users_create_invalid_email():
    # `input` for invoke was stuck on pytest, better to directly patch the prompt
    with patch(
        "typer.prompt",
        side_effect=["gizabrain", "Gizapassword1", "Gizapassword1", "notanemail"],
    ):
        result = invoke_cli_runner(["users", "create"], expected_error=True)

    assert result.exit_code == 1
    assert "Review the provided information" in result.stdout
    assert "value is not a valid email address" in result.stdout


def test_users_create_invalid_email_debug():
    # `input` for invoke was stuck on pytest, better to directly patch the prompt
    with patch(
        "typer.prompt",
        side_effect=["gizabrain", "Gizapassword1", "Gizapassword1", "notanemail"],
    ):
        result = invoke_cli_runner(["users", "create", "--debug"], expected_error=True)

    assert result.exit_code == 1
    assert "Review the provided information" in result.stdout
    assert "Debugging mode is on" in result.stdout
    assert isinstance(result.exception, ValidationError)


def test_users_create_invalid_response():
    # `input` for invoke was stuck on pytest, better to directly patch the prompt
    with patch(
        "typer.prompt",
        side_effect=[
            "gizabrain",
            "Gizapassword1",
            "Gizapassword1",
            "giza@gizatech.xyz",
        ],
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
        "typer.prompt",
        side_effect=["gizabrain", "gizapassword"],
    ):
        result = invoke_cli_runner(["users", "login"], expected_error=True)

    mock_login.assert_called_once()
    assert result.exit_code == 0


def test_users_login_no_auth():
    with patch(
        "giza.client.UsersClient.retrieve_token", side_effect=HTTPError
    ) as mock_login, patch(
        "typer.prompt",
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
        "typer.prompt",
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


def test_resend_email_success():
    # Test successful email resend
    with patch("giza.client.UsersClient.resend_email") as mock_resend, patch(
        "typer.prompt",
        return_value="giza@gizatech.xyz",
    ), patch("giza.commands.users.validate_email") as mock_validate:
        result = invoke_cli_runner(["users", "resend-email"])

    mock_resend.assert_called_once()
    mock_validate.assert_called_once()
    assert result.exit_code == 0
    assert "Verification email resent" in result.stdout


def test_resend_email_invalid_email():
    # Test invalid email for resend
    with patch(
        "typer.prompt",
        return_value="notanemail",
    ):
        result = invoke_cli_runner(["users", "resend-email"], expected_error=True)

    assert result.exit_code == 1
    assert "Could not resend" in result.stdout
    assert "The email address is not valid." in result.stdout


def test_resend_email_invalid_email_debug():
    # Test invalid email for resend with debug mode
    with patch(
        "typer.prompt",
        return_value="notanemail",
    ):
        result = invoke_cli_runner(
            ["users", "resend-email", "--debug"], expected_error=True
        )

    assert result.exit_code == 1
    assert "Could not resend" in result.stdout
    assert "Debugging mode is on" in result.stdout
    assert isinstance(result.exception, EmailNotValidError)


def test_resend_email_invalid_response():
    # Test invalid response from server
    with patch(
        "typer.prompt",
        return_value="giza@gizatech.xyz",
    ), patch.object(
        UsersClient, "resend_email", side_effect=HTTPError
    ), patch("giza.commands.users.get_response_info", return_value={}), patch(
        "giza.commands.users.validate_email"
    ) as mock_validate:
        result = invoke_cli_runner(
            ["users", "resend-email", "--debug"], expected_error=True
        )

    mock_validate.assert_called_once()
    assert result.exit_code == 1
    assert "Could not resend the email" in result.stdout
    assert "Debugging mode is on" in result.stdout
    assert isinstance(result.exception, HTTPError)
