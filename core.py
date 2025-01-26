from typing import List, Callable, Union
from .exceptions import InvalidOperationError, IndexOutOfBoundsError

class SwingTree:
    """An efficient segment tree for tracking high-low value swings with fast updates and queries."""

    def __init__(self, data: List[Union[int, float]], func: Callable = min):
        if not data or not isinstance(data, list):
            raise ValueError("Data must be a non-empty list of numerical values.")
        if not callable(func):
            raise TypeError("Aggregation function must be callable.")
        
        self.n = len(data)
        self.func = func
        self.tree = [0] * (2 * self.n)
        self._build(data)

    def _build(self, data: List[Union[int, float]]):
        for i in range(self.n):
            self.tree[i + self.n] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.func(self.tree[i * 2], self.tree[i * 2 + 1])

    def update(self, index: int, value: Union[int, float]):
        if not (0 <= index < self.n):
            raise IndexOutOfBoundsError(f"Index {index} out of bounds.")
        
        index += self.n
        self.tree[index] = value
        while index > 1:
            index //= 2
            self.tree[index] = self.func(self.tree[index * 2], self.tree[index * 2 + 1])

    def query(self, left: int, right: int) -> Union[int, float]:
        if not (0 <= left <= right < self.n):
            raise IndexOutOfBoundsError("Invalid query range.")
        
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
    """User-friendly API for interacting with SwingTree for high-low value tracking."""

    def __init__(self, data: List[Union[int, float]], mode: str = "min"):
        func_map = {
            "min": min,
            "max": max,
            "sum": sum
        }
        
        if mode not in func_map:
            raise InvalidOperationError("Mode must be 'min', 'max', or 'sum'.")
        
        self.mode = mode
        self.tree = SwingTree(data, func_map[mode])

    def update_value(self, index: int, value: Union[int, float]):
        self.tree.update(index, value)

    def range_query(self, left: int, right: int) -> Union[int, float]:
        return self.tree.query(left, right)

    def get_tree_snapshot(self) -> List[Union[int, float]]:
        return self.tree.tree

    def __repr__(self):
        return f"SwingTreeAPI(mode={self.mode}, size={self.tree.n})"
