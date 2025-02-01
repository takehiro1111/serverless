"""C138:反復横跳び大会
今日は PAIZA 小学校の反復横跳び大会でした。
あなたは、この大会の記録委員に任命されており、記録を集計する必要があります。

生徒の記録からそれぞれの順位を求めてください。

ただし、記録が X 回の生徒の順位は、記録が X より大きい生徒の人数 + 1 となり、同じ順位の生徒が存在することもあります。

例えば、入力例 1 の場合、以下のようになります。

入力例1
4 人数
55 回数
57
55
52

出力例1 (順位)
2
1
2
4
"""

# 人数の受け取り
PLAYERS = int(input())

# 回数の受け取り
side_jump_count = [int(input()) for _ in range(PLAYERS)]
# [55,57,55,52]

# 順位づけの判定
for score in side_jump_count:
    # より良い記録の数を数えるための変数
    better_count = 0

    # リストの中の各記録と比較
    for compared_score in side_jump_count:
        # もし比較する記録が現在の記録より大きければ
        # 例1: compared_score -> [55,57,55,52]の各要素をループで処理 / score -> 55
        # 例2: compared_score -> [55,57,55,52]の各要素をループで処理 / score -> 57
        # 例3: compared_score -> [55,57,55,52]の各要素をループで処理 / score -> 52
        if compared_score > score:
            # カウントを1増やす
            better_count += 1

    # 順位は「より良い記録の数 + 1」
    ranking = better_count + 1
    print(ranking)


# 以下、理解できなかったためよりわかりやすい書き方にする。
# 順位づけの判定
# scoreにはインデックスではなく、要素自体が入る。
# for score in side_jump_count:
#     # その記録より大きい記録の数を数える
#     # print(f"score:{score}")
#     # i > scoreなら1を生成する。
#     # i > scoreを満たさない場合はFalseの0を返す。
#     # score(固有の要素(例:55))に対して、iはsum()の中のfor文だけで回しているイメージ。
#     better_scores = sum(1 for i in side_jump_count if i > score)
#     # 順位 = より大きい記録の数 + 1
#     ranking = better_scores + 1
#     print(ranking)


# 以下は自分で書こうとしたが書けなかった残骸。
# # 順位づけの判定
# for i in range(PLAYERS):
#   if side_jump_count[i] < max(side_jump_count):
#     ranking = i + 1
#     print(ranking)


# 各々の順位を出力
