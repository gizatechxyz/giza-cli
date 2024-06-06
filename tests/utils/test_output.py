from giza.cli.schemas.models import Model, ModelList
from giza.cli.utils.output import extract_row, print_model

model_one = Model(
    id=1,
    name="Model One",
    description="This is model one",
)

model_two = Model(
    id=2,
    name="Model Two",
)

models = ModelList(root=[model_one, model_two])


def test_print_single_model(capsys):
    print_model(model_one)
    captured = capsys.readouterr()
    assert "Model One" in captured.out
    assert "This is model one" in captured.out


def test_print_list_model(capsys):
    print_model(models)
    captured = capsys.readouterr()
    assert "Model One" in captured.out
    assert "Model Two" in captured.out
    assert "This is model one" in captured.out
    assert "" in captured.out


def test_extract_row():
    row = extract_row(model_one)
    assert row == ["1", "Model One", "This is model one"]
    row = extract_row(model_two)
    assert row == ["2", "Model Two", ""]
