"""C129:工場の検品

ある工場では、寿司 1 から寿司 N までの N 種類の寿司を生産しており、M 個入りのパックにして出荷しています。
パックする際は、見栄えの観点から指定された順番に寿司を並べます。もっとも、寿司を指定の順番に並べる機械は投入される寿司に過不足があると正常に機能しません。そこで、あなたは機械に寿司を投入する前に、パックを作成するために流れてきた寿司を指定された順に並び替えることができるかチェックすることにしました。

指定の寿司の順番と、投入しようとしている寿司の情報が与えられるので、指定された順に並び替えることができるかチェックし、並び替えることができるなら Yes を出力し、できないなら No と出力するプログラムを作成してください。
入力例 1 では以下のようになります。

入力される値
入力は以下のフォーマットで与えられます。

N M
A_1
A_2
...
A_M
B_1
B_2
...
B_M

1 行目には、寿司の種類の数を表す整数 N と、パックされる寿司の個数を表す整数 M が半角スペース区切りで与えられます。
・続く M 行のうちの i 行目 (1 ≦ i ≦ M) には、i 番目に並べるべき寿司の番号を表す整数 A_i が与えられます。
・続く M 行のうちの j 行目 (1 ≦ j ≦ M) には、パックを作成するために j 番目に流れてきた寿司の番号を表す整数 B_j が与えられます。
・入力は合計で 1 + 2 × M 行となり、入力値最終行の末尾に改行が 1 つ入ります。

期待する出力
投入しようとしている寿司を指定された順に並べることができる場合は "Yes" を、そうでない場合は "No" を出力してください。
末尾に改行を入れ、余計な文字、空行を含んではいけません。
"""

# 入力
## 寿司の種類の数と寿司の情報の受け取り
sushi_types, sushi_count = list(map(int, input().split()))
# 3 5

## i 番目に並べるべき寿司の番号を表す整数 A_iの受け取り
sort_order = [int(input()) for i in range(1, sushi_count + 1)]
print(sort_order)
# [1,2,1,2,3]

## パックを作成するために j 番目に流れてきた寿司の番号を表す整数 B_jの受け取り
random_order = [int(input()) for i in range(1, sushi_count + 1)]
print(random_order)
# [2, 1, 3, 2, 1]

result = []
for target in sort_order:
    print(f"target:{target}")
    for i, num in enumerate(random_order):
        print(f"num:{num}")
        if num == target:
            result.append(num)
            break

# 二重ループの出力
# target:1
# num:2
# num:1
# target:2
# num:2
# target:1
# num:2
# num:1
# target:2
# num:2
# target:3
# num:2
# num:1
# num:3

print("Yes" if result == sort_order else "No")

# 処理
# sorted_pairs = sorted(zip(sort_order,random_order))
# print(sorted_pairs)

# sorted_list2 = [i[1] for i in sorted_pairs]
# print(sorted_list2)

# indices = sorted(range(len(sort_order)), key = lambda i: sort_order[i])
# print(indices)
# sorted_list = [random_order[i] for i in indices]
# print(sorted_list)

# 出力
