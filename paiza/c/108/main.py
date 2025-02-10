"""C108:【50万人記念問題】観光の計画
あなたはある都市に旅行にいくことになりました。
その都市には、観光名所がいくつかあり、各観光名所の所要時間と各観光名所間の移動にかかる時間がわかっています。
訪れたい観光名所がリストで与えられるので、与えられた順に観光名所を訪れた際どれくらい時間がかかるのか求めてください。
最初の観光名所を巡り始めるところから時間を計るものとします。

入力例 1 の場合、以下のように、観光名所の所要時間と移動時間が与えられています。

観光名所 1 で時間 2, 観光名所 1 から 2 に移動するのに時間 3 かかります。
観光名所 2 で時間 1, 観光名所 2 から 3 に移動するのに時間 8 かかります。
観光名所 3 で時間 4, 観光名所 3 から 1 に移動するのに時間 2 かかります。
最後にまた観光名所 1 で時間 2 必要なので、全部で時間 22 かかります。

入力例1
3 観光名所の数
2 観光名所の滞在時間(1)
1 観光名所の滞在時間(2)
4 観光名所の滞在時間(3)
0 3 2
3 0 8
2 8 0
4 観光名所の数
1
2
3
1

出力例1
22
"""

# 観光名所の数
NUM = int(input())

# 観光名所の滞在時間
stay_hours = []
# [2,1,4]
for i in range(NUM):
    stay_place = int(input())
    stay_hours.append(stay_place)

distance_list = []
# [[0, 3, 2], [3, 0, 8], [2, 8, 0]]
for i in range(NUM):
    distance = list(map(int, input().split()))
    distance_list.append(distance)

# 実際に赴く名所の数
go_place = int(input())
# 4

# 観光地の番号のリスト
visit_order = []
for i in range(go_place):
    place = int(input())
    visit_order.append(place - 1)


# stay_hours = [2,1,4] -> 各名所での観光時間
# distance_list = [[0, 3, 2], [3, 0, 8], [2, 8, 0]] -> 移動の所要時間
# visit_order = [1, 2, 3, 1]


## メイン処理
# 最初の観光名所での滞在時間
total_time = 0
total_time += stay_hours[visit_order[0]]

print(stay_hours)  # [2, 1, 4]
print(visit_order)  # [0, 1, 2, 0]
print(distance_list)  # [[0, 3, 2], [3, 0, 8], [2, 8, 0]]

# 1.前の場所から現在の場所への移動時間を加算
# 2.現在の場所での滞在時間を加算
for i in range(1, go_place):
    # 移動時間の加算
    ## 1から2に移動するところからスタート
    prev_place = visit_order[i - 1]  # 0
    current_place = visit_order[i]  # 1
    total_time += distance_list[prev_place][current_place]  # 3

    # 滞在時間の加算
    total_time += stay_hours[current_place]  # 1
    # 3(移動時間) + 1(滞在時間) = 1回目のループで4hを加算

print(total_time)

"""
・各名所での観光時間
  stay_hours = [2,1,4]

・観光地間の移動時間
  distance_list = [[0, 3, 2], [3, 0, 8], [2, 8, 0]]
  visit_order = [0, 1, 2, 0]

0.最初のステップ（観光名所1）:
  滞在時間: stay_hours[1 -1] -> 2を加算
  合計時間: 2

1.ループ1回目（1→2の移動）:
  前の場所: visit_order[0] -> 1
  現在の場所: visit_order[1] -> 2
  移動時間: distance_list[1-1][2-1] -> distance_list[0][1] -> 3を加算
  滞在時間: stay_hours[2-1] -> 1を加算
  合計時間: 3 + 1 = 4

2.ループ2回目（2→3の移動）:
  前の場所: visit_order[1] -> 2
  現在の場所: visit_order[2] -> 3
  移動時間: distance_list[2-1][3-1] -> distance_list[1][2] -> 8を加算
  滞在時間: stay_hours[3-1] -> 4を加算
  合計時間: 8 + 4 = 12

3.ループ3回目（3→1の移動）:
  前の場所: visit_order[2] -> 3
  現在の場所: visit_order[3] -> 1
  移動時間: distance_list[3-1][1-1] -> distance_list[2][0] -> 2を加算
  滞在時間: stay_hours[1-1] -> 2を加算
  合計時間: 2 + 2 = 4

  total_time = 22h
"""
