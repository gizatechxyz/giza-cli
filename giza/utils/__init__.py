import json

from requests import Response

from giza.utils.echo import Echo

echo = Echo()


def get_response_info(response: Response):
    try:
        content = response.json()
        detail = content.get("detail")
    except json.JSONDecodeError:
        content = response.text if len(response.text) < 255 else response.text[:255]

    return {"content": content, "detail": detail, "status_code": response.status_code}
