"""C040:【ロジサマコラボ問題】背比べ
何やら子供たちが集まって背比べをしています。
話を聞いてみると、一人の子供をのぞいて他の子供の身長は正確にわかっており、
その一人の子供の身長を他の子どもと比べることで測ろうとしているようです。
手助けをしてあげましょう。

ここでは 6 人の子供の身長がわかっており、
この子供たちともう一人の子供の身長を比較すると上のようになりました。
これらの結果をまとめると身長のわかっていない子供の身長は
116.9cm 以上 117.6cm 以下であることがわかります (入力例 1)。


他の同じような状況の子供たちのためにもこれを自動化するプログラムをつくりましょう。

入力例1
6
le 120.3
ge 115.7
le 122.0
ge 116.9
le 119.1
le 117.6

出力例1
116.9 117.6
"""

# 入力
## 比較する子供の人数
CHILDREN = int(input())

le = []  # 求めたい身長はこの要素以下
ge = []  # 求めたい身長この要素以上

## 比較結果と比較対象の身長
for i in range(CHILDREN):
    result, height = map(str, input().split())

    if result == "le":
        le.append(float(height))
    elif result == "ge":
        ge.append(float(height))

min_le = min(le)
max_ge = max(ge)

print(f"{max_ge} {min_le}")


### 辞書を用いた書き方
n = int(input())
heights = {"le": [], "ge": []}
for _ in range(n):
    comp, height = input().split()
    heights[comp].append(float(height))
print(f"{max(heights['ge'])} {min(heights['le'])}")


### classでの書き方
class HeightComparer:
    def __init__(self):
        self.le_heights = []
        self.ge_heights = []

    def add_comparison(self, comp, height):
        if comp == "le":
            self.le_heights.append(float(height))
        else:
            self.ge_heights.append(float(height))

    def get_range(self):
        return f"{max(self.ge_heights)} {min(self.le_heights)}"


n = int(input())
comparer = HeightComparer()
for _ in range(n):
    comp, height = input().split()
    comparer.add_comparison(comp, height)
print(comparer.get_range())


### reduce関数での書き方
from functools import reduce

n = int(input())


def process_height(acc, _):
    comp, height = input().split()
    acc[0 if comp == "ge" else 1].append(float(height))
    print(f"acc:{acc}")
    return acc


heights = reduce(process_height, range(n), [[], []])
print(heights)  # [[115.7, 116.9], [120.3, 122.0, 119.1, 117.6]]
print(f"{max(heights[0])} {min(heights[1])}")
