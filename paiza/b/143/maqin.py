# # B143:じゃんけん列車

# あなたはぱいざ幼稚園の先生です。あなたのクラスには N 人の園児がおり、それぞれの園児には 1 から N までの出席番号が振られています。

# 今日、あなたが受け持つクラスで「じゃんけん列車」というゲームをすることになりました。
# じゃんけん列車のおける「列車」とは、園児が一列に並んだ様子を列車に見立てた表現です。
# じゃんけん列車は、次のようなルールのゲームです。

# ・初め、それぞれの園児は 1 人からなる列車である。
# ・先生が「やめ」の合図をするまで、以下が繰り返される。
# 1. 2 つの列車の先頭の園児同士がジャンケンをする(勝敗が決まるまで続ける)。
# 2. 負けた列車は、勝った列車の最後尾に連結し、一つの列車となる。
# ・「やめ」の合図があった時点で、最も長い列車の先頭の園児が優勝者となる。ただし、そのような列車が複数存在するなら、それらの先頭の園児は全員優勝者とする。

# 園児の人数と、ゲーム中のじゃんけんの勝敗記録の情報が与えられたときに、ゲームの優勝者の出席番号の一覧を表示するプログラムを作成してください。
# ただし、園児たちはルールを守ってゲームを楽しみ、ジャンケンの勝敗記録は正確に記録されました。

# たとえば、入力例 1 では、あなたのクラスには 5 人の園児がいます。
# ゲーム中に、合計 3 回のじゃんけんが行われました。
# 1 回目のじゃんけんでは、出席番号 1 の園児が出席番号 2 の園児に勝ちます。
# 2 回目のじゃんけんでは、出席番号 3 の園児が出席番号 4 の園児に勝ちます。
# 3 回目のじゃんけんでは、出席番号 5 の園児が出席番号 3 の園児に勝ちます。

# ゲームが終わった時点で、

# ・出席番号 1 の園児が先頭の列 (長さ 2)
# ・出席番号 5 の園児が先頭の列 (長さ 3)

# ができています。よって、優勝者は出席番号 5 の園児となります。

# 入力例1
# 5 3
# 1 2
# 3 4
# 5 3

# 出力例1
# 5

kids_number, times = map(int, input().split())

trains = {i: [i] for i in range(1, kids_number + 1)}

print("trains", trains)

for _ in range(times):
  win_leader_input, lose_leader_input = map(int, input().split())
  
  trains[win_leader_input].extend(trains[lose_leader_input])

  #負けた列車の削除
  del trains[lose_leader_input]

print("trains2", trains)

max_length = 0
champion_leaders = []

for leader_kid, members in trains.items():
    current_length = len(members)
    if current_length > max_length:
        max_length = current_length
        champion_leaders = [leader_kid]
    elif current_length == max_length:
        champion_leaders.append(leader_kid)
        
sorted_champions = sorted(champion_leaders)

for champion in sorted_champions:
  print(champion)
