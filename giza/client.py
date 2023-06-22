import copy
import json
import os
from pathlib import Path
from typing import BinaryIO
from urllib.parse import urlparse

from jose import jwt
from jose.exceptions import ExpiredSignatureError
from requests import Session
from rich import print

from giza.schemas import users
from giza.schemas.token import TokenResponse
from giza.utils.decorators import auth

DEFAULT_API_VERSION = "v1"
GIZA_TOKEN_VARIABLE = "GIZA_TOKEN"


class ApiClient:
    """
    Implementation of the API client to interact with core-services
    """

    def __init__(
        self,
        host: str,
        token: str = None,
        api_version: str = DEFAULT_API_VERSION,
        verify: bool = True,
    ) -> None:
        self.session = Session()
        if host[-1] == "/":
            host = host[:-1]
        parsed_url = urlparse(host)

        self.url = f"{parsed_url.scheme}://{parsed_url.hostname}/api/{api_version}"

        if token is not None:
            headers = {"Authorization": "Bearer {token}", "Content-Type": "text/json"}
        else:
            headers = {}

        self.default_headers = {}
        self.default_headers.update(headers)
        self.verify = verify
        self.giza_dir = Path.home() / ".giza"
        self._default_credentials = self._load_credentials_file()

    def _load_credentials_file(self):
        if (self.giza_dir / ".credentials.json").exists():
            with open(self.giza_dir / ".credentials.json") as f:
                credentials = json.load(f)
        else:
            credentials = {}
        return credentials

    def _get_oauth(self, user: str, password: str):
        """
        Retrieve JWT token

        Args:
            user (str): _description_
            password (str): _description_
        """

        if user is None or password is None:
            raise ValueError("Missing credentials")

        user_login = users.UserLogin(username=user, password=password)
        response = self.session.post(
            f"{self.url}/login/access-token",
            data=user_login.dict(),
        )
        response.raise_for_status()
        try:
            token = TokenResponse(**response.json())
        except json.JSONDecodeError:
            print(response.text)
            print(f"Status Code -> {response.status_code}")

        self.token = token.access_token

    def _write_credentials(self, **kwargs):
        if self.token is not None:
            if not self.giza_dir.exists():
                self.giza_dir.mkdir()
            kwargs.update({"token": self.token})
            with open(self.giza_dir / ".credentials.json", "w") as f:
                json.dump(kwargs, f, indent=4)

    def _is_expired(self, token: str):
        try:
            jwt.decode(
                token,
                "",
                algorithms=["HS256"],
                options={"verify_signature": False},
            )
            return False
        except ExpiredSignatureError:
            print("Signature has expired. Renew it with default login.")
            return True

    def retrieve_token(
        self,
        user: str = None,
        password: str = None,
        renew: bool = False,
    ):
        """
        Get the JWT token.

        First,  it will try to get it from GIZA_TOKEN.
        Second, from ~/.giza/.credentials.json.
        And finally it will try to retrieve it from the API login the user in.
        """

        token = os.environ.get(GIZA_TOKEN_VARIABLE)

        if token is None and len(self._default_credentials) != 0 and not renew:
            # Try with the home folder
            if "token" in self._default_credentials:
                token = self._default_credentials.get("token")
                user_cred = self._default_credentials.get("user")

                # Different users but credentials file exists make sure we ask for the new JWT
                if user is not None and user != user_cred:
                    token = None
        if token is not None and not self._is_expired(token) and not renew:
            self.token = token

        if token is None and user is not None and password is not None:
            self._get_oauth(user, password)
            self._write_credentials(user=user)

        if self.token is None:
            raise Exception(
                "Token is expired or could not retrieve it. "
                "Please get a new one using `user` and `password`.",
            )


class UsersClient(ApiClient):
    """
    Client to interact with `users` endpoint.
    """

    USERS_ENDPOINT = "users"

    def create(self, user: users.UserCreate):
        response = self.session.post(
            f"{self.url}/{self.USERS_ENDPOINT}/",
            json=user.dict(exclude_unset=True),
        )

        body = response.json()
        print(body)
        return users.UserResponse(**body)

    @auth
    def me(self):
        headers = copy.deepcopy(self.default_headers)
        headers.update(
            {"Authorization": f"Bearer {self.token}", "Content-Type": "text/json"},
        )
        response = self.session.get(
            f"{self.url}/{self.USERS_ENDPOINT}/me",
            headers=headers,
        )
        return users.UserResponse(**response.json())


class TranspileClient(ApiClient):
    """
    Client to interact with `users` endpoint.
    """

    TRANSPILE_ENDPOINT = "transpile"

    @auth
    def transpile(self, f: BinaryIO):
        headers = copy.deepcopy(self.default_headers)
        headers.update(
            {"Authorization": f"Bearer {self.token}", "Content-Type": "text/json"},
        )

        response = self.session.post(
            f"{self.url}/{self.TRANSPILE_ENDPOINT}",
            files={"": f},
        )
        return response.content
