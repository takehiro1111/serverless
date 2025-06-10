# cards, shuffle_nums = map(int, input().split())

# cards, shuffle_nums = 8, 3

# temp_list = [i for i in range(1, cards+1)]
# print(temp_list)
# # [1, 2, 3, 4, 5, 6, 7, 8]


# first_half = []
# second_half = []


# for i in range(1, cards+1):
#   if i <= (cards // 2 ):
#     first_half.append(i)
#   else:
#     second_half.append(i)

# print("first_half", first_half)
# print("second_half", second_half)
# # first_half [1, 2, 3, 4]
# # second_half [5, 6, 7, 8]

# result_shuffle = []


import sys


def perfect_shuffle():
    """
    パーフェクトシャッフルをN回行った結果を出力する
    """
    try:
        M, N = map(int, sys.stdin.readline().split())
        print(M, N)
    except ValueError:
        # ローカルでのテスト用に値を設定
        M, N = 8, 3

    cards = list(range(1, M + 1))
    print("forの前のcards", cards)

    for _ in range(N):
        first_half = cards[: M // 2]
        second_half = cards[M // 2 :]
        print("first_half", first_half)
        print("second_half", second_half)

        shuffled = []
        for i in range(M // 2):
            shuffled.append(second_half[i])
            shuffled.append(first_half[i])
            print("shuffled", shuffled)
        # cardsの並び順を変えている。
        cards = shuffled
        print("forの中のcards", cards)

    print(*cards)


perfect_shuffle()

# print('s------------------------')
# s = list(range(1,10+1))
# s1 = s[:10//2]
# s2 = s[10//2:]
# print(s1)
# print(s2)


# cards, shuffle_nums = map(int, input().split())

cards, shuffle_nums = 8, 3

# 初期のカードの並び順を作る。
cards_list = list(range(1, cards + 1))

for _ in range(shuffle_nums):
    first_half = cards_list[: cards // 2]
    second_half = cards_list[cards // 2 :]

    temp_shuffled = []
    for j in range(cards // 2):
        temp_shuffled.append(second_half[j])
        temp_shuffled.append(first_half[j])

    cards_list = temp_shuffled

print(*cards_list)
