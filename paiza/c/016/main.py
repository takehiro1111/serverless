"""C016:Leet文字列
Leet と呼ばれるインターネットスラングがあります。
Leet ではいくつかのアルファベットをよく似た形の他の文字に置き換えて表記します。
Leet の置き換え規則はたくさんありますが、ここでは次の置き換え規則のみを考えましょう。

置き換え前	置き換え後
A	4
E	3
G	6
I	1
O	0
S	5
Z	2

入力例1
PAIZA

出力例1
P4124

"""

# stdin
TEXT = str(input())

# 文字列の変換
# translateメソッドのmaketrans関数で変換元、変換先の文字列を指定して処理を行う。
t = TEXT.translate(str.maketrans("AEGIOSZ", "4361052"))

# stdout
print(t)
