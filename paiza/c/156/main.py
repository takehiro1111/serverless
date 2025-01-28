"""C156:勤怠管理
あなたは論文の提出が迫っており、向こう N 日間毎日研究室に通って作業することにしました。
その N 日間で、合計でどれだけの時間研究室にいたかを後で見返そうと思ったあなたは、その N 日間は毎日入室時間と退室時間を記録することにしました。

N 日間の研究室への入室時間と退室時間がそれぞれ与えられるので、合計何時間何分研究室にいたかを求めるプログラムを作成してください。

入室時刻と退室時刻は 24 時間表記で hh:mm の形式で与えられます。また、必ず入室日と退室日は同じで、退室時刻はその日の入室時刻の後です。

入力例 1 の場合、5 日間研究室に通いました。

各日の入退室時間は次の通りであり、そこから在室時間を計算します。在室時間の合計は38時間16分となるので、38 16 と出力します。


入力例1
5
07:11 17:09
11:10 23:00
13:11 13:20
00:59 08:08
08:23 17:33

出力例1
38 16
"""

from datetime import datetime

# 入力(入退室の回数)の受け取り
N = int(input())

# 合計時間を入れていく変数
total_minutes = 0

# 時刻の差を計算
for _ in range(N):

    # 時刻の受け取り
    enter, exit = input().split()
    print(f"enter:{enter}")  # enter:07:11(1巡目)
    print(f"exit:{exit}")  # exit:17:09(1巡目)

    # 時刻の計算ができるようdatetime型への変換
    s_format = "%H:%M"
    enter_time = datetime.strptime(enter, s_format)
    exit_time = datetime.strptime(exit, s_format)
    print(f"enter_time:{enter_time}")  # enter_time:1900-01-01 07:11:00(1巡目)
    print(f"exit_time:{exit_time}")  # exit_time:1900-01-01 17:09:00(1巡目)

    # 時間差の計算
    ## diffにはtimedeltaオブジェクトが返される。
    diff = abs(exit_time - enter_time)
    print(f"diff:{diff}")  # diff:9:58:00(1巡目)

    # 時刻を秒に変換する。
    ## timedeltaオブジェクトのため。
    print(f"diff.seconds:{diff.seconds}")  # diff.seconds:35880(1巡目)
    total_minutes += diff.seconds // 60

    # 秒を分に変換する。
    print(f"total_minutes:{total_minutes}")  # total_minutes:598(1巡目)

# 分を時間に変換する。
hours = total_minutes // 60

# 60分で時間変換できなかった値を分として算出。
minutes = total_minutes % 60

# 指定された形式で出力。(hh mm)
print(f"{hours} {minutes}")
