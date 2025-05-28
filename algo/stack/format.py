"""
lookupのキーと開き括弧が一致した場合はペアになる閉じ括弧をスタックに入れる。
それで閉じ括弧のイテレータを処理するときにスタックの中から取り出して一致すれば正しいネストのデータ構造になる。
一致しなかったり、そもそもスタックに閉じ括弧が入っていない(開き括弧がないのに閉じ括弧がある)なら不正なネスト構造ということ。
また、最終的に閉じ括弧を全て処理してもネストの中にまだ要素があれば、括弧が完全に対になっていないため不正と判断される。
"""


def validate_format(chars):
    lookup = {"{": "}", "[": "]", "(": ")"}
    stack = []

    for char in chars:
        # lookupの中のキーのいずれかに合致する場合はスタックに追加する。
        if char in lookup.keys():
            # バリュー(閉じ括弧)をスタックへ入れる
            print(stack)
            stack.append(lookup[char])

            print(
                f"開き括弧 '{char}' 発見 → 期待する閉じ括弧 '{lookup[char]}' をスタックに積む"
            )
            print(f"現在のスタック: {stack}")

        # loookupのバリューのいずれかに合致する場合はスタックから取り出す。
        if char in lookup.values():
            print(f"char: {char}")
            # 先に開き括弧が入っていない場合は不正な括弧とみなしたいため。
            if not stack:
                return False

            # 　スタックから取り出した閉じ括弧がこのイテレータの閉じ括弧と一致しない場合はFalse
            if char != stack.pop():
                return False

            print(f"現在のスタック: {stack}")

    if stack:
        return False

    print(f"現在のスタック: {stack}")

    return True


if __name__ == "__main__":
    j = "{'key1': 'value1', 'key2': [1,2,3]}"
    print(validate_format(j))
