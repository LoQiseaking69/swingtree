#  SwingTree - High-Low Value Tracking

## Overview
SwingTree is a fast and efficient segment tree implementation designed to track high-low value swings in numerical data. It supports real-time updates and queries with logarithmic time complexity.

## Features
- Supports operations for `min`, `max`, and `sum`.
- Efficient range queries and updates.
- User-friendly API wrapper.
- Built-in utility functions for power-of-two calculations.

## Installation

pip install swingtree

## Usage

### Basic Example

```python
from swingtree import SwingTreeAPI

data = [3.5, 2.1, 8.7, 6.0, 1.2]
api = SwingTreeAPI(data, mode="min")

# Query the minimum value in range 1 to 3
print(api.range_query(1, 3))

# Update value at index 2
api.update_value(2, 0.9)

# Get updated range query
print(api.range_query(0, 4))
```
Utility Functions

SwingTree provides two useful utility functions for power-of-two calculations.

Check if a Number is a Power of Two

from swingtree.utils import is_power_of_two
```
print(is_power_of_two(8))  # True
print(is_power_of_two(10)) # False
print(is_power_of_two(0))  # False
```
Find the Next Power of Two

from swingtree.utils import next_power_of_two
```
print(next_power_of_two(7))  # 8
print(next_power_of_two(16)) # 16
print(next_power_of_two(0))  # Raises ValueError
```
Performance

SwingTree leverages efficient segment tree operations, achieving:
	•	Range Queries: O(log n)
	•	Updates: O(log n)
	•	Build Time: O(n)

License

MIT License.

---

