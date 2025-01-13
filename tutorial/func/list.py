l = [10, 20, 30]
add = [100, 200]

l.append(40)  # 末尾に挿入
l.insert(1, 15)  # インデックス,値
l.extend(add)  # 末尾にリストを挿入
l.pop(3)  # 指定された位置の要素を削除します。
l.pop()  # 引数を取らなければ末尾を削除します。
l.sort()  # sortメソッド .sort() は対象となるリストそのものを変更します。(参照渡し)
l.reverse()  # 順序の反転 (対象となるリストそのものを変更)

print(l)


lst = [4, 2, 3, 1]


print(sorted(lst))
print(list(reversed(lst)))

import copy

lstA = [40, 2, 30, 1]
lstB = copy.copy(lstA)
lstB.sort()
print(lstB)  # lstB = [1, 3, 2, 4]
print(lstA)  # lstA = [4, 2, 3, 1]


# 多次元配列を関数とリスト内包表記でリスト化したい場合
multi_dimensional_lists = [[1, 3], [1, 2, 3], [3, 2]]


def flatten(multi_dimensional_lists):
    flatten_list = [
        element for elements in multi_dimensional_lists for element in elements
    ]
    return flatten_list


def_flatten = flatten(multi_dimensional_lists)
print(def_flatten)
