"""C075:ポイント払い
paiza 市に住んでいるあなたは、普段の移動手段は全て paiza バスを使います。paiza バスでは paica という
IC カードを乗車券として使うことができます。事前に paica にチャージをすることで利用できます。

バスの運賃支払に paica のカード残額を使うと、運賃の 10 % が paica ポイントとしてたまります。

バスを降車する時に、支払う運賃以上のポイントがある場合は、ポイントが優先的に運賃の支払いに使われます。
ただし、1 ポイントは 1 円になります。ただし、ポイントで運賃を支払った場合、新たなポイントは発生しません。

入力例1
2000 5
300
500
300
100
100

出力例1
1700 30
1200 80
900 110
900 10
800 20

"""

# 最初のカード残高(お金)と乗車回数のstdinを取得
first_money, num = list(map(int,input().split()))

# ポイントの初期値
point = 0


# 乗車毎ごとの残高とポイントを出力
for i in range(1,num+1):
  # 乗車賃の取得
  fee = int(input())
  
  # 支払い方法の条件を指定して、計算する。
  if fee >= point:
    # 残高から払う場合は残高の10%をポイントとして加算
    point += (fee * 0.1)
    
    first_money -= fee
    
  elif fee <= point:
    point -= fee
    # ポイントから支払う場合はポイント加算は行われない。
  
  # 乗車毎に乗車賃とポイントの出力
  print(f"{first_money} {int(point)}")
    
