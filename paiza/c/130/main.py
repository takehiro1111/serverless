"""C130:繰り返し学習
あなたは、ある問題集を解いていて、全ての問題を完璧に解けるようにしようと思っています。
既に解けるようになった問題を何度も解くのは時間の無駄であると考えたため、はじめの 2 周は全ての問題を解きますが 3 周目では 1, 2 周目両方で正解した問題は解かないことにしました。
1 周目および 2 周目のそれぞれの問題の正誤状況が与えられるので、3 周目で解かなければならない問題の番号を、番号の小さい順に出力するプログラムを作成してください。

入力例1
4
y n
n y
n n
y y

出力例1
3
1
2
3
"""

# yyの問題は3週目以降はスキップする。

# 問題数を入力から受け取り、定数として定義。
QUESTIONS = int(input())

answers = []
# 問題ごとに3週目を解く必要があるかどうかを判定する。

for i in range(1, QUESTIONS + 1):
    # 問題の正誤を入力から受け取る。
    fist, second = list(map(str, input().split()))

    # いずれかが正解ではない場合はイテレータを記録するためリストへ追加処理
    if fist != "y" or second != "y":
        # 問題番号を記録するためにrangeの番号をリストへ追加する。
        answers.append(i)


print(len(answers))
for num in answers:
    print(num)


QUESTIONS = int(input())
answers = []

for i in range(1, QUESTIONS + 1):
    first, second = input().split()
    if first != "y" or second != "y":
        answers.append(i)

print(len(answers))
for num in answers:
    print(num)
