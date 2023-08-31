import json
from unittest.mock import Mock

from requests import Response

from giza.utils import get_response_info


def test_get_response_info_json():
    # Test the get_response_info function with a json response

    # Mock a response with json content
    response_json = Mock(spec=Response)
    response_json.headers = {"x-request-id": "1234"}
    response_json.status_code = 400
    response_json.json.return_value = {"detail": "value"}

    # Test with json response
    result = get_response_info(response_json)
    assert result == {
        "content": {"detail": "value"},
        "request_id": "1234",
        "detail": "value",
        "status_code": 400,
    }


def test_get_response_info_text():
    # Test the get_response_info function with a text response

    # Mock a response with text content
    response_text = Mock(spec=Response)
    response_text.headers = {"x-request-id": "1234"}
    response_text.text = "response text"
    response_text.status_code = 400
    response_text.json.side_effect = json.JSONDecodeError("msg", doc="", pos=0)

    # Test with text response
    result = get_response_info(response_text)
    assert result == {
        "content": "response text",
        "detail": "",
        "request_id": "1234",
        "status_code": 400,
    }
