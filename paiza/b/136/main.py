# 今日はバレンタインデー。チョコレートが大好きなあなたはこの日を待ちわびていました。

# クラスの席は H × W 席からなり、あなたを含めた H × W 人のクラスメイトが座っています。

# あなたは、自分の席から移動してクラスメイトの座席を回り、チョコレートをもらいます。
# あなたは律儀なので、もらった分だけお返しがしたいです。

# あなたの移動経路、および各席に座っているクラスメイトがくれるチョコレートの数が与えられるので、
# チョコレートをもらった順番に貰ったチョコレートの個数を記録するプログラムを作成してください。
# ただし、あなたは席のない場所には移動せず、また同じ席に二度以上訪れることはありません。

# 例えば入力例 1 の場合以下のようになります

# 入力例1
# 3 3 3
# 2 1
# FRB
# 3 6 2
# 0 4 1
# 5 0 7

# 出力例1
# 3
# 6
# 4



# 移動回数を表す N、クラスの縦の席数 H、クラスの横の席数 W
n, h, w = map(int, input().split())

# あなたの座席が前から何列目かを表す sy と 左から何列目かを表す sx 
sy, sx = map(int, input().split())

# s の i 文字目 (1 ≦ i ≦ N) は、前方向に移動する場合 "F"、後方向に移動する場合 "B"、左方向に移動する場合 "L"、右方向に移動する場合 "R" 
s = list(input())

# 座席の座標

# [[3, 6, 2], [0, 4, 1], [5, 0, 7]]
seats_row = []
for i in range(h):
  row = list(map(int, input().split()))
  seats_row.append(row)
  

current_row = sy - 1
current_col = sx - 1

collected_chocolates = []

for move_direction in s:
    if move_direction == 'F':
        current_row -= 1
    elif move_direction == 'B':
        current_row += 1
    elif move_direction == 'L':
        current_col -= 1
    elif move_direction == 'R':
        current_col += 1
    
    chocolates_at_current_seat = seats_row[current_row][current_col] 
    
    collected_chocolates.append(chocolates_at_current_seat)

# 結果の出力
for chocolates in collected_chocolates:
    print(chocolates)
