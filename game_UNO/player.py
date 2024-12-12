from game_UNO import Hand

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def draw_card(self, deck):
        card = deck.deal()
        if card:
            self.hand.add_card(card)
        return card

    def play_card(self, index, discard_pile):
        card = self.hand.remove_card(index)
        discard_pile.append(card)
        return card

    def last_card_check(self):
        return all(card.cardtype == "number" for card in self.hand.cards)

    def win_check(self):
        return self.hand.nb_of_cards() == 0

    def __str__(self):
        return f"{self.name} (Cards: {self.hand.nb_of_cards()})"