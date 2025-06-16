"""
PAIZA 村には、カレーを作るカレー工場と、ライスを作るライス工場があります。村長であるあなたは、カレー工場でできたカレーとライス工場でできたライスを合わせてカレーライスを作る、カレーライス工場を作ることにしました。

カレー工場とライス工場で生産されるカレーとライスは、合計で 1 日あたり N 個で、時系列順に並べると F_1, F_2, ..., F_N の順に生産されます（同時に生産されることはありません）

生産されたカレーとライスは即時でカレーライス工場に運ばれ、

・カレーが運ばれてきたときにライスが 1 つ以上残っている
・ライスが運ばれてきたときにカレーが 1 つ以上残っている

いずれかのとき、カレーライスが生産されます。複数残っているときは、運ばれてきた時間が早いものを優先して選択します。

完成したカレーライスの数と、完成したカレーライスがそれぞれ何番目のカレーと何番目のライスからなっているのかを出力してください。

例えば、入力例 1 の場合は以下の図のようになっています。


"""

N = int(input())
order = input().split()

# 在庫を管理するリスト (キューとして使用)
# 中には生産された順番(1-indexed)を格納する
curry_stock = []
rice_stock = []

# 完成したペアを (カレーの順番, ライスの順番) のタプルで格納する
made_pairs = []

# 生産された順番に処理する
for i in range(N):
    item_index = i + 1

    # カレーの処理
    if order[i] == "C":
        # ライスの在庫があれば、一番古いものとペアにする
        if rice_stock:
            # pop(0)でリストの先頭(一番古い)要素を取得
            rice_index = rice_stock.pop(0)
            made_pairs.append((item_index, rice_index))
        # 在庫がなければ、カレーを在庫に追加
        else:
            curry_stock.append(item_index)

    # ライスの処理
    elif order[i] == "R":
        # カレーの在庫があれば、一番古いものとペアにする
        if curry_stock:
            curry_index = curry_stock.pop(0)
            made_pairs.append((curry_index, item_index))
        # 在庫がなければ、ライスを在庫に追加
        else:
            rice_stock.append(item_index)

# ----- 結果の出力 -----

# 完成したペアの総数
print(len(made_pairs))

# カレーの製造順にソートして出力する
made_pairs.sort()

for curry_idx, rice_idx in made_pairs:
    print(curry_idx, rice_idx)
