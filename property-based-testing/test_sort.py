from collections import Counter
import pytest

from sort import sort
from hypothesis import given, strategies as st


def test_my_sort_specific_examples():
    # assert sort([]) == []
    assert sort(list(range(10)[::-1])) == list(range(10))
    assert sort([42, 73, 0, 16, 10]) == [0, 10, 16, 42, 73]
    with pytest.raises(Exception) as e:
        # Question: What is `e` here? What does it contain?
        sort([])


@given(st.lists(st.integers()))
def test_my_sort(int_list):
    # if we don't cover this case in the unit test, we may do it here inside if-else
    #  otherwise, we can cover them in the unit test and set min_size=1 inside strategies as:
    #  `st.lists(st.integers(), min_size=1)`
    if not int_list:
        with pytest.raises(Exception) as e:
            # Question: What is `e` here? What does it contain?
            sort(int_list)
    else:
        result = sort(int_list)
        assert len(result) == len(int_list)
        # assert set(result) == set(int_list)  # Same numbers as input.
        assert Counter(result) == Counter(int_list)  # Should use numbers from input.
        for a, b in zip(result, result[1:]):
            assert a <= b
