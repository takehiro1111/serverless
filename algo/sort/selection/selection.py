"""
先頭から1つ要素を選択する。
その要素をtempに保持する。
比較する数値の方が小さければtempに小さい要素を入れる。
それを最初に選択した要素と入れ替える。

徐々に後の要素にずらしていく。
"""


def selection_sort(numbers):
    print("初期配列", numbers)
    for i in range(len(numbers)):
        min_idx = i
        print("min_idx", min_idx)
        for j in range(i + 1, len(numbers)):
            if numbers[min_idx] > numbers[j]:
                min_idx = j

        numbers[i], numbers[min_idx] = numbers[min_idx], numbers[i]

    return numbers


if __name__ == "__main__":
    import random

    nums = [random.randint(0, 1000) for _ in range(10)]

    print(selection_sort(nums))
