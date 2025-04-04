"""D164:区切りの良い日

1 月 1 日から 2 の 8 乗の 256 日目にあたる 9 月 13 日(うるう年では 9 月 12 日)はロシアではプログラマーの日とされています。
あなたはプログラマーの日まで 2 の n 乗日目の区切りを調べたくなりました。

1 月 1 日から何日目か x が与えられるので 2 の n 乗日目であれば「OK」そうでない場合は「NG」と出力してください。

例えば

64
と入力されたとき 64 は 2 の 6 乗なので
OK
と出力してください。

入力例1
256
出力例1
OK
"""

x = int(input())

while x % 2 ==0:
  x //= 2
  
# 最後に1になれば2のn乗と判定。
is_power_of_two = x == 1
  
print("OK" if is_power_of_two else "NG")


# 2のn乗の数を2で割り続けると：

# 例1: 8（2の3乗）の場合
# 8 ÷ 2 = 4
# 4 ÷ 2 = 2
# 2 ÷ 2 = 1
# → 1になった（2のn乗）

# 例2: 12（2のn乗ではない）の場合
# 12 ÷ 2 = 6
# 6 ÷ 2 = 3
# → 3で止まった（2のn乗ではない）
