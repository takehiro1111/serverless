import random
from typing import List


def in_order(numbers: list[int]) -> bool:
    # リストの添字なので-1している。
    # print(numbers[i] <= numbers[i+1] for i in range(len(numbers)-1))
    print(all(numbers[i] <= numbers[i + 1] for i in range(len(numbers))))
    return all(numbers[i] <= numbers[i + 1] for i in range(len(numbers)))


def bogo_sort(numbers: list[int]) -> list[int]:
    random.shuffle(numbers)
    return numbers


if __name__ == "__main__":
    print(bogo_sort([1, 5, 3, 2, 6]))

    random_nums = [random.randint(0, 1000) for _ in range(10)]
    in_order(random_nums)
