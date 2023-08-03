import json
from typing import Any, Dict

from requests import Response

from giza.utils.echo import Echo

# Provided an instance for ease of use
echo = Echo()


def get_response_info(response: Response) -> Dict[str, Any]:
    """
    Utility to retrieve information of the client response.

    Try to get the body, if not just get the text.

    Args:
        response (Response): a response from the API

    Returns:
        dict: information about the returned response
    """
    try:
        content = response.json()
        detail = content.get("detail")
    except json.JSONDecodeError:
        content = response.text if len(response.text) < 255 else response.text[:255]
        detail = ""

    return {"content": content, "detail": detail, "status_code": response.status_code}
