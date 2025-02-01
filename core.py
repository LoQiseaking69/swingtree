from typing import List, Callable, Union
from .exceptions import InvalidOperationError, IndexOutOfBoundsError


class SwingTree:
    """
    An optimized segment tree for efficient tracking of aggregate functions like min, max, or sum
    over a data range with dynamic updates.
    """

    def __init__(self, data: List[Union[int, float]], func: Callable = min):
        if not isinstance(data, list) or not data:
            raise ValueError("Data must be a non-empty list of numerical values.")
        if not callable(func):
            raise TypeError("Aggregation function must be callable.")

        self.n = len(data)
        self.func = func
        self.tree = [0] * (2 * self.n)
        self._build(data)

    def _build(self, data: List[Union[int, float]]):
        """Build the segment tree from the initial data."""
        for i in range(self.n):
            self.tree[i + self.n] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.func(self.tree[i * 2], self.tree[i * 2 + 1])

    def update(self, index: int, value: Union[int, float]):
        """Update a specific index and propagate changes."""
        if not (0 <= index < self.n):
            raise IndexOutOfBoundsError(index, self.n)

        index += self.n
        self.tree[index] = value
        while index > 1:
            index //= 2
            self.tree[index] = self.func(self.tree[index * 2], self.tree[index * 2 + 1])

    def query(self, left: int, right: int) -> Union[int, float]:
        """
        Perform a range query for [left, right] using the aggregation function.

        :param left: Start index of the range (inclusive)
        :param right: End index of the range (inclusive)
        :return: Aggregated result for the specified range
        """
        if not (0 <= left <= right < self.n):
            raise IndexOutOfBoundsError(left, self.n)

        left += self.n
        right += self.n + 1
        res = float('inf') if self.func == min else float('-inf') if self.func == max else 0

        while left < right:
            if left % 2 == 1:
                res = self.func(res, self.tree[left])
                left += 1
            if right % 2 == 1:
                right -= 1
                res = self.func(res, self.tree[right])
            left //= 2
            right //= 2

        return res

    def __repr__(self):
        return f"SwingTree(size={self.n}, func={self.func.__name__})"


class SwingTreeAPI:
    """
    User-friendly API for interacting with SwingTree to track high-low value swings or aggregates.
    """

    def __init__(self, data: List[Union[int, float]], mode: str = "min"):
        func_map = {
            "min": min,
            "max": max,
            "sum": sum
        }

        if mode not in func_map:
            raise InvalidOperationError(mode)

        self.mode = mode
        self.tree = SwingTree(data, func_map[mode])

    def update_value(self, index: int, value: Union[int, float]):
        """Update a value at a specific index."""
        self.tree.update(index, value)

    def range_query(self, left: int, right: int) -> Union[int, float]:
        """Perform a range query over the given indices."""
        return self.tree.query(left, right)

    def get_tree_snapshot(self) -> List[Union[int, float]]:
        """Return the current state of the segment tree."""
        return self.tree.tree[self.tree.n:]  # Only return the original data layer

    def __repr__(self):
        return f"SwingTreeAPI(mode={self.mode}, size={self.tree.n})"