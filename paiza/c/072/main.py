"""
あなたの育成するモンスターは日々成長しています。モンスターは成長すると進化をします。
モンスターがどのモンスターに進化するかは攻撃力、防御力、素早さの 3 つのパラメータによって決まります。
このとき、モンスターの持つパラメータによっては進化条件を満たすモンスターが複数存在する場合や、存在しない場合があります。

あなたのモンスターのパラメータと、それぞれ進化先のモンスターのモンスター名、進化条件が与えられるので、進化条件を満たすモンスター名を全て出力してください。
進化条件をみたすモンスターがいない場合は "no evolution" と出力してください。

例として、次のようなモンスターのパラメータと進化先それぞれのモンスターの能力の条件が与えられた場合を考えます。
この場合、攻撃力と防御力では paizabird と paizasheep へ進化する条件を満たし、素早さでは paizasheep へ進化する条件のみを満たすので、進化先のモンスターの名前は paizasheep の 1 つになります。

入力される値
入力は以下のフォーマットで与えられます。

ATK DEF AGI
N
s_1 MINATK_1 MAXATK_1 MINDEF_1 MAXDEF_1 MINAGI_1 MAXAGI_1
s_2 MINATK_2 MAXATK_2 MINDEF_2 MAXDEF_2 MINAGI_2 MAXAGI_2
...
s_N MINATK_N MAXATK_N MINDEF_N MAXDEF_N MINAGI_N MAXAGI_N
・1 行目にはそれぞれ、モンスターの現在の攻撃力、防御力、素早さを表す 3 つの整数 ATK, DEF, AGI がこの順で半角スペース区切りで与えられます。
・2 行目には進化先のモンスター数を表す整数 N が与えられます。
・続く N 行のうち、i 行目 (1 ≦ i ≦ N) には、i 番目の進化先のモンスターの名前を表す文字列 s_i と進化条件を表す 6 つの整数 MINATK_i, MAXATK_i, MINDEF_i, MAXDEF_i, MINAGI_i, MAXAGI_i がこの順で半角スペース区切りで与えられます。
　・s_i はモンスターの名前を表す、小文字の英字からなる文字列です。
　・MINATK_i, MAXATK_i は攻撃力の条件を表し、このモンスターに進化するには攻撃力が MINATK_i 以上 MAXATK_i 以下である必要があります。
　・MINDEF_i, MAXDEF_i は防御力の条件を表し、このモンスターに進化するには防御力が MINDEF_i 以上 MAXDEF_i 以下である必要があります。
　・MINAGI_i, MAXAGI_i は素早さの条件を表し、このモンスターに進化するには素早さが MINAGI_i 以上 MAXAGI_i 以下である必要があります。
・入力は合計で N + 2 行からなり、末尾には改行が 1 つ入ります。

入力例1
100 150 200
3
paizabird 100 200 130 180 80 120
paizawolf 180 220 100 120 90 140
paizasheep 80 110 150 220 170 250

出力例1
paizasheep
"""

attack, defence, rapidly = map(int, input().split())

# 進化先モンスターの情報を格納
evolution_list = []
evolved = []

# 進化先データの取得
for _ in range(int(input())):
    data = input().split()
    evolution_list.append(
        {
            "name": data[0],
            "atk": tuple(map(int, data[1:3])),
            "df": tuple(map(int, data[3:5])),
            "rap": tuple(map(int, data[5:])),
        }
    )

# 進化判定
for monster in evolution_list:
    if (
        monster["atk"][0] <= attack <= monster["atk"][1]
        and monster["df"][0] <= defence <= monster["df"][1]
        and monster["rap"][0] <= rapidly <= monster["rap"][1]
    ):
        evolved.append(monster["name"])

print("no evolution" if not evolved else "\n".join(evolved))

# 攻撃 防御 素早さの現在の数値
# 100 150 200
# attack, defence, rapidly = map(int,input().split())

# # 要素数
# TOTAL = int(input())

# # 進化先モンスターの情報を格納する辞書のリスト
# evolution_list = []

# ## 進化の種別と基準の数値の入力をどのように受け取って処理に繋げれば良いかが全くイメージできない。
# for _ in range(TOTAL):
#   data = input().split()
#     # ['paizabird', '100', '200', '130', '180', '80', '120']
#     # ['paizawolf', '180', '220', '100', '120', '90', '140']
#     # ['paizasheep', '80', '110', '150', '220', '170', '250']
#   # 文字と数値を分解
#   evolution_name = data[0]
#   conditions = list(map(int,data[1:]))

#   # 辞書として保存
#   monster = {
#     "name": evolution_name,
#     "atk": (conditions[0],conditions[1]),
#     "df": (conditions[2],conditions[3]),
#     "rap": (conditions[4],conditions[5]),
#   }

#   evolution_list.append(monster)
# # print(evolutions)
# # [
# #   {'name': 'paizabird', 'atk': (100, 200), 'df': (130, 180), 'rap': (80, 120)},
# #   {'name': 'paizawolf', 'atk': (180, 220), 'df': (100, 120), 'rap': (90, 140)},
# #   {'name': 'paizasheep', 'atk': (80, 110), 'df': (150, 220), 'rap': (170, 250)}
# # ]

#   ## 判定


# def judge(m,a=attack,d=defence,r=rapidly):
#   if (m["atk"][0] <= a <= m["atk"][1] and m["df"][0] <= d <= m["df"][1] and m["rap"][0] <= r <= m["rap"][1]):
#       evolution_list.append(m["name"])
