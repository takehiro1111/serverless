"""C067:【ハッカー入門コラボ問題】数字の調査

あなたは 2 進数について勉強しました。
そこで、あなたは任意の数字の 2 進数表示のどの桁が 1 になるのか、もしくは 0 になるのかが気になりました。

知りたい桁が複数指定されるので、その桁が 0 なのか 1 なのか判定するプログラムを作成してください。
知りたい桁は、与えられた数字を 2 進数にしたときの桁数より小さいものとします。

入力例 1 の場合、以下の図のように、与えられた数字は 44 であるので、2 進数にした場合 101100 になります。
そして、出力する値は順番に、右から 4 番目、2 番目、6 番目の数字なので、
1, 0, 1 の各番号に改行を含んだものとなります。

入力例1
3 44 知りたい数字の数 10進数の値
4
2
6

出力例1
1
0
1
"""

N, X = map(int, input().split())  # 3 44 知りたい数字の数 10進数の値


# 44を10進数から2進数へ変換する処理
def base_num(num):  # num = 44の場合
    bit_list = []
    while True:
        bit = num % 2  # 余りは0になる。
        bit_list.append(bit)  # 44 / 2をの余りをループでリストに格納
        num //= 2  # 2で割る。

        if (
            num == 0
        ):  # 上記でnumが0まで破り尽くされればループが2進数が出来上がりループを脱出できる。
            break
    return bit_list


def extract(n, x):
    bits = base_num(x)  # [1, 0, 1, 1, 0, 0]

    for _ in range(n):
        t = int(input())  # 指定する番号を受け取る。4 2 6
        result = bits[t - 1]
        print(result)


extract(N, X)

# 入力の受け取り
# N, X = map(int,input().split()) # 3 44 知りたい数字の数 10進数の値

# # 44を10進数から2進数へ変換する処理
# def base_num(num): # num = 44の場合
#   bit_list = []
#   while True:
#     bit = num % 2 # 余りは0になる。
#     bit_list.append(bit) # 44 / 2をの余りをループでリストに格納
#     num //= 2 # 2で割る。

#     if num == 0: # 上記でnumが0まで破り尽くされればループが2進数が出来上がりループを脱出できる。
#       break

#   bit_list.reverse() # なぜソートする？
#   print(bit_list)
#   return bit_list

# def extract(n,x):
#   bits = base_num(x) # [1, 0, 1, 1, 0, 0]

#   for _ in range(n):
#     t = int(input()) # 指定する番号を受け取る。4 2 6
#     bits.reverse() # [0,0,1,1,0,1]
#     result = bits[t-1]
#     print(result)

# extract(N,X)
