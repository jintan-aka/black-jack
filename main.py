import time
import sys

from models import Card, Deck, Player, Human_Player, Dealer


# --- ゲームの実行 ---
deck = Deck()
dealer = Dealer()

name = input(" - あなたの名前を入力してください - :")
player = Human_Player(name)

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

# 3.ブラックジャック判定（先にチェック）
player_blackjack = player.is_blackjack()
dealer_blackjack = dealer.is_blackjack()

# プレイヤーターン
if player_blackjack:
    print("🎉Blackjack!!")
else:
    player.want_hit(deck)

# ディーラーターン
print("ディーラーの手札:", dealer.show_hand())

if dealer_blackjack:
    print("💥Blackjack!!")
    if not player_blackjack:
        print("Lose... ディーラーのBlackjack💥")
        sys.exit()

dealer.should_hit(deck, player)

# 5.勝敗判定（さっきの結果を使う）
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
