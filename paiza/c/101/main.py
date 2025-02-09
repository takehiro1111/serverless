"""C101:【2021年Xmas問題】ラッキーデイ
あなたは年初めの占いで、1 月 1 日からの経過日数にある数字 X が含まれる日は、幸運な日であることを知りました。
そのような日は 1 年にいくつあるでしょうか。数字 X が与えられるので、1 年のうち幸運な日がいくつあるのか答えてください。
ただし、1 年は 365 日であり、1 月 1 日から 0 日目である 1 月 1 日も幸運な日となりえるとします。

入力例 1 の場合、1 月 1 日からの経過日数のうち 15 の数字が入る日は 15, 115, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 215, 315 日目であるので、合計 14 日となります。
したがって、期待される出力は 14 となります。

入力例1
15
出力例1
14
入力例2
128
出力例2
1
入力例3
6
出力例3
68
"""

X = str(input())

count = 0
for i in range(365):
    if X in str(i):
        count += 1

print(count)
