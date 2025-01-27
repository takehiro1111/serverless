"""C149:大文字小文字
あなたは、とある会社で文字列の校正を行う仕事をしています。

校正ルール表と校正ルールに則って、校正を行います。
校正ルール表は以下の条件を満たす、長さ 26 の文字列です。

・i 番目の文字は英字アルファベット順で i 番目の文字の大文字または小文字

校正ルールは以下のとおりです。

・校正する文章に登場する全ての英字アルファベットについて、校正ルール表に書かれた英字アルファベットと 大文字/小文字 が一致するように書き換える

校正ルール表および校正前の文字列が与えられるので、校正ルールに従って校正を行った後の文字列を出力するプログラムを作成してください。

例えば、入力例 1 の場合、以下のようになります。

入力例1
abcdEFGHijklMNOPqrstUVWXyz
PAIZA

出力例1
Paiza
"""


# 一致するアルファベットを抜き取って校正前の文字列の状態で出力する。
# 大文字と小文字を区別する。
def correct_text(rule_str, text):
    # アルファベットのインデックスを取得する辞書を作成
    char_to_index = {
        character: i for i, character in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    }
    print(f"char_to_index:{char_to_index}")

    result = ""
    for char in text:
        # charが全て英字且つ1文字以上あればTrue
        if char.isalpha():
            # 大文字に変換してインデックスを取得
            # 辞書[キー]
            idx = char_to_index[char]
            print(f"char:{char}")
            print(f"idx{idx}")
            print(f"rule_str[idx]:{rule_str[idx]}")
            # resultに取得した文字を入れる。
            result += rule_str[idx]
            print(f"result:{result}")
        else:
            result += char

    return result


# 校正前の文字列の受け取り
before_calibration = str(input())

# 校正ルール表の受け取り
calibration_rule = str(input())

print(correct_text(before_calibration, calibration_rule))
