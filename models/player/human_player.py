import time
import sys
from ..card.choice import Choice
from .player import Player


class Human_Player(Player):
    def __init__(self, name="あなた"):
        super().__init__(name)

    def want_hit(self, deck):
        while True:
            # ユーザーにヒットするか尋ねる
            choice = input(
                "カードを追加（ヒット）する場合は、”H” と入力してください。カードがいらない場合（スタンド）は Enter: "
            ).upper()

            try:
                action = Choice(choice)
            except ValueError:
                print("無効な入力です。”H” か Enter を入力してください。")
                continue

            if action == Choice.HIT:
                card = deck.draw()
                self.receive_card(card)
                time.sleep(1)
                print(f"{self.name}の新しい手札:", self.show_hand())
                score = self.calc_score()
                print("現在の得点：", score)

                if score > 21:
                    print("バスト！")
                    print("ディーラーの勝ちです。")
                    sys.exit()

            elif action == Choice.STAND:
                score = self.calc_score()
                print(f"{self.name}の最終得点：", score)
                break
