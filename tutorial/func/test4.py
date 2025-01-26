# count = 0

# while count < 5:
#   n = int(input())
#   if 1 <= n <= 100:
#     numbers.append(n)
#   count += 1

# print(f"最小値:{min(numbers)}")

# numbers = []
# for _ in range(1,6):
#   num = (int(input()))
#   if 1 <= num <= 100:
#     numbers.append(num)

# print(min(numbers))


# numbers = []
# for _ in range(5):
#     itr = int(input())
#     if 1 <= itr <= 100:
#         numbers.append(itr)

# print(min(numbers))

# num = 0
# while num < 2:
#     input_line = input()
#     print(input_line)
#     num += 1

# for _ in range(2):
#   input_line = input()
#   print(input_line)
# The line `l = ["hello", "paiza"]` is creating a list named `l` with two elements: "hello" and
# "paiza".

# l = ["hello" ,"paiza"]
# answer = list(map(str,l))

# print(answer)

# splitで取得するとリストになる。
# str = input().split()
# print(str)
# for i in str:
#     print(i)


# リスト内包表記
# [print(x) for x in input().split()]

# map関数
# list(map(print, input().split(' ')))

# # join + 改行
# print('\n'.join(input().split()))

# text = "hello   world"
# print(text.split())      # ['hello', 'world']
# print(text.split(' '))   # ['hello', '', '', 'world']

# A,B,C = list(map(int,input().split()))

# N = 0
# N += A
# N *= B
# N %= C

# print(f"{int(N)}")

# A,B,C = input().split()
# num = int(A) - int(B) + int(C)


# print(num)

# input_line = input()
# if input_line == "paiza":
#   print('YES')
# else:
#   print("NO")

# input_line = input()
# length = len(input_line)
# ite = int(length) + 2

# print("+" * ite )
# print(f"+{input_line}+")
# print("+" * ite )
# print(f"+{input_line}+")
# print("+++++++")


# 5 10
# 5
# 11
# 20
# 8
# 7


# number_enemies,my_first_level = list(map(int,input().split()))
# for _ in range(number_enemies):
#     enemies_level = int(input())
#     # 勝ちの時
#     if int(my_first_level) > enemies_level:
#         # 相手のレベルを2で割って切り捨てた数値を自分のレベルに加算する。
#         my_first_level += (enemies_level // 2)

#     # 引き分けの時
#     elif int(my_first_level) == enemies_level:
#       continue

#     # 負けの時
#     elif int(my_first_level) < enemies_level:
#       # 自分のレベルから//2する。
#        my_first_level //= 2

# print(my_first_level)


# ceil() 切り上げ
# floor() 切り下げ


# number_enemies,my_first_level = (int(x) for x in input().split())
# # number_enemies,my_first_level = list(map(int,input().split()))
# print(number_enemies)
# print(my_first_level)
# list_x = []

# for i in range(number_enemies):
#     enemies_level = int(input())
#     print(f"enemies_level:{enemies_level}")
#     list_x.append(enemies_level)

# for list_enemies_level in list_x:
#     if my_first_level > list_enemies_level:
#         my_first_level += (list_enemies_level // 2)
#         print(f"list_enemies_level:{list_enemies_level}")
#         print(f"my_first_level:{my_first_level}")
#     elif my_first_level < list_enemies_level:
#         my_first_level = my_first_level // 2
#         print(f"list_enemies_level:{list_enemies_level}")
#         print(f"my_first_level:{my_first_level}")
# print(my_first_level)


# import math

# box = int(input())
# # リスト
# depth = list(map(int,input().split()))

# # total = 0
# # for i in depth:
# #     total += i

# # avg = int(total) / box
# result = math.ceil(sum(depth) / box)
# print(result)


# CARS, TRAFFIC_JAM = list(map(int,input().split()))
# traffic = 0
# for _ in range(4):
#   distance = int(input())
#   if distance <= TRAFFIC_JAM:
#     traffic += distance
#   elif distance > TRAFFIC_JAM:
#     continue

# print(int(traffic))

# CARS, TRAFFIC_JAM = map(int,input().split())
# traffic = 0
# for _ in range(CARS-1):
#   distance = int(input())
#   if distance <= TRAFFIC_JAM:
#     traffic += distance
#   else:
#     continue
# print(traffic,end="\n")

# want_to_eat = input()
# num = int(input())
# MENU = input().split()

# if want_to_eat in  MENU:
#   print("Yes")
# else:
#   print("No")


# 変数xとyはcase内で初めて定義される
# def analyze_point(point):
#     match point:
#         case (0, 0):
#             return "原点"
#         case (0, y):  # yが初めて定義される
#             return f"y軸上の点 (y={y})"
#         case (x, 0):  # xが初めて定義される
#             return f"x軸上の点 (x={x})"
#         case (x, y):  # xとyが初めて定義される
#             return f"座標- ({x}, {y})"


# # 使用例
# point = (5, 3)
# result = analyze_point(point)  # 座標 (5, 3) が返される
# print(result)

# count = 1
# for i in range(4):
#     translate = int(input())
#     count = abs(translate - count)  # 現在の値と次の値の差の絶対値

# print(count)
 
    
# # 入力でエレベーターが動く回数を定義
# num = int(input())

# # カウンター(初回の階数)を定義
# count = 1

# # エレベーターが何階分の距離を動いたか定義
# answer = 0

# for _ in range(num):
#     # 今回エレベーターが停まる階数
#     floor = int(input())
    
#     # 前の処理でエレベーターが止まった階との差を加算
#     answer += abs(floor - count)
    
#     # 前回記録として次の処理で差を測るための値を記録(初期化)
#     count = floor
    
# print(answer)



#ポイント
## 入力をどう受け取るか。
## 条件分岐
### 大文字か小文字か区別する

# NGワードを定義
# WORD = str(input())

# # メールの件数
# NUMBER = int(input())

# for _ in range(NUMBER):
#     # メッセージの入力をキャッチ
#     MESSAGE = str(input())
    
#     # "Free"のみ大文字で始まるかチェック’
#     ## "Free"が無いものをフィルターして除外
#     words = MESSAGE.split()
#     for i,word in enumerate(words):
#         if WORD in word:
#             FREE = word
#             print(FREE)
#         else:
#             continue
        
#     if WORD  in FREE :
#         print("Yes")
#     else:
#         print("No")





# WORD = str(input())
# NUMBER = int(input())

# for _ in range(NUMBER):
#    MESSAGE = str(input())
#    found = False
   
#    words = MESSAGE.split()
#    for word in words:
#        # 大文字小文字を区別して完全一致でチェック 
#        if WORD == word or WORD in word:
#            found = True
#            break
           
#    print("Yes" if found else "No")


# t = "TanakaTakehiro"
# ans = t.count("Ta")
# print(ans)


# --PA-I---ZA
# -PA-I-ZA
# 2つ以上のハイフンを1つに統一する。

# import re

# PAIZA = input()
# paiza_sub = re.sub('-{2,}',"-",PAIZA)

# print(paiza_sub)




