import pytest

@pytest.mark.parametrize("input_data,expected", [(1, 2), (2, 4), (3, 6)])
def test_multiply_by_two(input_data, expected):
    assert input_data * 2 == expected
