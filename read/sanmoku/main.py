import math
import random

# 先攻と後攻の定義
FIRST = "○"
SECOND = "x"
mark = {0: "-", 1: "", -1: ""}
# 1：プレイヤー、-1：コンピュータ

# 碁盤の値
field = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# 入力値
input_number = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def senkou_koukou():
    print("先攻（○）後攻（×）を決めます。")
    choice = int(input("0か1を入力してください。"))
    first_attack = random.randint(0, 1)
    print("先攻は " + str(first_attack) + "です。")

    if choice == first_attack:
        print("あなたは先攻です。")
        mark[1] = FIRST
        mark[-1] = SECOND
    else:
        print("あなたは後攻です。")
        mark[1] = SECOND
        mark[-1] = FIRST

    print(mark)


def print_field():
    str_line = ""
    print("")
    print("=====")
    for i in range(3):  # 3行分繰り返し
        for j in range(3):  # 各行で3カラム分処理
            if field[i][j] == 0:
                # マスが空いている(0の)場合、マス番号（1-9）を表示
                str_line += input_number[i * 3 + j]
            else:
                # マスが埋まっている場合、マーク（〇や×）を表示
                str_line += mark[field[i][j]]
            if j < 2:
                # マスとマスの間に区切り文字"|"を追加（最後のマス以外）
                str_line += "|"
        print(str_line)  # 完成した1行を表示
        str_line = ""  # 次の行のために初期化
        if i < 2:
            print("-+-+-")  # 最後の行以外の後に区切り線を表示
    print("=====")
    print("")


def input_player(turn):
    print("表示されている番号のいずれかを入力してください。")
    while True:
        input_str = input("")
        if input_str.isdigit():  # 数字ならTrueを返す。
            input_int = int(input_str)
            if input_int >= 1 and input_int <= 9:
                # 入力値から行（row）を計算
                # 例: 7の場合 → (7-1)/3 = 2 (3行目)
                row = math.floor((input_int - 1) / 3)
                # 入力値から列（column）を計算
                # 例: 7の場合 → (7-1)%3 = 0 (1列目)
                col = (input_int - 1) % 3
                if field[row][col] == 0:  # まだ選択されてないマスなら
                    field[row][col] = 1  # マス目へ入力する。
                    break
        print("")
        print("もう一度、表示されている番号のいずれかを入力してください。")


def input_computer(turn):
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if field[row][col] == 0:
            print("コンピュータは " + str(row * 3 + col + 1) + " を選びました。")
            field[row][col] = -1
            break


def check_winner(player_number):
    win = False
    for i in range(3):
        if sum(field[i]) == player_number * 3:
            win = True
            break
    if win == False:
        for j in range(3):
            if field[0][j] + field[1][j] + field[2][j] == player_number * 3:
                win = True
                break
    if win == False:
        if field[0][0] + field[1][1] + field[2][2] == player_number * 3:
            win = True
        elif field[2][0] + field[1][1] + field[0][2] == player_number * 3:
            win = True

    return win


def field_full():
    is_full = True
    for i in range(3):
        for j in range(3):
            if field[i][j] == 0:
                is_full = False
    return is_full


senkou_koukou()
print_field()


finish = False
turn = FIRST
while finish == False:
    if mark[1] == turn:  # mark[1]のプレーヤーの順番がFIRSTなら
        input_player(turn)
        print_field()
        if check_winner(1) == True:
            print("あなたの勝ち")
            finish = True
    else:
        input_computer(turn)
        print_field()
        if check_winner(-1):
            print("あなたの負け")
            finish = True

    if finish == False and field_full() == True:
        print("引き分け")
        finish = True

    if turn == FIRST:
        turn = SECOND
    else:
        turn = FIRST
