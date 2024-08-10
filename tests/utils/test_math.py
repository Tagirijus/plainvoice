from plainvoice.utils import math_utils


def test_int_convertible_check():
    # check if utils helper method gives correct output
    assert math_utils.is_convertible_to_int('1') is True
    assert math_utils.is_convertible_to_int('2.5') is False
    assert math_utils.is_convertible_to_int('1,5') is False
    assert math_utils.is_convertible_to_int('string') is False
    assert math_utils.is_convertible_to_int('1 h') is False
