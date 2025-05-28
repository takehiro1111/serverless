"""
コムソート
串の幅を小さくするイメージ。

Gap 7 / 1.3 = 5
5個離れている数値同士を比較してsortする。
Gap 5 / 1.3 = 3
3個離れている数値同士を比較してsortする。
Gap 3 / 1.3 = 2
2個離れている数値同士を比較してsortする。
Gap 2 / 1.3 = 1
1個(隣同士)離れている数値同士を比較してsortする。

最終的にSwapがFalseの状態で確認する必要がある。
"""

from typing import List


def comb_sort(numbers: list[int]) -> list[int]:
    len_numbers = len(numbers)
    gap = len_numbers
    swapped = True

    while gap != 1 or swapped:
        gap = int(gap / 1.3)
        if gap < 1:
            gap = 1

        swapped = False

        for i in range(0, len_numbers - gap):
            # 1.3で割った数離れている要素を比較してsortする。
            if numbers[i] > numbers[i + gap]:
                numbers[i], numbers[i + gap] = numbers[i + gap], numbers[i]
                swapped = True

    return numbers


if __name__ == "__main__":
    import random

    nums = [random.randint(0, 20) for _ in range(10)]
    print(f"処理前:{nums}")
    print(comb_sort(nums))
