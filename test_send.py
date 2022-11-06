from unittest.mock import patch, call
from send import mass_sending


@patch("send.send")
def test_mass_sending(mock_function):
    mass_sending("test_output.csv")
    mock_function.assert_has_calls([call("+447777777777", "Gifter", "Mrs Claus")])
