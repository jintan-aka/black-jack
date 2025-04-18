import random
from .card import Card

# --- 定数 ---
SUITS: list[str] = ["♠", "♥", "♦", "♣"]
RANKS: list[str] = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


class Deck:
    def __init__(self):
        # カードのデッキを作成
        self.deck = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop() if self.deck else None
