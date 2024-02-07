import random

# 指示のリストを定義
instructions = [
    "旗を上げろ",
    "旗を下げろ",
    "左の旗を上げろ",
    "左の旗を下げろ",
    "右の旗を上げろ",
    "右の旗を下げろ",
    "旗を上げたら負け",
    "旗を下げたら負け",
]

# ゲームのラウンド数を定義
rounds = 10

instruction = ""
# ラウンドごとにランダムな指示を出力
for i in range(rounds):
    instruction += (
        random.choice(instructions)
        if i == rounds - 1
        else random.choice(instructions) + "\n"
    )

print(instruction)
