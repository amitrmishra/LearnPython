from gcd import gcd


def test_gcd_on_specific_examples():
    assert gcd(15, 6) == 3
    assert gcd(15, 5) == 5
    assert gcd(-9, 15) == 3
    # Added after discovering them from the property-based testing
    assert gcd(0, 0) == 0
    assert gcd(0, 4) == 4
    # May also check for expected exceptions in unit test for certain arguments


# Link: https://semaphoreci.com/blog/property-based-testing-python-hypothesis-pytest

# Instead of writing inputs to the function gcd, we let Hypothesis generate arbitrary inputs.
# Instead of hardcoding the expected outputs, we write assertions that ensure that the solution
#   satisfies the properties that it should satisfy.

# if d is the result of gcd(n1, n2), then:
#   d is positive;
#   d divides n1;
#   d divides n2; and
#   no other number larger than d divides both n1 and n2.

# given is what we will use to tell Hypothesis that a test function needs to be given data.
# strategies is the module that contains lots of tools that know how to generate data.

from hypothesis import given, strategies as st


# pytest looks for functions that start with test_
# the test function needs to be given one integer, and then another integer
# @given(st.integers(), st.integers())
@given(st.integers(min_value=1, max_value=100),
       st.integers(min_value=-500, max_value=500))
def test_gcd(n1, n2):
    d = gcd(n1, n2)

    assert d > 0         # 1) `d` is positive
    assert n1 % d == 0   # 2) `d` divides `n`
    assert n2 % d == 0   # 3) `d` divides `m`

    # assert d == 0 if n1 == n2 == 0 else d > 0  # 1) `d` is positive
    # assert n1 % d == 0 if d != 0 else True     # 2) `d` divides `n`
    # assert n2 % d == 0 if d != 0 else True     # 3) `d` divides `m`

    # 4) no other number larger than `d` divides both `n` and `m`
    for i in range(d + 1, min(n1, n2)):
        assert (n1 % i) or (n2 % i)  # `i` fails to divide at least one of the args

# Benefits of property-based testing:
# -----------------------------------
# Hypothesis can generate dozens or hundreds of tests for you,
#   while you would typically only write a couple of them;
# Tests you write by hand will typically only cover the edge cases you have already thought of,
#   whereas Hypothesis will not have that bias; and
# Thinking about your solution to figure out its properties can give you deeper insights into the
#   problem, leading to even better solutions.
