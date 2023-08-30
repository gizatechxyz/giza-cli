import re

from giza.exceptions import PasswordError


def _check_password_strength(password: str) -> None:
    """
    Check if the password meets the requirements.

    Args:
        password (str): password to check

    Raises:
        PasswordError: if the password does not meet the requirements
    """
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d#?!@$%^&*-_]{8,}$"
    if not re.match(regex, password):
        raise PasswordError(
            "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter and one number."
        )
