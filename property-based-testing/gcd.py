# The greatest common divisor of n1 and n2 is the largest integer d that divides evenly into n1
#   and n2
def gcd(n1, n2):
    """Compute the GCD of two integers by Euclid's algorithm."""
    n1, n2 = abs(n1), abs(n2)
    n1, n2 = min(n1, n2), max(n1, n2)  # Sort their absolute values.

    # The right side of % operator can't be 0
    if not n1:
        return n2

    while n2 % n1:  # While `n1` doesn't divide into `n2`:
        # update the values of `n1` to be the remainder when `n2` divided
        # by `n1` and `n2` to be previous value of `n1`.
        n1, n2 = n2 % n1, n1
    return n1
