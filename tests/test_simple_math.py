import pytest
from src.test import add, is_even, factorial


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_is_even():
    assert is_even(2)
    assert not is_even(3)


def test_factorial():
    assert factorial(0) == 1
    assert factorial(5) == 120


def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-1)
