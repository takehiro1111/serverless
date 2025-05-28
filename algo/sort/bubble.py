from typing import List


# バブルソートの作成
# 並びが昇順でも最後までソート処理を継続する。
# インデックスの一番後ろから順にlimitを設ける。
def bubble_sort(numbers: list[int]) -> list[int]:
    print(numbers)
    for i in range(len(numbers)):
        print("i", i)
        for j in range(len(numbers) - 1 - i):
            print("len(numbers) -1 -i", len(numbers) - 1 - i)
            print("j", j)
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
            print(numbers)

    return numbers


if __name__ == "__main__":
    import random

    nums = [random.randint(0, 20) for _ in range(5)]
    print(bubble_sort(nums))
