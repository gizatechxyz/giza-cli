from unittest.mock import patch

import pytest
from requests.exceptions import HTTPError

from giza.cli.commands.reset_password import handle_http_error, prompt_for_input
from tests.conftest import invoke_cli_runner


# Test for successful request of reset password token
def test_request_reset_password_token_success():
    with patch(
        "giza.cli.client.UsersClient.request_reset_password_token"
    ) as mock_request_token, patch(
        "typer.prompt",
        return_value="test@test.com",
    ):
        result = invoke_cli_runner(["request-reset-password-token"])

    mock_request_token.assert_called_once()
    assert result.exit_code == 0
    assert "Please check your email for a password reset token" in result.stdout


# Test for HTTP error during request of reset password token
def test_request_reset_password_token_http_error():
    with patch(
        "giza.cli.client.UsersClient.request_reset_password_token",
        side_effect=HTTPError,
    ) as mock_request_token, patch(
        "typer.prompt",
        return_value="test@test.com",
    ), patch(
        "giza.cli.commands.reset_password.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(
            ["request-reset-password-token"], expected_error=True
        )

    mock_request_token.assert_called_once()
    assert result.exit_code == 1
    assert "Could not request the reset token" in result.stdout


# Test for successful password reset
def test_reset_password_success():
    with patch(
        "giza.cli.client.UsersClient.reset_password"
    ) as mock_reset_password, patch(
        "typer.prompt",
        side_effect=["request-reset-password-token", "New_password1", "New_password1"],
    ):
        result = invoke_cli_runner(["reset-password"])

    mock_reset_password.assert_called_once()
    assert result.exit_code == 0
    assert "Password reset was successful" in result.stdout


# Test for mismatched passwords during password reset
def test_reset_password_passwords_do_not_match():
    with patch(
        "typer.prompt",
        side_effect=[
            "request-reset-password-token",
            "new_password",
            "different_password",
        ],
    ):
        result = invoke_cli_runner(["reset-password"], expected_error=True)

    assert result.exit_code == 1
    assert "Passwords do not match" in result.stdout


# Test for invalid password during password reset
def test_reset_password_invalid_password():
    with patch(
        "typer.prompt",
        side_effect=["reset_token", "short", "short"],
    ):
        result = invoke_cli_runner(["reset-password"], expected_error=True)

    assert result.exit_code == 1
    assert "Password does not meet the requirements" in result.stdout


# Test for HTTP error during password reset
def test_reset_password_http_error():
    with patch(
        "giza.cli.client.UsersClient.reset_password", side_effect=HTTPError
    ) as mock_reset_password, patch(
        "typer.prompt",
        side_effect=["reset_token", "New_password1", "New_password1"],
    ), patch(
        "giza.cli.commands.reset_password.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(["reset-password"], expected_error=True)

    mock_reset_password.assert_called_once()
    assert result.exit_code == 1
    assert "Could not reset the password" in result.stdout


# Test for handling HTTP error
def test_handle_http_error():
    with patch("giza.cli.commands.reset_password.echo.error") as mock_echo_error, patch(
        "giza.cli.commands.reset_password.get_response_info", return_value={}
    ), pytest.raises(HTTPError):
        handle_http_error(HTTPError("error"), "Test error", True)
        assert mock_echo_error.call_count == 5


# Test for prompt input
def test_prompt_for_input():
    with patch("typer.prompt", return_value="test input") as mock_prompt:
        result = prompt_for_input("Test prompt")
        mock_prompt.assert_called_once_with("Test prompt", type=str, hide_input=False)
        assert result == "test input"


# Test for hidden prompt input
def test_prompt_for_input_hidden():
    with patch("typer.prompt", return_value="hidden input") as mock_prompt:
        result = prompt_for_input("Test prompt", hide_input=True)
        mock_prompt.assert_called_once_with("Test prompt", type=str, hide_input=True)
        assert result == "hidden input"


# Test for integer type prompt input
def test_prompt_for_input_type_int():
    with patch("typer.prompt", return_value="123") as mock_prompt:
        result = prompt_for_input("Test prompt", type=int)
        mock_prompt.assert_called_once_with("Test prompt", type=int, hide_input=False)
        assert result == "123"


# Test for failed prompt input
def test_prompt_for_input_fail():
    with patch("typer.prompt", side_effect=Exception("Test exception")) as mock_prompt:
        try:
            prompt_for_input("Test prompt")
        except Exception as e:
            assert str(e) == "Test exception"
        mock_prompt.assert_called_once_with("Test prompt", type=str, hide_input=False)
