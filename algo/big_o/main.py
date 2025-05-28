# O(log(n))
# データ量が多くなっても処理回数の増加は緩やか。効率の良い書き方。
def log_n(n):
    if n <= 1:
        return

    else:
        print(n)
        log_n(n / 2)


log_n(10)


# order n
# データ量と時間が比例する。
def o_n(numbers):
    for num in numbers:
        print(num)


o_n([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


# O(n * log(n))
#
def o_log_n(n):
    for i in range(int(n)):
        print(i, end=" ")

    print()

    if n <= 1:
        return

    o_log_n(n / 2)


o_log_n(10)


# O(n**2)
# データが2倍になると処理時間は4倍になる。非効率な書き方。
def big_o_square(numbers):
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            print(numbers[i], numbers[j])

        print()


big_o_square([1, 2, 3, 4, 5])
