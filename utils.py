def is_power_of_two(n: int) -> bool:
    """
    Check if a given number is a power of two.

    :param n: Integer to check
    :return: True if n is a power of two, otherwise False
    """
    if n < 1:
        return False
    return (n & (n - 1)) == 0


def next_power_of_two(n: int) -> int:
    """
    Find the next power of two greater than or equal to n.

    :param n: Integer input
    :return: The next power of two
    """
    if n < 1:
        raise ValueError("Input must be a positive integer.")
    return 1 if n == 1 else 2 ** (n - 1).bit_length()


def validate_data(data):
    """
    Validate that the input data is a non-empty list of numerical values.

    :param data: List to validate
    :raises ValueError: If validation fails
    """
    if not isinstance(data, list) or not data:
        raise ValueError("Data must be a non-empty list.")
    if not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("Data must contain only numerical values.")