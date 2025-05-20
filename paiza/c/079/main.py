# あなたは友達に勧められて、とあるカードゲームを始めることにしました。
# そのカードゲームには、カード番号 1 から M までの M 種類のカードがあります。
# あなたは完璧主義者なので、どうしても M 種類全てのカードが欲しくなり、カードを N 枚買いました。

# さあ、買ってきた N 枚のカードを順番に開けていきましょう!

# 開けたカードのカード番号が順番に与えられるので、M 種類そろったのは何枚開けたときかを出力するプログラムを書いて下さい。

# 以下は入力例 1 を図示したものです。

# 入力例1
# 6 3
# 1
# 2
# 2
# 3
# 1
# 3

# 出力例1
# 4

# 何枚開けたときに全種類そろったかを出力してください。
# ただし、全て開けても全種類そろわないときは、"unlucky" と出力してください。


buy_cards, all_cards = map(int, input().split())


collect_cards = set()

for i in range(buy_cards):
    card = int(input())

    if card not in collect_cards:
        collect_cards.add(card)

    if len(collect_cards) == all_cards:
        print(i + 1)
        break
    elif i + 1 == buy_cards:
        print("unlucky")
