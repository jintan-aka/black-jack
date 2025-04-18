import time
import sys
from .player import Player
from .human_player import Human_Player


class Dealer(Player):
    def __init__(self, name="ディーラー"):
        super().__init__(name)

    def should_hit(self, deck, player):
        def bust_check(score, player):
            if score > 21:
                print("バスト！")
                print(f"{player.name}の勝ちです。")
                if player.is_blackjack:
                    print(f"🎉Blackjack!! {player.name}の勝ちです！")
                sys.exit()
            else:
                pass

        # ディーラーは17未満ならヒット
        while True:
            if self.calc_score() < 17:
                card = deck.draw()
                self.receive_card(card)
                time.sleep(1)
                print("ディーラーの新しい手札:", self.show_hand())
                score = self.calc_score()

                bust_check(score, player)

            else:
                score = self.calc_score()
                print("ディーラーの得点：", score)
                time.sleep(1)
                break  # スタンドしたらループを抜ける
