from game_UNO import Hand

class Player:
    def __init__(self, name):
        """
               Initialise un joueur avec un nom et une main vide.
               """
        self.name = name
        self.hand = Hand()

    def draw_card(self, deck):
        """
                Pioche une carte du paquet et l'ajoute à la main du joueur.
                """
        card = deck.deal()
        if card:
            self.hand.add_card(card)
        return card

    def play_card(self, index, discard_pile):
        """
               Joue une carte de la main du joueur et l'ajoute à la pile de défausse.
               """
        card = self.hand.remove_card(index)
        discard_pile.append(card)
        return card

    def last_card_check(self):
        """
                Vérifie si toutes les cartes restantes dans la main sont des cartes numérotées.
                """
        return all(card.cardtype == "number" for card in self.hand.cards)

    def win_check(self):
        """
                Vérifie si le joueur a gagné (plus de cartes dans la main).
                """
        return self.hand.nb_of_cards() == 0

    def __str__(self):
        """
                Retourne une représentation en chaîne de caractères du joueur et du nombre de cartes dans sa main.
                """
        return f"{self.name} (Cards: {self.hand.nb_of_cards()})"