"""
あなたの友人である K 氏は電子工作が大好きです。
彼は毎晩試行錯誤を重ね、最近ついにコンピュータのミニチュア版を開発することに成功しました。

彼のコンピュータはちょうど 2 つの変数を持っており、どちらの変数も 0 で初期化されています。
また、彼のコンピュータは次の 3 種類の命令を実行することができます。

・SET i a : 変数 i に値 a を代入する (i = 1, 2)
・ADD a :「変数 1 の値 + a」を計算し、計算結果を変数 2 に代入する
・SUB a :「変数 1 の値 - a」を計算し、計算結果を変数 2 に代入する

彼は、自分のコンピュータが正しく動いているかどうかチェックしてほしいと依頼してきました。
コンピュータが完成して嬉しそうな彼の頼みを断るわけにはいきません。
そんな彼のために、彼のコンピュータをシミュレートするプログラムを書きましょう。

次の図は入力例 1 における変数の値の変化を示しています。

入力例1
3
SET 1 10
SET 2 20
ADD 40

出力例1
10 50

入力例2
3
SET 1 -23
SUB 77
SET 1 0

出力例2
0 -100
"""

loop = int(input())

one = 0
two = 0

for i in range(loop):
    orders = [i for i in map(str, input().split())]

    if orders[0] == "SET":
        order, var, num = orders

        if int(num) != 0:
            if int(var) == 1:
                one = int(num)
            elif int(var) == 2:
                two = int(num)
        elif int(num) == 0:
            if int(var) == 1:
                one = 0
            elif int(var) == 2:
                two = 0

    elif orders[0] == "ADD":
        order, num = orders

        two = one + int(num)

    elif orders[0] == "SUB":
        order, num = orders

        two = one - int(num)

print(one, two)
