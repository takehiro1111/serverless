"""
swapが一度もTrueにならない（入れ替わりがない）場合は、途中で見切って処理を終了する。
冒頭と最後にlimitを設けて徐々に挟み込んで絞るイメージ。
そのため、バブルソートよりいくらか処理速度が良い。
"""

from typing import List


def cocktail_sort(numbers: list[int]) -> list[int]:
    swapped = True
    start = 0
    end = len(numbers) - 1

    while swapped:
        swapped = False

        for i in range(start, end):
            if numbers[i] > numbers[i + 1]:
                numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
                swapped = True

        if swapped is False:
            break

        # 降順スキャンのための初期化
        swapped = False
        end = end - 1

        for i in range(end - 1, start - 1, -1):
            if numbers[i] > numbers[i + 1]:
                numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
                swapped = True

        start += 1

    return numbers


if __name__ == "__main__":
    import random

    nums = [random.randint(0, 20) for _ in range(10)]
    print(f"処理前:{nums}")
    print(cocktail_sort(nums))
