import copy
import json
import os
from io import BufferedReader
from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional, Tuple
from urllib.parse import urlparse

from jose import jwt
from jose.exceptions import ExpiredSignatureError
from pydantic import SecretStr
from requests import Response, Session
from rich import print, print_json

from giza.schemas import users
from giza.schemas.jobs import Job, JobCreate
from giza.schemas.message import Msg
from giza.schemas.models import Model, ModelCreate, ModelUpdate
from giza.schemas.proofs import Proof
from giza.schemas.token import TokenResponse
from giza.utils import echo
from giza.utils.decorators import auth

DEFAULT_API_VERSION = "v1"
GIZA_TOKEN_VARIABLE = "GIZA_TOKEN"
MODEL_URL_HEADER = "X-MODEL-URL"


class ApiClient:
    """
    Implementation of the API client to interact with core-services
    """

    def __init__(
        self,
        host: str,
        token: Optional[str] = None,
        api_version: str = DEFAULT_API_VERSION,
        verify: bool = True,
        debug: Optional[bool] = False,
    ) -> None:
        self.session = Session()
        if host[-1] == "/":
            host = host[:-1]
        parsed_url = urlparse(host)

        self.url = f"{parsed_url.scheme}://{parsed_url.netloc}/api/{api_version}"

        if token is not None:
            headers = {"Authorization": "Bearer {token}", "Content-Type": "text/json"}
            self.token = token
        else:
            headers = {}

        self.debug = debug
        self.default_headers = {}
        self.default_headers.update(headers)
        self.verify = verify
        self.giza_dir = Path.home() / ".giza"
        self._default_credentials = self._load_credentials_file()

    def _get_auth_header(self) -> Dict[str, str]:
        """
        Generates the authorization header for API requests.

        Returns:
            Dict[str, str]: A dictionary containing the authorization header.
        """

        return {"Authorization": f"Bearer {self.token}"}

    def _echo_debug(self, message: str, json: bool = False) -> None:
        """
        Utility to log debug messages when debug is on

        Args:
            message (str): Message to print when debugging
            json (bool): indicates if the message is a json to treat it as such
        """

        if self.debug:
            print_json(message) if json else echo.debug(message)

    def _load_credentials_file(self) -> Dict:
        """
        Checks if the `~/.giza/.credentials.json` exists to retrieve existing credentials.
        Useful to reuse credentials that are still valid.

        Returns:
            Dict: if the file exists return the credentials from the file if not return an empty dict.
        """
        if (self.giza_dir / ".credentials.json").exists():
            with open(self.giza_dir / ".credentials.json") as f:
                credentials = json.load(f)
                self._echo_debug(
                    f"Credentials loaded from: {self.giza_dir / '.credentials.json'}",
                )
        else:
            credentials = {}
            self._echo_debug("Credentials not found in default directory")

        return credentials

    def _get_oauth(self, user: str, password: str) -> None:
        """
        Retrieve JWT token.

        Args:
            user (str): username used to retrieve the token
            password (str): password to authenticate agains the login endpoint

        Raises:
            json.JSONDecodeError: when the response does not have the expected body
        """

        user_login = users.UserLogin(username=user, password=SecretStr(password))
        response = self.session.post(
            f"{self.url}/login/access-token",
            data={
                "username": user_login.username,
                "password": user_login.password.get_secret_value(),
            },
        )
        response.raise_for_status()
        try:
            token = TokenResponse(**response.json())
        except json.JSONDecodeError:
            # TODO: if response is succesfull (2XX) do we need this?
            print(response.text)
            print(f"Status Code -> {response.status_code}")
            raise

        self.token = token.access_token
        self._echo_debug(response.json(), json=True)
        self._echo_debug(f"Token: {self.token}")

    def _write_credentials(self, **kwargs: Any) -> None:
        """
        Write credentials to the giza credentials file for later retrieval

        Args:
            kwargs(dict): extra keyword arguments to save with the credentials, usually `user`.
        """
        if self.token is not None:
            if not self.giza_dir.exists():
                echo("Creating default giza dir")
                self.giza_dir.mkdir()
            kwargs.update({"token": self.token})
            with open(self.giza_dir / ".credentials.json", "w") as f:
                json.dump(kwargs, f, indent=4)
            echo(f"Credentials written to: {self.giza_dir / '.credentials.json'}")

    def _is_expired(self, token: str) -> bool:
        """
        Check if the token is expired.

        Args:
            token (str): token to check expiry

        Returns:
            bool: if the token has expired
        """
        try:
            jwt.decode(
                token,
                "",
                algorithms=["HS256"],
                options={"verify_signature": False},
            )
            return False
        except ExpiredSignatureError:
            self._echo_debug("Token is expired")
            return True

    def retrieve_token(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        renew: bool = False,
    ) -> None:
        """
        Get the JWT token.

        First,  it will try to get it from GIZA_TOKEN.
        Second, from ~/.giza/.credentials.json.
        And finally it will try to retrieve it from the API login the user in.

        Args:
            user: if provided it will be used to check against current credentials
                  and if provided with `password` used to retrieve a new token.
            password: if provided with `user` it will be used to retrieve a new token.
            renew: for renewal of the JWT token by user login.

        Raises:
            Exception: if token could not be retrieved in any way
        """

        token = os.environ.get(GIZA_TOKEN_VARIABLE)
        if token is None:
            self._echo_debug(
                f"No token found in environment variable {GIZA_TOKEN_VARIABLE}",
            )
        if token is None and len(self._default_credentials) != 0 and not renew:
            # Try with the home folder
            if "token" in self._default_credentials:
                token = self._default_credentials.get("token")
                user_cred = self._default_credentials.get("user")

                # Different users but credentials file exists make sure we ask for the new JWT
                if user is not None and user != user_cred:
                    self._echo_debug(
                        "Logging as a different user, need to retrieve a new token",
                    )
                    token = None

        if token is not None and not self._is_expired(token) and not renew:
            self.token = token

        if (
            getattr(self, "token", None) is None
            and user is not None
            and password is not None
        ):
            self._get_oauth(user, password)
            self._write_credentials(user=user)

        if getattr(self, "token", None) is None:
            raise Exception(
                "Token is expired or could not retrieve it. "
                "Please get a new one using `user` and `password`.",
            )


