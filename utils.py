def is_power_of_two(n: int) -> bool:
    """Check if a number is a power of two."""
    return n > 0 and not (n & (n - 1))

def next_power_of_two(n: int) -> int:
    """Find the next power of two greater than or equal to n."""
    if n < 1:
        raise ValueError("Input must be a positive integer.")
    return 1 if n == 1 else 2 ** (n - 1).bit_length()
