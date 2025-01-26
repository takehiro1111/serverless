"""
配列 A の要素数 N と整数 K, 配列 A の各要素 A_1, A_2, ..., A_N が与えられるので、
配列 A に K がいくつ含まれるか数えてください。

入力例1
1 2
1

出力例1
0

[登場要素]
A -> 配列
N -> 要素数
K -> 整数
A_1 配列の各要素
"""

# 要素数 N , 整数 K
n,k = map(int,input().split())

a = [int(input()) for _ in range(n)]
ans= 0

for i in a:
  if i == k:
    ans += 1
    
print(ans)




