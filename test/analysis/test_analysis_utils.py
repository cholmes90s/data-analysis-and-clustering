import datetime as dt
import pandas.arrays as pdarray
import pandas as pd
import src.analysis.utils as to_test


def test_calculate_days_between():
    input_days = pdarray.DatetimeArray(pd.Series([dt.datetime(2021, 5, 1), dt.datetime(2021, 5, 2), dt.datetime(2021, 5, 2), dt.datetime(2021, 5, 3), dt.datetime(2021, 5, 6), dt.datetime(2021, 5, 8)]))
    
    expected_result = [1, 0, 1, 3, 2]
    result = to_test.calculate_days_between(input_days)
    
    assert result == expected_result


def test_calculate_result_of_waiting__some_1s__wait_1():
    input_days_between = [1, 1, 1, 2, 1, 1]
    expected_result = 3

    result = to_test.calculate_result_of_waiting(input_days_between, 1)

    assert result == expected_result


def test_calculate_result_of_waiting__all_1s__wait_1():
    input_days_between = [1, 1, 1, 1, 1, 1]
    expected_result = 3

    result = to_test.calculate_result_of_waiting(input_days_between, 1)

    assert result == expected_result


def test_calculate_result_of_waiting__no_1s__wait_1():
    input_days_between = [2, 3, 3, 4, 2, 2]
    expected_result = 0

    result = to_test.calculate_result_of_waiting(input_days_between, 1)

    assert result == expected_result


def test_calculate_result_of_waiting__single_1_and_greater__wait_1():
    input_days_between = [2, 3, 3, 4, 1, 3]
    expected_result = 1

    result = to_test.calculate_result_of_waiting(input_days_between, 1)

    assert result == expected_result


def test_calculate_result_of_waiting__some2s__wait_2():
    input_days_between = [2, 2, 3, 4, 1, 3]
    expected_result = 2

    result = to_test.calculate_result_of_waiting(input_days_between, 2)

    assert result == expected_result


def test_calculate_result_of_waiting__some2s__wait_4():
    input_days_between = [2, 2, 4, 4, 1, 3]
    expected_result = 4

    result = to_test.calculate_result_of_waiting(input_days_between, 4)

    assert result == expected_result