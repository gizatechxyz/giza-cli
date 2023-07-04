from functools import wraps
from typing import Callable


def auth(func: Callable):
    """
    Check that we have the token and it is not expired before executing
    """

    @wraps(func)
    def wrapper(*args, **kargs):
        self_ = args[0]
        self_.retrieve_token()

        if self_.token is not None:
            expired = self_._is_expired(self_.token)

        if self_.token is None or expired:
            raise Exception("Token expired or not set. Log in again.")
        return func(*args, **kargs)

    return wrapper
