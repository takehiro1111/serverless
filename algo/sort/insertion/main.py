"""
入れ替える際に値を適切な位置まで持っていく。
"""

from typing import List


def insertion_sort(numbers: list[int]) -> list[int]:
    len_numbers = len(numbers)
    for i in range(1, len_numbers):
        print(f"###########for文の開始############")
        # 一つ先のインデックスの要素をtempに置く
        temp = numbers[i]
        print("1つ目のtemp", temp, i)
        # 比較元になるインデックス
        j = i - 1
        print("whileの前のj", j)
        print(f"(temp)numbers[i]:{temp}")
        print(numbers[j])
        while j >= 0 and numbers[j] > temp:
            print(f"-----while文の開始/ J:{j}-------")
            print(f"  比較: numbers[{j}] ({numbers[j]}) > temp ({temp})")
            numbers[j + 1] = numbers[j]
            print(
                f"  移動: numbers[{j}] の値を numbers[{j+1}] へ。配列: {numbers}"
            )  # 要素移動後の配列状態
            j -= 1
            print("  whileの中でjを-1する。", j)

        numbers[j + 1] = temp
        print(
            f"temp ({temp}) を numbers[{j+1}] に挿入。配列: {numbers}"
        )  # temp挿入後の配列状態

    return numbers


if __name__ == "__main__":
    import random

    nums = [5, 3, 2, 8, 6, 1]
    print(insertion_sort(nums))