class UsersClient(ApiClient):
    """
    Client to interact with `users` endpoint.
    """

    USERS_ENDPOINT = "users"

    def create(self, user: users.UserCreate) -> users.UserResponse:
        """
        Call the API to create a new user

        Args:
            user (users.UserCreate): information used to create a new user

        Returns:
            users.UserResponse: the created user information
        """
        response = self.session.post(
            f"{self.url}/{self.USERS_ENDPOINT}/",
            json={
                "username": user.username,
                "password": user.password.get_secret_value(),
                "email": user.email,
            },
        )

        response.raise_for_status()
        body = response.json()
        self._echo_debug(body, json=True)
        return users.UserResponse(**body)

    @auth
    def me(self) -> users.UserResponse:
        """
        Retrieve information about the current user.
        Must have a valid token to perform the operation, enforced by `@auth`

        Returns:
            users.UserResponse: User information from the server
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(
            {"Authorization": f"Bearer {self.token}", "Content-Type": "text/json"},
        )
        response = self.session.get(
            f"{self.url}/{self.USERS_ENDPOINT}/me",
            headers=headers,
        )
        self._echo_debug(response.json(), json=True)
        return users.UserResponse(**response.json())

    def resend_email(self, email: str) -> Msg:
        """
        Resend the verification email to the user.

        Args:
            email (EmailStr): The email of the user who wants to resend the verification email.

        Returns:
            Msg: A message indicating the success or failure of the request.
        """
        try:
            response = self.session.post(
                f"{self.url}/{self.USERS_ENDPOINT}/resend-email",
                json={"email": email},
            )
            response.raise_for_status()
            body = response.json()
            self._echo_debug(body, json=True)
            if response.status_code == 200:
                return Msg(**body)
        except Exception as e:
            self._echo_debug(f"Could not resend the email: {str(e)}")
            raise e
        return Msg(msg="Could not resend the email")

    def request_reset_password_token(self, email: str) -> Msg:
        """
        Sends a request to the server to generate a password reset token.
        The token is sent to the user's email.

        Args:
            email (str): The email of the user who wants to reset their password.

        Returns:
            Msg: A message indicating the success or failure of the request.
        """

        response = self.session.post(
            f"{self.url}/{self.USERS_ENDPOINT}/reset-password-token",
            params={"email": email},
        )

        response.raise_for_status()
        body = response.json()
        self._echo_debug(body, json=True)
        if response.status_code == 200:
            return Msg(**body)
        raise Exception("Could not request a password reset token")

    def reset_password(self, token: str, new_password: str) -> Msg:
        """
        Resets the user's password using the provided token and new password.

        Args:
            token (str): The password reset token sent to the user's email.
            new_password (str): The new password the user wants to set.

        Returns:
            Msg: A message indicating the success or failure of the password reset.
        """

        response = self.session.post(
            f"{self.url}/{self.USERS_ENDPOINT}/reset-password",
            json={"token": token, "new_password": new_password},
        )

        response.raise_for_status()
        body = response.json()
        self._echo_debug(body, json=True)
        if response.status_code == 200:
            return Msg(**body)
        raise Exception("Could not reset the password")


class TranspileClient(ApiClient):
    """
    Client to interact with `users` endpoint.
    """

    TRANSPILE_ENDPOINT = "transpile"

    @auth
    def transpile(self, f: BinaryIO) -> Response:
        """
        Make a call to the API transpile endpoint with the model as a file.

        Args:
            f (BinaryIO): model to send for transpilation

        Returns:
            Response: raw response from the server with the transpiled model as a zip
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())
        response = self.session.post(
            f"{self.url}/{self.TRANSPILE_ENDPOINT}",
            files={"file": f},
            headers=headers,
        )
        self._echo_debug(str(response))

        response.raise_for_status()
        return response


