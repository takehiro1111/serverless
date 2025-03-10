"""C109:IDを登録順に並べよう
とある SNS サービスでは、ユーザー ID は「ユーザーネーム + 通し番号」となります。ここで言う通し番号とは、その人がこの SNS に何番目に登録したユーザーかを表す数字です。

例えば、paiza さんが 1 番目に登録した場合、ユーザー ID は「paiza1」、kirishima さんが 813 番目に登録した場合、ユーザー ID は「kirishima813」になります。

いま、この SNS サービスに登録しているユーザーのうち N 人のユーザー ID が与えられるので、それらを登録の早い順に並べて出力してください。

入力例 1 を例に考えると、末尾の通し番号の小さい順に並べることで、

paiza1
pizza99
sushi100
kirishima813
beef1001
となるので、これを出力すれば正答となります。


入力例1
5
paiza1
kirishima813
pizza99
sushi100
beef1001

出力例1
paiza1
pizza99
sushi100
kirishima813
beef1001
"""

# 入力
## ユーザーの人数
USERS = int(input())

## ユーザーとIDを出力
user_id = [input() for _ in range(1, USERS + 1)]
# print(user_id)

#######################################################
# 正規表現を使用する場合
#######################################################
import re


def extract_num(text):
    return int(re.findall(r"\d+", text)[0])


def main(users):
    return sorted(users, key=extract_num)


sorted_users = main(user_id)

for user in sorted_users:
    print(user)

# sorted(users, key = extract_num)で分けることで
# sortedの第一引数はイテラブルとしてここの文字列の要素が入るからtypeerrorにならない
# re.findall()は文字列を期待しているため。
# そのままuser_idを渡すとリストが入るため。
# (ダメな例)
# def main(x):
#     sorted_users = sorted(int(re.findall(r"\d+", x)[0]))
#     print(sorted_users)

# sorted_users = sorted(user_id, key=lambda x: int(re.findall(r"\d+", x)[0]))


# sorted_usersの要素がxに入る。
# xの要素の中で数字にマッチする部分を抜き出してリストとして返す。
# re.findall(r"\d+", x)がリストとして出力されるため、[0]で要素を抜き出す。

# findall()の結果:
# "paiza1" → ["1"]
# "kirishima813" → ["813"]
# "pizza99" → ["99"]
# "sushi100" → ["100"]
# "beef1001" → ["1001"]

# [0]でそれぞれの最初の（この場合は唯一の）要素を取得:
# ["1"][0] → "1"
# ["813"][0] → "813"
# ["99"][0] → "99"
# ["100"][0] → "100"
# ["1001"][0] → "1001"

# lambda x: 各ユーザーID文字列を x として受け取る無名関数

# sorted() 関数は内部でリストの要素を1つずつ key 関数に渡して、その結果を基準に並び替えを行います。
# この場合、lambda 関数が key 関数として機能し、x としてリストの各要素を受け取ります。

# re.findall(r"\d+", x):
# r"" ->  "raw"（生の、加工されていない）の頭文字
# バックスラッシュ（\）がエスケープ文字として解釈されない
# 正規表現パターンを書く際によく使用される
# findall()
# 文字列の中から正規表現パターンにマッチするすべての部分を探す
# マッチした部分をリストとして返す
# \d+: 1つ以上の連続する数字にマッチ(正規表現)
# x から数字部分を抽出して配列を返す
# 例："paiza1" → ["1"]

# [0]: 配列の最初の要素を取得
# 例：["1"] → "1"


# 正規表現
# \d	半角数字
# +	  直前のパターンを1回以上繰り返し
# 最長一致なので、できるだけ長い文字列にヒットします。

#######################################################
# 正規表現を使用しない場合
#######################################################
sorted_users = sorted(user_id, key=lambda x: int("".join(filter(str.isdigit, x))))
# keyで最終的にintが返るのでそれを基準に並び替えるが、sorted_usersの出力自体は入力の文字列と一緒。順番が変わるだけ。
for user in sorted_users:
    print(user)

# filter(str.isdigit,x)
# filter()でx(イテレータ)の中で数値(True)で返るものを抽出する。
#

# # 1. filter(str.isdigit, x)
# filter(function, iterable)
# filter(): 指定した条件で要素を選別する関数
# "paiza1" → filter(数字かどうか判定) → "1"
# "kirishima813" → filter(数字かどうか判定) → "813"

# joinを使用するには文字列でないといけない。

# str.isdigit()
# 文字が数字かどうかを判定するメソッド
# print("1".isdigit())  # True
# print("a".isdigit())  # False

# # 2. "".join()
# 空文字で結合（この例では1つの数字しかないので変化なし）

# # 3. int()
# 文字列を整数に変換:
# "1" → 1
# "813" → 813

# # 4. sorted()
# これらの数値を基準に並び替え


###########################################################################
# より細かい説明
###########################################################################
# filterはPythonの組み込み関数で、処理結果をイテレータとして返すように設計されています。

# 1. filter(str.isdigit, x)

# filter(function, iterable)
# x = "paiza12"

# 1. filter(str.isdigit, x)
# - "p" → False
# - "a" → False
# - "i" → False
# - "z" → False
# - "a" → False
# - "1" → True
# - "2" → True
# 結果：イテレータ（"1", "2"）

# 2. "".join()
# ("1", "2") → "12"

# 3. int()
# "12" → 12

# 4. 整数12がsortedのキーに使用
