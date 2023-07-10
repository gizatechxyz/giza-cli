from functools import wraps
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from giza.client import ApiClient


def auth(func: Callable):
    """
    Check that we have the token and it is not expired before executing

    Expects to be called from an instance of ApiClient to and endpoint that needs authorization

    Args:
        func (Callable): function to decorate

    Returns:
        Callable: decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        """
        Get the API client from the function and retrieve the token, check expiry.

        Args:
            args (Tuple): positional arguments of the function
            kwargs (Dict): keyword arguments fo the decorated function

        Raises:
            Exception: When the token is expired or it does not exist.

        Returns:
            Any: result of the function
        """
        self_: ApiClient = args[0]

        self_.retrieve_token()

        if self_.token is not None:
            expired = self_._is_expired(self_.token)

        if self_.token is None or expired:
            raise Exception("Token expired or not set. Log in again.")
        return func(*args, **kwargs)

    return wrapper
