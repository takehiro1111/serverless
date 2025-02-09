"""
ボブとアリスは期末テストの点数で勝負をすることにしました。
しかし、ボブとアリスでは普段の成績に差があり、まともな勝負になりません。

そこで、期末テストの点数の各位の数を足した数の一の位で勝負することにし、大きい方が勝ちとしました。

つまり、85 点であれば 8 + 5 = 13 で、13 の一の位の 3 となります。

二人の期末テストの点数が入力されるので、どちらが勝ったか、あるいは引き分けたかを出力してください。

入力例1
75 81

出力例1
Alice
"""

# 入力
# ボブの点数 X アリスの点数 Y
X, Y = map(int, input().split())

x_list = [int(x) for x in str(X)]
y_list = [int(y) for y in str(Y)]

# 処理
# 十の位と一の位を足して一の位の大きさで判断する。
##十の位と一の位を分割
bob_score = x_list[0] + x_list[1]
alice_score = y_list[0] + y_list[1]
# print(bob_score)
# print(alice_score)

# 足し合わせた後に一の位を抽出するための処理
x_list_2 = [int(x) for x in str(bob_score)]
y_list_2 = [int(y) for y in str(alice_score)]
# print(x_list_2)
# print(y_list_2)

# 判定
if x_list_2[-1] > y_list_2[-1]:
    print("Bob")
elif x_list_2[-1] < y_list_2[-1]:
    print("Alice")
elif x_list_2[-1] == y_list_2[-1]:
    print("Draw")
