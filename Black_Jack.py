import time
import random
import sys

print("プレイスユアベット")
time.sleep(1)
input("【 - ベットが終了したらEnterを押してください - 】")

print("ノーモアベット")
time.sleep(1)

class Deck:
    def __init__(self):
        # カードのデッキを作成
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(self.deck)
    
    def draw(self):
        return self.deck.pop() if self.deck else None
    def deal(self, num):
        return[self.draw() for _ in range(num)]

class Player:
    def __init__(self, name="player"):
        self.name = name
        self.hand = []

    def receive_card(self, card):
        if card:
            self.hand.append(card)
    
    def show_hand(self):
        return self.hand

    def calc_score(self):
        score = 0
        ace_count = 0
        for card in self.hand:
            rank = card[:-1]  # マークを除いた部分
            if rank in ['J', 'Q', 'K']:
               score += 10
            elif rank == 'A':
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
            choice = input("カードを追加（ヒット）する場合は、”H”と入力してください。カードがいらない場合（スタンド）は Enter: ")
            if choice.upper() == "H":
                card = deck.draw()
                self.receive_card(card)
                time.sleep(1)
                print("あなたの新しい手札:", self.show_hand())
                score = self.calc_score()
                print("現在の得点：", score)
               
                if score > 21:
                    print("バスト！")
                    print("ディーラーの勝ちです。")
                    sys.exit()                
                                        
            else:
                score = self.calc_score()
                print("あなたの最終得点：", score)
                break
            
        

class Dealer(Player):
    def __init__(self, name="ディーラー"):
        super().__init__(name)
    
    def should_hit(self, deck):
        # ディーラーは17未満ならヒット
        while True:
            if self.calc_score() < 17 :
                card = deck.draw()
                self.receive_card(card)
                time.sleep(1)
                print("ディーラーの新しい手札:", self.show_hand())
                score = self.calc_score()

                def Bust_check(score):
                    if score > 21:
                        print("バスト！")
                        print("あなたの勝ちです。")
                        if player_blackjack:
                           print("🎉Blackjack!! あなたの勝ちです！")
                        sys.exit()
                    else:
                        pass
                    
                Bust_check(score)
        
            else:
                score = self.calc_score()
                print("ディーラーの得点：", score)
                time.sleep(1)
                break    # スタンドしたらループを抜ける

# --- ゲームの実行 ---

deck = Deck()
player = HumanPlayer()
dealer = Dealer()

# 1.初期配布
for _ in range(2):
    player.receive_card(deck.draw())
    dealer.receive_card(deck.draw())

# 2.1 手札表示
print("あなたの手札:", player.show_hand())
print("ディーラーの手札:", [dealer.show_hand()[0], "??"])
# 2.2 ブラックジャック判定の定義
player_blackjack = (player.calc_score()==21  and  len(player.hand)==2 )
dealer_blackjack = (dealer.calc_score()==21  and  len(dealer.hand)==2 )
# 2.3 ブラックジャック演出だけ先に表示
if player_blackjack:
    print("🎉Blackjack!!")

# 3.プレイヤーターン
player.want_hit(deck)

# 4.1 ディーラーターン
print("ディーラーの手札:", dealer.show_hand())
# 4.2 ブラックジャック演出だけ先に表示
if dealer_blackjack:
    print("💥Blackjack!!")
dealer.should_hit(deck)

# 5.勝敗判定
player_score = player.calc_score()
dealer_score = dealer.calc_score()

print(f"あなた: {player_score} 点 / ディーラー: {dealer_score} 点")

if player_blackjack and not dealer_blackjack:
    print("🎉Blackjack!! あなたの勝ちです。")
elif dealer_blackjack and not player_blackjack:
    print("Lose... ディーラーのBlackjack💥")
elif player_blackjack and dealer_blackjack:
    print("両者Blackjack! プッシュ! 引き分けです。")

elif player_score > dealer_score:
    print("Win! あなたの勝ちです。")
elif player_score < dealer_score:
    print("Lose... ディーラーの勝ちです。")
else:
    print("プッシュ！引き分けです。")



