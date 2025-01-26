"""C055:ログのフィルター
あなたはサーバ管理者です。 日々洪水のように流れるログを追っています。
とうとう自分の目と頭では処理しきれない量になってしまったため、プログラムを作って、重要な文字列を含むログだけ抽出する事にしました。

例えば、入力例 2 では、ログは上から順に "pizza"、 "paiza"、 "aizu"、 "ai"、 "sai" の 5 つです。
この 5 つのログに対して、重要な文字列 "ai" が含まれているのは "pizza" 以外の 4 つです。
結果として "pizza" だけが除かれ、 "paiza"、 "aizu"、 "ai"、 "sai" がこの順に抽出されます。

このように、ログと重要な文字列が与えられたとき、重要な文字列が含まれているログを抽出して出力するプログラムを作成してください。
重要な文字列が含まれていない場合は "None" と出力してください。

入力例1
1
paiza
paizaonlinehackathon

出力例1
paizaonlinehackathon
"""

# イテラブルとして回す文字列の数を取得
TARGET_NUM = int(input())

# フィルターする文字列を定義
FLITER_WORD = str(input())


for i in range(1, TARGET_NUM + 1):
    TARGET_WORD = str(input())

    # フィルターする文字列と重なっているか判定
    if FLITER_WORD in TARGET_WORD:
        print(TARGET_WORD)
