l = [3, 1, 4, 5, 2]


for h in range(len(l)):
    min = h
    for i in range(min + 1, len(l)):
        if l[min] > l[i]:
            # 暫定的な一番小さい要素を持っているインデックスを変数で保持する。
            min = i

    # 「未ソート部分の先頭の値(l[h])」と「その範囲で見つかった最小の値(l[min])」を入れ替える、
    l[h], l[min] = l[min], l[h]

print(l)
