from unittest.mock import patch

import pytest

from giza.utils.echo import Echo


def test_format_message():
    """
    Test that the formatting is as expected
    """

    echo = Echo()

    formated_message = echo.format_message("Dummy message")

    assert "[orange3]" in formated_message
    assert "[giza]" in formated_message
    assert "Dummy message" in formated_message


def test_format_debug():
    """
    Test that the formatting is as expected when using a debug formatting
    """

    echo = Echo()

    formated_message = echo.format_debug("Dummy message")

    assert "[red]" in formated_message
    assert "[giza-debug]" in formated_message
    assert "Dummy message" in formated_message


def test_format_error():
    """
    Test that the formatting is as expected when using a debug formatting
    """

    echo = Echo()

    formated_message = echo.format_error("Dummy message")

    assert "[red]" in formated_message
    assert "[ERROR]" in formated_message
    assert "Dummy message" in formated_message


def test_echo_ok():
    """
    Test that the echo is successfully calling rich print
    """

    echo = Echo()
    message = "Dummy Message"
    formatted = f"[red]{message}[/red]"
    with patch("giza.utils.echo.rich_print") as print_mock:
        echo.echo(message, formatted)
        print_mock.assert_called_once_with(formatted)


def test_echo_ok_fallback(capsys):
    """
    Test that the echo is successfully calling rich print
    """

    echo = Echo()
    message = "Dummy Message"
    formatted = f"[red]{message}[/red]"
    with patch("giza.utils.echo.rich_print", side_effect=UnicodeError):
        echo.echo(message, formatted)

    captured = capsys.readouterr()

    assert "[giza]" in captured.out
    assert message in captured.out


@pytest.mark.parametrize("method", ["info", "debug", "info"])
def test_echo_methods(method):
    """
    Test that the echo methods successfully call the main `echo` method
    """
    echo = Echo()
    echo_func = getattr(echo, method)
    with patch("giza.utils.echo.Echo.echo") as mock_echo:
        echo_func("Dummy message")

    mock_echo.assert_called_once()


def test_echo__call():
    """
    Test that the `__call__` soes indeed call the `info` method
    """
    echo = Echo()
    with patch("giza.utils.echo.Echo.info") as mock_echo:
        echo("Message")

    mock_echo.assert_called_once_with("Message")
