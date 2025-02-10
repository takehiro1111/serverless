"""C035:試験の合格判定

総合力を重視する paiza 大学の入試では 1 次試験 (英語、数学、理科、国語、
地理歴史の 5 科目で各 100 点満点) の成績で2段階選抜を行います。
2段階選抜を通過する条件は以下のようになっています。

全科目の合計得点が 350 点以上
理系の受験者の場合は理系 2 科目 (数学、理科) の合計得点が 160 点以上
文系の受験者の場合は文系 2 科目 (国語、地理歴史) の合計得点が 160 点以上
受験者それぞれの各科目の点数が入力されるので、何人2段階選抜を通過できるかを求めてください。

例）

図1

受験者 2 は全科目の合計は 350 点以上ですが文系 2 科目の合計が 160 点未満なので不合格。
一方受験者 4 は理系 2 科目の合計は 160 点以上ですが全科目の合計が 350 点未満なので不合格となります。

→ 通過人数: 2 人

これは入力例 1 に対応しています。

入力例1
5 受験者数
s 70 78 82 57 74
l 68 81 81 60 78
s 63 76 55 80 75
s 90 100 96 10 10
l 88 78 81 97 93

※試験の通過人数
出力例1
2
"""

# 受験者数の受け取り
N = int(input())

successful_applicants = 0

for i in range(N):
    scores = [str(x) for x in input().split()]
    scores_int = [int(y) for y in scores[1:]]

    if scores[0] == "s":
        if scores_int[1] + scores_int[2] >= 160 and sum(scores_int) >= 350:
            successful_applicants += 1
    elif scores[0] == "l":
        if scores_int[3] + scores_int[4] >= 160 and sum(scores_int) >= 350:
            successful_applicants += 1

print(successful_applicants)


# ['s', '70', '78', '82', '57', '74']
# ['l', '68', '81', '81', '60', '78']
# ['s', '63', '76', '55', '80', '75']
# ['s', '90', '100', '96', '10', '10']
# ['l', '88', '78', '81', '97', '93']


def check_exam(n, data):
    count = 0
    for student in data:
        course_type = student[0]
        scores = list(map(int, student[1:]))
        total = sum(scores)

        science_total = scores[1] + scores[2]  # 数学、理科
        lit_total = scores[3] + scores[4]  # 国語、地理歴史

        if course_type == "s":  # 理系
            if total >= 350 and science_total >= 160:
                count += 1
        elif course_type == "l":  # 文系
            if total >= 350 and lit_total >= 160:
                count += 1
    return count


n = int(input())
data = [input().split() for _ in range(n)]
# [['s', '70', '78', '82', '57', '74'], ['l', '68', '81', '81', '60', '78'], ['s', '63', '76', '55', '80', '75'], ['s', '90', '100', '96', '10', '10'], ['l', '88', '78', '81', '97', '93']]
print(check_exam(n, data))
