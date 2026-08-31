from app.ui.cli import get_float


def test_get_float(monkeypatch):

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "80000"
    )

    result = get_float(
        "Income: "
    )

    assert result == 80000.0