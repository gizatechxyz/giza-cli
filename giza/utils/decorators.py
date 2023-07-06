from functools import wraps
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from giza.client import ApiClient


def auth(func: Callable):
    """
    Check that we have the token and it is not expired before executing

    Expects to be called from an instance of ApiClient to and endpoint that needs authorization
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        self_: ApiClient = args[0]

        self_.retrieve_token()

        if self_.token is not None:
            expired = self_._is_expired(self_.token)

        if self_.token is None or expired:
            raise Exception("Token expired or not set. Log in again.")
        return func(*args, **kwargs)

    return wrapper
