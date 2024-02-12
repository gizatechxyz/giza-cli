import os
import re
import zipfile
from io import BytesIO
from typing import Optional

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


def download_model_or_sierra(
    content: bytes, output_path: str, name: Optional[str] = None
):
    """
    Download the model or sierra file.

    Args:
        content (bytes): file content
        output_path (str): path to save the file
        name (str): file name. Defaults to None.
    """
    f = BytesIO(content)
    is_zip = zipfile.is_zipfile(f)
    if not is_zip and name is not None:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        with open(os.path.join(output_path, name), "wb") as file_:
            file_.write(content)
    else:
        zip_file = zipfile.ZipFile(f)
        zip_file.extractall(output_path)