class ModelsClient(ApiClient):
    """
    Client to interact with `models` endpoint.
    """

    MODELS_ENDPOINT = "models"

    @auth
    def get(self, model_id: int) -> Model:
        """
        Make a call to the API to retrieve model information.

        Args:
            model_id: Model identfier to retrieve information

        Returns:
            Model: model entity with the retrieved information
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())

        response = self.session.get(
            f"{self.url}/{self.MODELS_ENDPOINT}/{model_id}",
            headers=headers,
        )
        self._echo_debug(str(response))

        response.raise_for_status()

        return Model(**response.json())

    @auth
    def create(self, model_create: ModelCreate) -> Tuple[Model, str]:
        """
        Create a new model.

        Args:
            model_create: Model information to create

        Raises:
            Exception: if there is no upload Url

        Returns:
            Tuple[Model, str]: the recently created model and a url, used to upload the model.
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())

        response = self.session.post(
            f"{self.url}/{self.MODELS_ENDPOINT}",
            headers=headers,
            json=model_create.dict(),
        )
        self._echo_debug(str(response))

        response.raise_for_status()

        upload_url = response.headers.get(MODEL_URL_HEADER.lower())

        if upload_url is None:
            raise Exception("Missing upload URL")

        return Model(**response.json()), upload_url

    def _upload(self, upload_url: str, f: BufferedReader) -> None:
        """
        Upload the file to the specified url.

        Args:
            upload_url: Url to perform a PUT operation to load file `f`
            f: Model to upload, opened as a file
        """

        response = self.session.put(
            upload_url, headers={"Content-Type": "application/octet-stream"}, data=f
        )
        self._echo_debug(str(response))

        response.raise_for_status()

        if response.status_code != 200:
            raise Exception()

    @auth
    def update(self, model_id: int, model_update: ModelUpdate) -> Model:
        """
        Update a model.

        Args:
            model_id: Model identfier to retrieve information
            model_update: body to partially update the model

        Returns:
            Model: the updated model
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())

        response = self.session.put(
            f"{self.url}/{self.MODELS_ENDPOINT}/{model_id}",
            headers=headers,
            json=model_update.dict(),
        )
        self._echo_debug(str(response))

        response.raise_for_status()

        return Model(**response.json())

    @auth
    def download(self, model_id: int) -> bytes:
        """
        Download a Transpiled model from the API.

        Args:
            model_id: Model identfier to download

        Returns:
            The model content of the request
        """

        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())

        response = self.session.get(
            f"{self.url}/{self.MODELS_ENDPOINT}/{model_id}:download",
            headers=headers,
        )
        self._echo_debug(str(response))
        url = response.json()["download_url"]
        response.raise_for_status()

        download_response = self.session.get(
            url, headers={"Content-Type": "application/octet-stream"}
        )

        self._echo_debug(str(download_response))
        download_response.raise_for_status()

        return download_response.content


class JobsClient(ApiClient):
    """
    Client to interact with `jobs` endpoint.
    """

    JOBS_ENDPOINT = "jobs"

    @auth
    def get(self, job_id: int) -> Job:
        """
        Make a call to the API to retrieve job information.

        Args:
            job_id: Job identfier to retrieve information

        Returns:
            Job: job entity with the retrieved information
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())

        response = self.session.get(
            f"{self.url}/{self.JOBS_ENDPOINT}/{job_id}",
            headers=headers,
        )
        self._echo_debug(str(response))

        response.raise_for_status()

        return Job(**response.json())

    @auth
    def create(self, job_create: JobCreate, f: BufferedReader) -> Job:
        """
        Create a new job.

        Args:
            job_create: Job information to create
            f: filed to upload, a CASM json

        Raises:
            Exception: if there is no upload Url

        Returns:
            Tuple[Model, str]: the recently created model and a url, used to upload the model.
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())

        response = self.session.post(
            f"{self.url}/{self.JOBS_ENDPOINT}",
            headers=headers,
            params=job_create.dict(),
            files={"file": f},
        )
        self._echo_debug(str(response))

        response.raise_for_status()

        return Job(**response.json())

    @auth
    def list(self) -> List[Job]:
        """
        List jobs.

        Returns:
            A list of jobs created by the user
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())

        response = self.session.get(
            f"{self.url}/{self.JOBS_ENDPOINT}",
            headers=headers,
        )
        self._echo_debug(str(response))

        response.raise_for_status()

        return [Job(**job) for job in response.json()]


