import pytest
from logic_utils import check_guess, parse_guess, INITIAL_ATTEMPTS


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

def test_winning_guess():
    assert check_guess(50, 50) == "Win"

def test_guess_too_high():
    assert check_guess(60, 50) == "Too High"

def test_guess_too_low():
    assert check_guess(40, 50) == "Too Low"

def test_check_guess_secret_is_1_guess_exact():
    assert check_guess(1, 1) == "Win"

def test_check_guess_secret_is_100_guess_exact():
    assert check_guess(100, 100) == "Win"

def test_check_guess_guess_above_max_boundary():
    # guess one above secret at the top of the range
    assert check_guess(101, 100) == "Too High"

def test_check_guess_guess_below_min_boundary():
    # guess one below secret at the bottom of the range
    assert check_guess(0, 1) == "Too Low"

def test_check_guess_by_one_above():
    assert check_guess(51, 50) == "Too High"

def test_check_guess_by_one_below():
    assert check_guess(49, 50) == "Too Low"

def test_check_guess_large_overshoot():
    assert check_guess(999, 1) == "Too High"

def test_check_guess_large_undershoot():
    assert check_guess(1, 999) == "Too Low"

def test_check_guess_negative_guess_vs_positive_secret():
    assert check_guess(-5, 10) == "Too Low"

def test_check_guess_zero_secret_guess_exact():
    assert check_guess(0, 0) == "Win"

def test_check_guess_zero_secret_guess_above():
    assert check_guess(1, 0) == "Too High"

def test_check_guess_zero_secret_guess_below():
    assert check_guess(-1, 0) == "Too Low"

@pytest.mark.parametrize("guess,secret,expected", [
    (10, 10, "Win"),
    (11, 10, "Too High"),
    (9,  10, "Too Low"),
    (1,   1, "Win"),
    (2,   1, "Too High"),
    (0,   1, "Too Low"),
])
def test_check_guess_parametrized(guess, secret, expected):
    assert check_guess(guess, secret) == expected


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_valid_float_truncates():
    ok, value, err = parse_guess("3.9")
    assert ok is True
    assert value == 3
    assert err is None

def test_parse_guess_float_rounds_down():
    ok, value, err = parse_guess("7.1")
    assert ok is True
    assert value == 7
    assert err is None

def test_parse_guess_none_input():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_whitespace_only():
    # whitespace is not a valid number
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_alphabetic():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_alphanumeric():
    ok, value, err = parse_guess("12abc")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_special_characters():
    ok, value, err = parse_guess("!@#")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_negative_number():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None

def test_parse_guess_zero():
    ok, value, err = parse_guess("0")
    assert ok is True
    assert value == 0
    assert err is None

def test_parse_guess_large_number():
    ok, value, err = parse_guess("9999")
    assert ok is True
    assert value == 9999
    assert err is None

def test_parse_guess_leading_whitespace():
    # int() strips leading/trailing whitespace, so " 5" is valid
    ok, value, err = parse_guess(" 5")
    assert ok is True
    assert value == 5
    assert err is None

def test_parse_guess_returns_three_tuple_on_success():
    result = parse_guess("10")
    assert len(result) == 3

def test_parse_guess_returns_three_tuple_on_failure():
    result = parse_guess("bad")
    assert len(result) == 3

def test_parse_guess_error_message_is_string_on_failure():
    _, _, err = parse_guess("")
    assert isinstance(err, str)

def test_parse_guess_error_is_none_on_success():
    _, _, err = parse_guess("50")
    assert err is None


# ---------------------------------------------------------------------------
# INITIAL_ATTEMPTS regression
# ---------------------------------------------------------------------------

def test_initial_attempts_is_zero():
    # Regression: attempts was initialized to 1, causing Normal mode
    # to display 7 attempts remaining instead of 8 at the start of a new game.
    assert INITIAL_ATTEMPTS == 0
