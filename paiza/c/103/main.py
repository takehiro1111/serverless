"""
あなたは、ロボットのプログラミングをしています。
ロボットは N 秒間動き、ロボットを起動してから a_j (j = 1, 2, ... M) の倍数秒経過する度に、
それぞれに設定された動作 b_j を行います。

ある時間に複数の動作が起こるとき、ロボットは動作が登録された順に、登録された動作を全て行います。

ロボットを動作させたときのシミュレーションを行ってください。

シミュレーション結果は、以下の書式に従って出力してください。

・シミュレーション結果は N 行からなる。
・各 i (i = 1, 2, ..., N) 行目は、以下の通り。
　・ i 行目には、i 秒経過時のロボットの動作を出力する。
　・ i 秒目にロボットが動作するとき、i 行目には、登録された動作名を動作する順に半角スペース区切りで出力する。
　・ i 秒目にロボットが動作しないとき、i 行目には、i を出力する。

たとえば、入力例 1 に対する出力は以下のようになります。

・1 行目には、1 は 2 の倍数でも 3 の倍数でもないので、"1" と出力する。
・2 行目には、2 は 2 の倍数であるが 3 の倍数ではないので、"foo" と出力する。
・3 行目には、3 は 2 の倍数ではないが 3 の倍数であるので、"bar" と出力する。
・4 行目には、4 は 2 の倍数であるが 3 の倍数ではないので、"foo" と出力する。
・5 行目には、5 は 2 の倍数でも 3 の倍数でもないので、"5" を出力する。
・6 行目には、6 は 2 の倍数であり 3 の倍数でもあるので、"foo bar" と出力する。

入力例1
6 2
2 foo
3 bar

出力例1
1
foo
bar
foo
5
foo bar

ロボットの動きのシミュレーション結果を以下の形式で出力してください。
c_1
c_2
...
c_N

"""

# 、ロボットが作動する時間を表す整数 N、ロボットの動作の規則の数を表す整数 M
N, M = map(int, input().split())
# 12 5

num_list = []
word_list = []

for _ in range(M):
    num, word = map(str, input().split())
    num_list.append(int(num))
    word_list.append(word)

# print(num_list)
# print(word_list)
# ['2', '3']
# ['foo', 'bar']

# ['4', '2', '3', '4', '6']
# ['p', 'a', 'i', 'z', 'a']

for i in range(1, N + 1):
    actions = []  # その秒の動作を格納
    for n, w in zip(num_list, word_list):
        if i % n == 0:  # 倍数判定
            actions.append(w)

    print(" ".join(actions) if actions else i)
    # if actions:  # 動作がある場合
    #   print(' '.join(actions))
    # else:        # 動作がない場合
    #   print(i)


# for i in range(1,N+1):
#   for n, w in zip(num_list, word_list):
#     if i % n == 0:
#       print(w)
#     elif i % n != 0 :
#       print(i)


# for i, n, w in enumerate(zip(num_list, word_list),1) :
#   if i % int(num1) == 0 and i % int(num2) != 0:
#     print(word1)
#   elif i % int(num1) != 0 and i % int(num2) == 0:
#     print(word2)
#   elif i % int(num1) == 0 and i % int(num2) == 0:
#     print(f"{word1} {word2}")
#   else:
#     print(str(i))


# for i in range(1,N+1):
#   if i % int(num1) == 0 and i % int(num2) != 0:
#     print(word1)
#   elif i % int(num1) != 0 and i % int(num2) == 0:
#     print(word2)
#   elif i % int(num1) == 0 and i % int(num2) == 0:
#     print(f"{word1} {word2}")
#   else:
#     print(str(i))
