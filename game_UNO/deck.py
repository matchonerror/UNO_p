import random
from game_UNO import Card, Color, Rank, CardType

class Deck:
    def __init__(self):
        """
              Initialise le paquet de cartes et mélange les cartes.
              """
        self.cards = self.create_deck()
        random.shuffle(self.cards)
        self.discard_pile = []

    def create_deck(self):
        """
               Crée un paquet de cartes UNO avec les cartes numérotées et les cartes d'action.
               """
        deck = []

        # Add number cards and action cards for each color
        for color in [Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE]:
            # Number cards: 0-9 (two of each, except 0)
            for rank in list(Rank)[0:10]:  # First 10 ranks (0-9)
                card_type = CardType.NUMBER
                deck.append(Card(color, rank, card_type))
                if rank != Rank.ZERO:
                    deck.append(Card(color, rank, card_type))

            # Action cards: Skip, Reverse, Draw Two (two of each)
            for rank in [Rank.SKIP, Rank.REVERSE, Rank.DRAW_TWO]:
                card_type = CardType.ACTION
                deck.append(Card(color, rank, card_type))
                deck.append(Card(color, rank, card_type))

        # Add Wild cards: Wild and Draw Four (four of each)
        for rank in [Rank.WILD, Rank.DRAW_FOUR]:
            for _ in range(4):
                deck.append(Card(Color.WILD, rank, CardType.ACTION))

        return deck

    def deal(self):
        """
                Distribue une carte du paquet. Retourne None si le paquet est vide.
                """
        if not self.cards:
            print(f"Deck is empty!")
            return None
        return self.cards.pop()
    def top_discard(self):
        """
                Retourne la carte du dessus de la pile de défausse.
                """
        return self.discard_pile[-1] if self.discard_pile else None
