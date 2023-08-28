import pytest

from giza.exceptions import PasswordError
from giza.utils.misc import _check_password_strength


# Test check strength password
@pytest.mark.parametrize(
    "password",
    [
        "1234567",
        "12345678",
        "abcdefgh",
        "abcdefghi",
        "123456789",
        "abcdefghi",
    ],
)
def test_check_password_strength_raises(password):
    """
    Test check password strength.
    """
    with pytest.raises(PasswordError):
        _check_password_strength(password)


def test__check_password_strength_ok():
    """
    Test that a valid password does not raise an exception.
    """
    _check_password_strength("12345678aA")
