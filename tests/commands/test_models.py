from unittest.mock import patch

from pydantic import ValidationError
from pydantic_core import InitErrorDetails
from requests import HTTPError

from giza.commands.models import ModelsClient
from giza.schemas.models import Model, ModelList
from tests.conftest import invoke_cli_runner


# Test successful model retrieval
def test_models_get():
    model = Model(
        id=1,
        name="test_model",
        description="test_description",
        created_at="2021-08-31T15:00:00.000000",
        updated_at="2021-08-31T15:00:00.000000",
    )
    with patch.object(ModelsClient, "get", return_value=model) as mock_get:
        result = invoke_cli_runner(["models", "get", "--model-id", "1"])

    assert result.exit_code == 0
    mock_get.assert_called_once()
    assert "Retrieving model information" in result.stdout


# Test model retrieval with invalid model id
def test_models_get_invalid_id():
    with patch.object(
        ModelsClient,
        "get",
        side_effect=ValidationError.from_exception_data(
            line_errors=[InitErrorDetails(type="missing")],
            title="Resource validation error",
        ),
    ), patch("giza.commands.models.get_response_info", return_value={}):
        result = invoke_cli_runner(
            ["models", "get", "--model-id", "1"], expected_error=True
        )

    assert result.exit_code == 1
    assert "Model validation error" in result.stdout


# Test successful model listing
def test_models_list():
    models = ModelList(
        root=[
            Model(
                id=1,
                name="test_model",
                description="test_description",
                created_at="2021-08-31T15:00:00.000000",
                updated_at="2021-08-31T15:00:00.000000",
            )
        ]
    )
    with patch.object(ModelsClient, "list", return_value=models) as mock_list:
        result = invoke_cli_runner(["models", "list"])

    assert result.exit_code == 0
    mock_list.assert_called_once()
    assert "Listing models" in result.stdout


# Test model listing with server error
def test_models_list_server_error():
    with patch.object(ModelsClient, "list", side_effect=HTTPError), patch(
        "giza.commands.models.get_response_info", return_value={}
    ):
        result = invoke_cli_runner(["models", "list"], expected_error=True)

    assert result.exit_code == 1
    assert "Could not list models" in result.stdout


# Test model retrieval with HTTPError in normal mode
def test_models_get_httperror():
    with patch.object(ModelsClient, "get", side_effect=HTTPError), patch(
        "giza.commands.models.get_response_info", return_value={"request_id": 1}
    ):
        result = invoke_cli_runner(
            ["models", "get", "--model-id", "1"], expected_error=True
        )

    assert result.exit_code == 1
    assert "Could not retrieve model information" in result.stdout
    assert "Detail" in result.stdout
    assert "Status code" in result.stdout
    assert "Error message" in result.stdout
    assert "Request ID" in result.stdout


# Test model retrieval with HTTPError in debug mode
def test_models_get_httperror_debug():
    with patch.object(ModelsClient, "get", side_effect=HTTPError), patch(
        "giza.commands.models.get_response_info", return_value={"request_id": 1}
    ):
        result = invoke_cli_runner(
            ["models", "get", "--model-id", "1", "--debug"], expected_error=True
        )

    assert result.exit_code == 1
    assert "Could not retrieve model information" in result.stdout
    assert "Detail" in result.stdout
    assert "Status code" in result.stdout
    assert "Error message" in result.stdout
    assert "Request ID" in result.stdout
    assert "Debugging mode is on" in result.stdout
