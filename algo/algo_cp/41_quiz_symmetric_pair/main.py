"""
Symmetric
Input  [(1, 2), (3, 5), (4, 7), (5, 3), (7, 4)]
Output [(5, 3), (7, 4)]
"""

from collections.abc import Iterator
from typing import List, Tuple


def find_pair(pairs: list[tuple[int, int]]) -> Iterator[tuple[int, int]]:
    cache = {}
    for pair in pairs:
        first, second = pair[0], pair[1]
        value = cache.get(second)
        if not value:
            cache[first] = second
        elif value == first:
            yield pair


if __name__ == "__main__":
    l = [(1, 2), (3, 5), (4, 7), (5, 3), (7, 4)]
    for r in find_pair(l):
        print(r)
