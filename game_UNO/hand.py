class Hand:
    def __init__(self):
        """
               Initialise la main avec une liste de cartes vide.
               """
        self.cards = []

    def add_card(self, card):
        """
              Ajoute une carte à la main.
              """
        self.cards.append(card)

    def remove_card(self, index):
        """
              Retire une carte de la main à l'index spécifié et la retourne.
              """
        return self.cards.pop(index)

    def nb_of_cards(self):
        """
             Retourne le nombre de cartes dans la main.
             """
        return len(self.cards)

    def cards_in_hand(self):
        """
              Affiche les cartes dans la main avec leur index.
              """
        for i, card in enumerate(self.cards):
            print(f"{i}: {card}")

    def single_card(self, index):
        """
             Retourne la carte à l'index spécifié.
             """
        return self.cards[index]