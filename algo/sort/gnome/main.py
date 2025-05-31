"""
ノームソート

次の要素と比較して入れ替える。
入れ替えたら左に1つズレる。（ソートできてなかったら連続して戻る。）


"""

from typing import List


def gnome_sort(numbers: list[int]) -> list[int]:
    len_numbers = len(numbers)
    index = 0

    while index < len_numbers:
        # 初回はインデックス0からで比較するための準備としてインデックスを増やす。
        if index == 0:
            index += 1

        # 現在のインデックスの要素が一つ前の要素より小さければ要素を入れ替え、スコープを前の要素からにする。
        if numbers[index] < numbers[index - 1]:
            numbers[index], numbers[index - 1] = numbers[index - 1], numbers[index]
            index -= 1
        else:
            # 問題なく照準になっていれば次のスコープを次のインデックスにスライドする。
            index += 1

    return numbers


if __name__ == "__main__":
    import random

    numbers = [random.randint(0, 100) for _ in range(10)]
    print(gnome_sort(numbers))
