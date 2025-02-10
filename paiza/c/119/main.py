"""C119:お菓子かいたずらか
今日はハロウィン。Paiza 町に住む女の子 Alice は、お菓子を貰いに近所の家を巡ろうと考えました。
Paiza 町には N 軒の家があり、それぞれ 1 から N で番号付けられています。
Alice は 1 番の家から順にインターホンを押して回り、すべての家を回り終えると自宅に帰ります。

一方で、Paiza 町に住む M 人の男の子たちが、お菓子をもらえなかった腹いせに、それぞれ N 軒の家のどこかに隠れて、お菓子を貰いに来た子供を驚かせているようです。
Alice は怖がりな子であるため、驚かされてしまったらお菓子を貰わずに次の家を目指し一目散に走りだします。
しかし、次の家でもまた驚かされてしまうかもしれません。
Alice は K 軒の家で連続して驚かされると、泣き出して自宅に帰ってしまいます。

M 人の男の子たちが隠れている家がわかるとき、Alice が貰えるお菓子の個数を計算するプログラムを作成してください。
以下の図に示す例では 2 軒の家でお菓子をもらうことができます。

入力例1
6 3 2
2
4
5

出力例1
2

入力例2
10 4 3
1
5
6
9

出力例2
6
"""

# 家の軒数 男の子の人数 Aliceが泣き出して帰る軒数(連続記録が成立する数)
HOUSES, MEN, CRY_HOUSES = map(int, input().split())
# 6 3 2

men_hidden = []
# [2,4,5]
# [1,5,6,9]
for i in range(MEN):
    men = int(input())
    men_hidden.append(men)

total_count = 0
continuous_scares = 0  # 連続で驚かされた回数

for house in range(1, HOUSES + 1):
    if house in men_hidden:
        continuous_scares += 1
        if continuous_scares >= CRY_HOUSES:
            break

    else:
        total_count += 1  # お菓子がもらえる
        continuous_scares = 0  # 連続カウントをリセット

print(total_count)
