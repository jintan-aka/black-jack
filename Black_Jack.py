import time
import random
import sys
from enum import Enum

# --- 定数 ---
SUITS: list[str] = ["♠", "♥", "♦", "♣"]
RANKS: list[str] = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


# --- Enum（選択肢） ---
class Choice(Enum):
    HIT = "H"
    STAND = ""


# --- クラス定義 ---
class Card:
    def __init__(self, rank: str, suit: str):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"


class Deck:
    def __init__(self):
        # カードのデッキを作成
        self.deck = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop() if self.deck else None


class Player:
    def __init__(self, name="player"):
        self.name = name
        self.hands = []

    def receive_card(self, card: Card) -> None:
        if not card:
            raise Exception("カードが存在しません")
        self.hands.append(card)

    def show_hand(self) -> str:
        return " ".join(str(card) for card in self.hands)

    def calc_score(self):
        score = 0
        ace_count = 0
        for card in self.hands:
            rank = card.rank  # マークを除いた部分
            if rank in ["J", "Q", "K"]:
                score += 10
            elif rank == "A":
                ace_count += 1
                score += 11  # とりあえず11で加算
            else:
                score += int(rank)
        # エースがあって22を超えたら1として数える
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1
        return score


class HumanPlayer(Player):
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


class Dealer(Player):
    def __init__(self, name="ディーラー"):
        super().__init__(name)

    def should_hit(self, deck):
        # ディーラーは17未満ならヒット
        while True:
            if self.calc_score() < 17:
                card = deck.draw()
                self.receive_card(card)
                time.sleep(1)
                print("ディーラーの新しい手札:", self.show_hand())
                score = self.calc_score()

                def bust_check(score):
                    if score > 21:
                        print("バスト！")
                        print(f"{player.name}の勝ちです。")
                        if player_blackjack:
                            print(f"🎉Blackjack!! {player.name}の勝ちです！")
                        sys.exit()
                    else:
                        pass

                bust_check(score)

            else:
                score = self.calc_score()
                print("ディーラーの得点：", score)
                time.sleep(1)
                break  # スタンドしたらループを抜ける


# --- ゲームの実行 ---

deck = Deck()
dealer = Dealer()

name = input(" - あなたの名前を入力してください - :")
player = HumanPlayer(name)

print("プレイスユアベット")
time.sleep(1)
input("【 - ベットが終了したらEnterを押してください - 】")

print("ノーモアベット")
time.sleep(1)

# 1.初期配布
for _ in range(2):
    player.receive_card(deck.draw())
    dealer.receive_card(deck.draw())

# 2.1 手札表示
print(f"{player.name}の手札:", player.show_hand())
print("ディーラーの手札:", f"{dealer.hands[0]} ❓")

# 3.プレイヤーターン
# ブラックジャック判定の定義
player_blackjack = player.calc_score() == 21 and len(player.hands) == 2
dealer_blackjack = dealer.calc_score() == 21 and len(dealer.hands) == 2

if player_blackjack:  # ブラックジャック演出だけ先に表示
    print("🎉Blackjack!!")
else:
    player.want_hit(deck)

# 4.1 ディーラーターン
print("ディーラーの手札:", dealer.show_hand())

if dealer_blackjack:  # ブラックジャック演出だけ先に表示
    print("💥Blackjack!!")
    if not player_blackjack:
        print("Lose... ディーラーのBlackjack💥")
        sys.exit()

dealer.should_hit(deck)

# 5.勝敗判定
player_score = player.calc_score()
dealer_score = dealer.calc_score()

print(f"{player.name}: {player_score} 点 / ディーラー: {dealer_score} 点")

if player_blackjack and not dealer_blackjack:
    print(f"🎉Blackjack!! {player.name}の勝ちです。")
elif dealer_blackjack and not player_blackjack:
    print("Lose... ディーラーのBlackjack💥")
elif player_blackjack and dealer_blackjack:
    print("両者Blackjack! プッシュ! 引き分けです。")

elif player_score > dealer_score:
    print(f"Win! {player.name}の勝ちです。")
elif player_score < dealer_score:
    print("Lose... ディーラーの勝ちです。")
else:
    print("プッシュ！引き分けです。")
