"""C089:ストラックアウト

あなたはお祭りでストラックアウトを出すことになりました。
ストラックアウトは H × W のマス状に配置されたパネルを撃ち抜くゲームです。
それぞれのパネルにはそれぞれの得点が書かれており、ゲームが終了した際、撃ち抜かれたパネルの得点を合計して最終得点を出します。
撃ち抜かれたパネルとそれぞれの得点が与えられるので、得点集計を自動化するプログラムを作成してください。

入力例 1 の場合、4 × 3 マスのパネルが与えられます。それぞれのパネルには、下図のように得点が割り当てられています。
ゲーム終了後には、それぞれのパネルが撃ち抜かれているか、残っているかが、それぞれ半角アルファベットの "o" と "x" で示されます。
下図では、1, 3, 4, 5, 7, 9 のパネルが撃ち抜かれているので、期待される出力はそれらの合計である 29 となります。

入力される値
入力は以下のフォーマットで与えられます。

H W
s_1
s_2
...
s_H
p_{1,1} p_{1,2} ... p_{1,W}
p_{2,1} p_{2,2} ... p_{2,W}
...
p_{H,1} p_{H,2} ... p_{H,W}
・1 行目にそれぞれストラックアウトの高さ、幅を表す整数 H, W がこの順で半角スペース区切りで与えられます。
・続く H 行のうちの i 行目 (1 ≦ i ≦ H) には半角アルファベット "o" および "x" からなる長さ W の文字列 s_i が与えられます。s_i の j 番目 (1 ≦ j ≦ W) の文字はゲーム終了時の i 行 j 列のパネルの状態を表し、"o" は撃ち抜かれた状態を、"x" はそのパネルが残っている状態を表します。
・続く H 行のうちの i 行目 (1 ≦ i ≦ H) には W 個の整数が半角スペース区切りで与えられます。i 行目の j 番目 (1 ≦ i ≦ W) の整数 p_{i, j} はストラックアウトの i 行 j 列目のパネルの得点を表します。
・入力は合計で 2 * H + 1 行となり、入力値最終行の末尾に改行が 1 つ入ります。

期待する出力
最終得点を整数で出力してください。

"""

# マス目の高さ、幅の受け取り
height, weight = list(map(int, input().split()))

# マス目のoxの入力の受け取り
panel_score = [input() for i in range(1, height + 1)]
# print(panel_score)
# ['oxo', 'oox', 'oxo', 'xxx']
# リストを各要素に分割
flat_panel_score = [score_element for score in panel_score for score_element in score]
# print(flat_panel_score)

# パネルの数字の受け取り
panel_num = [list(map(int, input().split())) for _ in range(height)]
# print(panel_num)
# ['1 2 3', '4 5 6', '7 8 9', '10 11 12']
# リストを各要素に分割
flat_panel_num = [num for row in panel_num for num in row]
# print(flat_panel_num)

### 上記まででそれぞれリストで持っている。

total_score = 0
# リストの要素をマッピングする。
for score, num in zip(flat_panel_score, flat_panel_num):
    # "o"なら加算。
    if score == "o":
        total_score += num

print(total_score)
