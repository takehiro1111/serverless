"""C126:宿泊費と交通費

あなたは、長期休みを利用して、いくつかのインターンシップに行くことにしました。

全てのインターンシップ先は同じ地域にありますが、あなたはその地域の遠くに住んでおりインターンシップ先には新幹線で移動しなければなりません。

幸運なことに、全てのインターンシップ先はあるホテルから徒歩で行くことができ、インターンシップ期間はそのホテルに宿泊します。
インターンシップ期間の宿泊費はインターンシップ先が負担しますが、交通費やインターンシップ期間外の宿泊費は自己負担となっています。

それぞれのインターンシップの間に、あなたはホテルに泊まり続けるか、一度家に帰るかを選択します。

ホテルに泊まり続ける場合は一泊ごとに宿泊費がかかりますが、新幹線に乗る必要はないので交通費はかかりません。
一方、家に帰る場合は、宿泊費はかかりませんが、往復の新幹線の交通費がかかってしまします。

あなたは自己負担する交通費と宿泊費の合計をできるだけ安くしつつ、すべてのインターンシップに参加したいです。
インターンシップの日程と、新幹線の片道の料金、ホテルの一泊あたりの料金の情報が与えられるので、
最も安く行動したときの自己負担額を計算するプログラムを作成してください。

入力例 1 では片道の交通費が 200 円、ホテルの宿泊費は 300 円です。



1 つ目のインターンシップは 1 日から 3 日の間に行われ、
これに参加するために片道の交通費 200 円を自己負担します。

2 つ目のインターンシップは 4 日から 6 日の間に行われるため、
次のインターンシップまでホテルに泊まり続ける場合は 1 泊分の料金 300 円がかかります。
新幹線で一度帰宅すると、往復の 400 円かかってしまうため、ホテルに泊まり続けたほうが自己負担額は安く抑えられます。

3 つ目のインターンシップは 8 日から 10 日の間に行われるため、
次のインターンシップまでホテルに泊まり続ける場合は 2 泊分の料金 600 円がかかります。
新幹線で一度帰宅すると、往復の 400 円で済むので、新幹線を利用して一度帰るほうが自己負担額は安く抑えられます。

3 つ目のインターンシップが終了し、帰宅するために片道の交通費 200 円を自己負担するので、
自己負担額の合計は 1,100 円となり、これが最安です。

※インターンシップは3つある。

入力例1
200 300 3
1 3
4 6
8 10

片道の新幹線の料金を表す整数 A ホテルの一泊あたりの料金を表す整数 B インターンシップの回数 N
A 200円 B 300円 N 3回
インターンシップの初日 最終日


出力例1
1100


入力例2
100 1 3
1 2
10 15
30 50

出力例2
223
"""

# 入力の受け取り
shinkansen, hotel, INTERNS = map(int, input().split())

# インターンの初日と最終日を受け取る。
start_day = []
last_day = []
for _ in range(INTERNS):
    start, last = map(int, input().split())
    start_day.append(start)
    last_day.append(last)

# print(start_day)
# print(last_day)
# [1, 4, 8]
# [3, 6, 10]

# 料金のカウンター
total_cost = 0

# 最安料金を計算する処理
for i, (st, la) in enumerate(zip(start_day, last_day)):

    # 初日の行きと最終日の交通費を加算。
    # 交通費のみなので処理を抜ける。
    if i == 0 or la == last_day[-1]:
        total_cost += shinkansen

    # 2回目以降のインターンの開始日と前回終了日の差が1日の場合は宿泊を選択する。
    if st - last_day[i - 1] == 1:
        total_cost += hotel

    # 2回目以降のインターンの開始日と前回終了日の差が2日以上の場合は交通費が往復で発生する。
    # 新幹線(片道)が宿泊費よりも安い場合
    elif st - last_day[i - 1] >= 2 and shinkansen < hotel:
        total_cost += shinkansen * 2

    # ホテル代の方が安い場合は宿泊日分のホテル代を払う。
    elif st - last_day[i - 1] >= 2 and hotel < shinkansen:
        total_cost += hotel * (st - last_day[i - 1])


print(total_cost)
