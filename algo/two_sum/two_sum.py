class Solution:
    def two_sum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        # 「今まで見た値」を記録する箱
        # 辞書型
        memo = {}
        # numsを1つずつ取り出す。i=添え字, num=値
        for i, num in enumerate(nums):
            print(f"--- {i+1}周目 ---")
            print(f"i={i}, num={num}")

            # 自分とペアになる相手の値を定義
            partner_num = target - num
            print(f"partner_num = {target} - {num} = {partner_num}")
            print(f"現在のmemo = {memo}")

            # memoの中に相手の値があれば
            if partner_num in memo:
                # いれば「相手の添え字」と「自分の添え字」を返して終了
                print(f"→ {partner_num} はmemoにある! 答え発見\n")
                return [memo[partner_num], i]

            # いなければ自分を登録(次以降のループで誰かの相手になれるように)
            print(f"→ {partner_num} はmemoに無い。自分を記録 memo={memo}\n")
            memo[num] = i
            print("新しく記録したメモ:", memo)
        return []


sol = Solution()
print("結果:", sol.two_sum([2, 11, 7, 15], 9))