class ProofsClient(ApiClient):
    """
    Client to interact with `proofs` endpoint.
    """

    PROOFS_ENDPOINT = "proofs"

    @auth
    def get(self, proof_id: int) -> Proof:
        """
        Make a call to the API to retrieve proof information.

        Args:
            proof_id: Proof identfier to retrieve information

        Returns:
            Proof: proof entity with the desired information
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())

        response = self.session.get(
            f"{self.url}/{self.PROOFS_ENDPOINT}/{proof_id}",
            headers=headers,
        )
        self._echo_debug(str(response))

        response.raise_for_status()

        return Proof(**response.json())

    @auth
    def get_by_job_id(self, job_id: int) -> Proof:
        """
        Make a call to the API to retrieve proof information based on the job id.

        Args:
            job_id: Job identifier to query by.

        Returns:
            Proof: proof entity with the desired information
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())

        response = self.session.get(
            f"{self.url}/{self.PROOFS_ENDPOINT}",
            params={"job_id": job_id},
            headers=headers,
        )
        self._echo_debug(str(response))

        response.raise_for_status()

        return Proof(**response.json()[0])

    @auth
    def download(self, proof_id: int) -> bytes:
        """
        Download a proof.

        Args:
            proof_id: Proof identifier

        Returns:
            The proof binary file
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())

        response = self.session.get(
            f"{self.url}/{self.PROOFS_ENDPOINT}/{proof_id}:download",
            headers=headers,
        )

        self._echo_debug(str(response))
        response.raise_for_status()

        url = response.json()["download_url"]

        download_response = self.session.get(url)

        self._echo_debug(str(download_response))
        download_response.raise_for_status()

        return download_response.content

    @auth
    def list(self) -> List[Proof]:
        """
        List all the proofs related to the user.

        Returns:
            A list of proofs created by the user
        """
        headers = copy.deepcopy(self.default_headers)
        headers.update(self._get_auth_header())

        response = self.session.get(
            f"{self.url}/{self.PROOFS_ENDPOINT}",
            headers=headers,
        )
        self._echo_debug(str(response))

        response.raise_for_status()

        return [Proof(**proof) for proof in response.json()]
