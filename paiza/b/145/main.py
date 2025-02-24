"""B145:ビンゴゲームの判定
N × N のビンゴカードが 1 枚あります。
どのビンゴカードにも中央のマスには 0 が書かれており、最初から開けることができます。また、他のマスには数字がランダムに書かれています。
ただし、同じ数字が書かれたマスはありません。

これから K 回の抽選が行われます。
抽選では数字がランダムに排出されます。同じ数字が2回以上排出されることはありません。
ビンゴカードに抽選された数字と同じ数字が書かれたマスがあれば、そのマスを開けることができます。

ビンゴカードの縦横もしくは対角の斜め N 個のマスがすべて開けられたとき、ビンゴとします。
K 回の抽選の後、ビンゴの数を出力してください。

図1

たとえば、入力例 1 では 0, 9, 3, 13, 16, 8 が書かれた 6 つのマスを開けることができます。
縦、横、斜め、それぞれひとつずつビンゴになっており、ビンゴの数は合計で 3 となります。

入力例1
3 8
13 3 9
8 0 2
16 17 15
7 14 9 10 3 13 16 8

出力例1
3
"""

# 入力
## N = ビンゴカードのマス
## K = 抽選回数
N, K = map(int, input().split())

## ビンゴカードの並び順
### 多分、多次元配列でスタックしておくのが良さそう。
card_num = []
for i in range(N):
    nums = list(map(int, input().split()))
    card_num.append(nums)


# 抽選番号は1行で入力される
bingo_nums = list(map(int, input().split()))


# 開いているマスを管理する2次元配列
opened_card = [[False] * N for _ in range(N)]
# [[False, False, False], [False, False, False], [False, False, False]]

# 中央のマスを開ける
center = N // 2
opened_card[center][center] = True
# [[False, False, False], [False, True, False], [False, False, False]]


# ビンゴの数(Trueになっているマス)を集計している。
def check_bingo(opened_card, N):
    bingo_count = 0

    # 横の判定
    for row in opened_card:
        if any(row):
            bingo_count += 1

    # 縦の判定
    for col in range(N):
        if all(opened_card[row][col] for row in range(N)):
            bingo_count += 1

    # 左上から右下への対角線
    if all(opened_card[i][i] for i in range(N)):
        bingo_count += 1
        print(f"左上から右下への対角線{opened_card[i][i]}")

    # 右上から左下への対角線
    # N = 3は定数
    if all(opened_card[i][N - 1 - i] for i in range(N)):
        bingo_count += 1
        print(f"右上から左下への対角線:{opened_card[i][N-1-i]}")

    return bingo_count


# 当選番号との照合
for num in bingo_nums:
    for i in range(N):
        for j in range(N):
            if card_num[i][j] == num:
                opened_card[i][j] = True

# 結果出力
print(check_bingo(opened_card, N))
