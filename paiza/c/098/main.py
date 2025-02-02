"""C098:多重パス回し

あなたは友達とボールのパス回しをしています。
どうやら、このパス回しはルールが特徴的なようです。

最初に各人はそれぞれボールをいくつか所持しています。
その後、適当な順番でボールをパスしていくのですが、この際にパスする相手とボールの個数を宣言します。
宣言した個数以上のボールを持っている場合は宣言した個数のボールを、そうでない場合は持っているボールすべてを、選んだ相手にパスします。
なお、ボールを所持できる数に上限はありません。

このパス回しの情報が順番に与えられるので、最終的に各人が持っているボールの個数を求めてください。
下図は入力例 1 の様子を表しています。

入力例1
3 人数
10 人iが最初に持っているボールの数
5 人iが最初に持っているボールの数
8 人iが最初に持っているボールの数
3 パス回しの情報の数
1 3 5 パス回しの情報
3 2 3 パス回しの情報
2 1 10 パス回しの情報
(誰が 誰に ボールを何個宣言するか)

入力は以下のフォーマットで与えられます。

N
s_1
...
s_N
M
a_1 b_1 x_1
...
a_M b_M x_M
・1 行目には、人数を表す整数 N が与えられます。
・続く N 行のうちの i 行目 (1 ≦ i ≦ N) には、 人 i が最初に持っているボールの個数を表す整数 s_i が与えられます。
・N+2 行目には、パス回しの情報の数を表す整数 M が与えられます。
・続く M 行のうちの i 行目 (1 ≦ i ≦ M) には、 i 番目のパス回しの情報を表す
3 つの整数 a_i, b_i, x_i がこの順に半角スペース区切りで与えられます。
これは、人 a_i が相手として人 b_i を、そしてボールの個数 x_i を宣言したことを表します。


出力例1
13
0
10
"""

# パス回しに参加している人数を受け取る。
PLAYERS = int(input())


# ボールの数を受け取って保持する。
# [10,5,8]
has_balls = [int(input()) for _ in range(PLAYERS)]

# パス回しの情報の数の受け取り
INFO_NUMBER = int(input())

for i in range(INFO_NUMBER):
    # 誰が 誰に ボールを何個宣言するかの情報を受け取る。
    # 1 3 5
    # 3 2 3
    # 2 1 10
    my_name, your_name, defined_balls = list(map(int, input().split()))

    if defined_balls <= has_balls[my_name - 1]:

        # 宣言した個数のボールを相手に渡す。
        # 3のボールが増える。
        has_balls[your_name - 1] += defined_balls

        # ボールをパスするのでこのループの要素(ボールの数)を渡す分減らす。
        has_balls[my_name - 1] -= defined_balls

        # デバッグ用
        print(has_balls)

    else:
        # そうでない場合は持っているボールすべてを、選んだ相手にパスします。
        has_balls[your_name - 1] += has_balls[my_name - 1]

        # ボールの数を持っている分減らすので0を入れる。
        has_balls[my_name - 1] = 0

        # デバッグ用
        print(has_balls)


for i in range(PLAYERS):
    print(has_balls[i])
