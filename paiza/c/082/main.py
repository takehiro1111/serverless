"""C082:【推しプロコラボ問題】テストの赤点

Paiza 高校で英語、国語、数学の 3 科目のテストがありました。

Paiza 高校ではテストを受けた X 人に対して、科目ごとに、下から Y 位までの生徒を赤点としています。ただし、下から Y 位の生徒が複数いた場合、その全員が赤点となります (全員が同じ点数だった場合は全員が下から 1 位なので赤点となります)。
また、下から i 位 (1 ≦ i ≦ X-1) の生徒が複数いた場合、次の順位はその人数分飛ばされます (下の図の国語の列を参考にしてください)。

入力例 1 では以下のようになります。

生徒の数は 4 人、下から 2 位までが赤点となります。

図1

テストを受けた生徒の人数 X、赤点となってしまう下からの順位 Y、各生徒の科目ごとの点数が与えられるので、
それぞれの生徒がいくつ赤点を取ったか出力してください。

入力例1
4 2
80 60 40
50 50 40
80 50 40
40 80 80

出力例1
1
3
2
1

"""

# 入力
X, Y = map(int, input().split())

# 生徒の成績を二次元配列で保持
scores = []
for _ in range(X):
    scores.append(list(map(int, input().split())))


# 教科ごとに赤点を判定する関数
def get_red_marks(subject_scores, Y):
    # 点数でソート（降順）
    sorted_scores = sorted(subject_scores, reverse=True)
    # 赤点となる基準点（下からY位の点数）
    red_mark_threshold = sorted_scores[-Y]
    # 赤点の生徒のインデックスを記録
    red_mark_students = []

    for i, score in enumerate(subject_scores):
        if score <= red_mark_threshold:
            red_mark_students.append(i)

    return red_mark_students


# 各教科の点数リストを作成
english = [score[0] for score in scores]
japanese = [score[1] for score in scores]
math = [score[2] for score in scores]


# 各教科の赤点者を取得
eng_red = get_red_marks(english, Y)
jp_red = get_red_marks(japanese, Y)
math_red = get_red_marks(math, Y)

# 生徒ごとの赤点数をカウント
for student in range(X):
    red_count = 0
    if student in eng_red:
        red_count += 1
    if student in jp_red:
        red_count += 1
    if student in math_red:
        red_count += 1
    print(red_count)


# 入力
## 生徒の人数 X 下からの順位 Y
X, Y = map(int, input().split())

## 生徒の成績
### 二次元配列 or リストの中の辞書

scores = []
for i in range(X):
    english, japanese_language, mathematics = map(int, input().split())

    score_dict = {
        "英語": english,
        "国語": japanese_language,
        "数学": mathematics,
    }
    scores.append(score_dict)

# [{'英語': 80, '国語': 60, '数学': 40},
#  {'英語': 50, '国語': 50, '数学': 40},
#  {'英語': 80, '国語': 50, '数学': 40},
# {'英語': 40, '国語': 80, '数学': 80}]


## 科目ごとに点数を並べる。
eng = []
lang = []
math = []

# 処理
## 二重ループを用いて各教科で赤点の該当数を算出
for j in scores:
    for k, v in j.items():
        if k == "英語":
            eng.append(v)
        elif k == "国語":
            lang.append(v)
        elif k == "数学":
            math.append(v)

# eng  [80, 50, 80, 40]
# lang [60, 50, 50, 80]
# math [40, 40, 40, 80]


# 出力
# sort_eng = sorted(eng,reverse=True) # [80, 80, 50, 40]
# sorted_lang = sorted(lang)
# sorted_math = sorted(math)
# print(sort_eng)

# 下位2人に当てはまる場合は赤点 & 下位2人以上の点数が同列の場合も赤点とみなす。


def judge(subject_score):
    sort_scores = sorted(subject_score, reverse=True)
    # 赤点の基準点（下からY位の点数）
    red_mark_threshold = sort_scores[-Y]

    red_students = []
    for i, score in enumerate(subject_score):
        if score <= red_mark_threshold:
            red_students.append(i)

    return red_students


eng_red = judge(eng)
jp_red = judge(lang)
math_red = judge(math)

print(eng_red)
print(jp_red)
print(math_red)

# 教科ごとの赤点取得者
# loop = [eng,lang,math]
# for i in loop:
#   red_holders = judge(i)
#   print(red_holders)


# 生徒毎に赤点保持数
for student in range(X):
    red_count = 0
    # 生徒の赤点保持数を判定する必要があるため教科ごとにifを使用した逐次処理で良い。
    # elifではなく、ifで教科ごとに完結させている。
    if student in eng_red:
        red_count += 1
    if student in jp_red:
        red_count += 1
    if student in math_red:
        red_count += 1
    print(red_count)
