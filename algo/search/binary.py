from typing import List, NewType

IndexNum = NewType("IndexNum", int)


def linear_search(numbers: list[int], data: int) -> IndexNum:
    """
    線形で探すのでループによって処理効率が悪い。
    """
    for i in range(0, len(numbers)):
        if numbers[i] == data:
            return f"linear_search/ インデックス{IndexNum(i)}にありました。"

    return -1


def binary_search(numbers: list[int], data: int) -> IndexNum:
    """
    リストのインデックスで先頭と最後から徐々に幅を小さくしながら探すイメージ。
    平均値を取り、その要素が条件に合っているかサーチしている。
    """
    left, right = 0, len(numbers) - 1

    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == data:
            return f"binary_search/ インデックス{IndexNum(mid)}にありました。"

        elif numbers[mid] < data:
            left = mid + 1
        elif numbers[mid] > data:
            right = mid - 1

    return -2


# 再帰関数でのbinary_searchの実装
def recursive_binary_search(numbers: list[int], data: int) -> IndexNum:
    def _binary_search(
        numbers: list[int], data: int, left: IndexNum, right: IndexNum
    ) -> IndexNum:
        if left > right:
            return -1

        mid = (left + right) // 2
        if numbers[mid] == data:
            return f"binary_search/ インデックス{IndexNum(mid)}にありました。"

        elif numbers[mid] < data:
            return _binary_search(numbers, data, mid + 1, right)
        elif numbers[mid] > data:
            return _binary_search(numbers, data, left, mid - 1)

    return _binary_search(numbers, data, 0, len(numbers) - 1)


if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    data = 3
    print(linear_search(numbers, data))
    print(binary_search(numbers, data))
    print(recursive_binary_search(numbers, data))
