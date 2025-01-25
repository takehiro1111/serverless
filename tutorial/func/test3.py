# 紙幣の組み合わせを見つける関数を定義
def find_bills(N, Y):
   # 10000円札の枚数を0からNまで試す
   for x10k in range(N + 1):
       # 5000円札の枚数を0から(N - 10000円札の枚数)まで試す
       for x5k in range(N + 1 - x10k):
           # 1000円札の枚数は全体の枚数から10000円札と5000円札を引いた残り
           x1k = N - x10k - x5k
           
           # 各紙幣の合計金額を計算
           total = 10000 * x10k + 5000 * x5k + 1000 * x1k
           
           # 計算した合計金額が目標金額と一致し、1000円札が0以上なら
           if total == Y and x1k >= 0:
               # 見つかった組み合わせを返す
               return x10k, x5k, x1k
   
   # どの組み合わせも条件を満たさない場合は-1を返す
   return -1, -1, -1

# スペース区切りの2つの整数を入力として受け取り、それぞれNとYに代入
N, Y = map(int, input().split())

# 関数を実行して結果を受け取る
x10k, x5k, x1k = find_bills(N, Y)

# 結果をスペース区切りで出力
print(f"{x10k} {x5k} {x1k}")
