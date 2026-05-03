def two_sum(nums, target):
    # 値を保管する用の辞書
    memo = {}

    for i, num in enumerate(nums):
        # 相方の値を定義
        partner_num = target - num

        # 相方の数値があれば添字のペアを配列で返す
        if partner_num in memo:
            return [memo[partner_num], i]

        memo[num] = i

    return []


print("結果:", two_sum([2, 11, 7, 15], 9))
