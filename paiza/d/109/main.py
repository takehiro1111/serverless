"""D109:ゾロ目の日付

11 月 11 日が迫るある日、あなたはゾロ目の日付を判定するプログラムを作成することにしました。

ゾロ目の日とはある日付に対して 月 と 日 に含まれる全ての桁の数字が同じものを指します。
スペース区切りで月と日が与えられるのでゾロ目の日であれば "Yes" そうでなければ "No" と出力してください。

例えば入力例 1 では 11 月 1 日が以下のように与えられます。

11 1
この場合、月と日ともに 1 のゾロ目なので

Yes
と出力して下さい。
"""

month, day = map(str, input().split())

month_digits = set(map(int, month))
day_digits = set(map(int, day))

print("Yes" if month_digits == day_digits else "No")
