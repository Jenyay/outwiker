import pytest

from outwiker.gui.theme import defaultValue


class Data:
    def __init__(self, val) -> None:
        self.val = val

    @defaultValue("ok")
    def get_val(self):
        return self.val


@pytest.mark.parametrize("input,expected", [(123, 123), (None, "ok"), ("", "ok"), ("None", "ok")])
def test_decorator(input, expected):
    data = Data(input)
    assert data.get_val() == expected
