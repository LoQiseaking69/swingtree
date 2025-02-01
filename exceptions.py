class InvalidOperationError(Exception):
    """
    Raised when an invalid operation is attempted within the SwingTree or its API.
    """

    def __init__(self, operation: str):
        super().__init__(f"Invalid operation: '{operation}'. Ensure the operation is valid for this context.")
        self.operation = operation


class IndexOutOfBoundsError(Exception):
    """
    Raised when an index is out of the valid range within the SwingTree.
    """

    def __init__(self, index: int, size: int):
        super().__init__(f"Index {index} is out of bounds for data size {size}.")
        self.index = index
        self.size = size


class DataIntegrityError(Exception):
    """
    Raised when there are issues with data format, consistency, or unexpected values.
    """
    def __init__(self, message: str):
        super().__init__(message)