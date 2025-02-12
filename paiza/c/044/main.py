"""C044:手の組み合わせ

じゃんけんは、2 人以上の参加者により行われるゲームです。
各参加者は、3 種類の手(グー・チョキ・パー) のいずれかを出します。
この手 の組み合わせにより勝者が決まります。

勝敗の決定は以下の通りです。

・グーは、チョキに勝ち、パーに敗れる
・チョキは、パーに勝ち、グーに敗れる
・パーは、グーに勝ち、チョキに敗れる
・グー・チョキ・パーの 3 種類が出されている場合は引き分け
・グー・チョキ・パーのいずれか 1 種類のみが出されている場合も引き分け

3 人でじゃんけんした場合の例を下図に示しました。
"""

# じゃんけんする人数の受け取り
PLAYERS = int(input())

# じゃんけんの手をリストで受け取る。
hands = []
for i in range(PLAYERS):
    hand = str(input())
    hands.append(hand)

# setで勝敗がつくケースとあいこのケースを分岐
# setで重複をなくし、要素数が2ならば勝敗を分岐し、要素数が1 or 3の場合はあいことみなす。
result = set(hands)
if len(result) == 2:
    if "paper" in result and "rock" in result:
        print("paper")
    elif "paper" in result and "scissors" in result:
        print("scissors")
    elif "rock" in result and "scissors" in result:
        print("rock")
else:
    print("draw")
