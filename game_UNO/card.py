from enum import Enum

class Color(Enum):
    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLUE = "Blue"
    WILD = 'Wild'
class Rank(Enum):
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    SKIP = "Skip"
    REVERSE = "Reverse"
    DRAW_TWO = "Draw2"
    WILD = "Wild"
    DRAW_FOUR = "Draw4"

class CardType(Enum):
    NUMBER = "Number"
    ACTION = "Action"

class Card:
    def __init__(self, color: Color, rank: Rank, card_type: CardType):
        """
                Initialise une carte avec une couleur, un rang et un type.
        """
        self.color = color
        self.rank = rank
        self.card_type = card_type

    def __str__(self):
        """
                Initialise une carte avec une couleur, un rang et un type.
        """
        return f"{self.color.value} {self.rank.value} ({self.card_type.value})"