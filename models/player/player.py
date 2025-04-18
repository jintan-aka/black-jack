from ..card.card import Card


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

    # ブラックジャック判定の定義
    def is_blackjack(self) -> bool:
        return self.calc_score() == 21 and len(self.hands) == 2
