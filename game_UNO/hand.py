class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, index):
        return self.cards.pop(index)

    def nb_of_cards(self):
        return len(self.cards)

    def cards_in_hand(self):
        for i, card in enumerate(self.cards):
            print(f"{i}: {card}")

    def single_card(self, index):
        return self.cards[index]