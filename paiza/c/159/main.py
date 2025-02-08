"""C159:当選通知
あなたはくじの当選通知を行う担当者です。

くじはユーザーが投票期間中に 0 から 9999 までの数を 1 つだけ選んで投票する方式です。投票した数字のことを投票番号と言います。
投票には 1 から順に連番で投票 ID が与えられます。ユーザーは自分の投票 ID と投票番号を知ることができます。

投票期間終了時に運営が 0 から 9999 までの当選番号をランダムに N 個選びます。
N 個の当選番号の中に自分の投票番号と 1 つでも同じ番号があれば当選となります。

N 個の当選番号と、K 個の投票番号が 投票 ID が 1 のものから順に与えられます。
当選した投票の ID をすべて出力してください。
当選した投票がなかった場合、-1 を出力してください。

入力例1
6 8
765 876 961 346 315 283
13 39 52 346 190 49 283 28

出力例1
4
7
"""

# 当選番号の数と投票数の受け取り
WINS, POLLS = map(int, input().split())

# 当選番号
winning_nums = [int(i) for i in input().split()]
# print(winning_nums)

# 各自の投票番号
poll_nums = [int(i) for i in input().split()]
# print(poll_nums)

# counter = {}
win_ids = []

# 処理
# for i,num in enumerate(poll_nums):
#   if num in winning_nums:
#     print(int(i+1))
#   elif num not in winning_nums:
#     counter.add(-1)
#     print(counter)

for i, num in enumerate(poll_nums, 1):
    if num in winning_nums:
        win_ids.append(i)

if not win_ids:
    print(-1)
else:
    for i in win_ids:
        print(i)
